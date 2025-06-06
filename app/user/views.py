import logging

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from app.core.views import CustomPageNumberPagination
from app.global_constants import SuccessMessage, ErrorMessage, GlobalValues
from app.user.serializers import UserDisplaySerializer, UserCreateSerializer, UserListFilterDisplaySerializer
from app.utils import get_response_schema
from permissions import IsSuperAdmin

logger = logging.getLogger('django')

class UserCreateThrottle(AnonRateThrottle):
    """Custom throttle for login endpoint"""
    rate = '10/hour'


class SuperAdminSetupView(GenericAPIView):
    """ View: Admin setup """
    throttle_classes = [UserCreateThrottle]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
                'bio': openapi.Schema(type=openapi.TYPE_STRING, description='Biography'),
                'birth_date': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Birth date'),
                'location': openapi.Schema(type=openapi.TYPE_STRING, description='Location'),
                'website': openapi.Schema(type=openapi.TYPE_STRING, format='url', description='Website'),
                'profile_picture': openapi.Schema(type=openapi.TYPE_STRING, format='binary',
                                                  description='Profile picture'),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
                'is_private': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is private'),
            }
        )
    )
    def post(self, request):
        with transaction.atomic():
            request.data['role'] = GlobalValues.SUPER_ADMIN

            serializer = UserCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                user = get_user_model().objects.get(pk=serializer.data['pk'])
                response_serializer = UserDisplaySerializer(user)

                return get_response_schema(response_serializer.data, SuccessMessage.RECORD_CREATED,
                                           status.HTTP_201_CREATED, )

            return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST, status.HTTP_400_BAD_REQUEST)


class UserLoginThrottle(AnonRateThrottle):
    """Custom throttle for login endpoint"""
    rate = '5/hour'


class UserLogin(GenericAPIView):
    """ View: User login """

    throttle_classes = [UserLoginThrottle]
    serializer_class = UserDisplaySerializer

    @swagger_auto_schema(
        request_body=
        openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
        )
    )
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return get_response_schema(
                    {settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: [ErrorMessage.MISSING_FIELDS]},
                    ErrorMessage.BAD_REQUEST,
                    status.HTTP_400_BAD_REQUEST
                )

            user = get_user_model().objects.filter(email=email, is_active=True).first()

            if user is None:
                logger.warning(f"Login attempt for non-existent email: {email}")
                return get_response_schema(
                    {},
                    ErrorMessage.NOT_FOUND,
                    status.HTTP_404_NOT_FOUND
                )

            if not user.check_password(password):
                logger.warning(f"Failed login attempt for user: {email}")
                return get_response_schema(
                    {settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: [ErrorMessage.PASSWORD_MISMATCH]},
                    ErrorMessage.BAD_REQUEST,
                    status.HTTP_400_BAD_REQUEST
                )

            # Successful authentication
            login(request, user)
            refresh = RefreshToken.for_user(user)
            user_data = self.get_serializer(user).data

            # Log successful login (without sensitive data)
            logger.info(f"User {user.id} logged in successfully")

            return_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data
            }

            return get_response_schema(
                return_data,
                SuccessMessage.CREDENTIALS_MATCHED,
                status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)
            return get_response_schema(
                {settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: [ErrorMessage.SOMETHING_WENT_WRONG]},
                ErrorMessage.SOMETHING_WENT_WRONG,
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserLogout(GenericAPIView):
    """ View: User logout """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=
        openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='refresh token'),
            },
        )
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()

            return get_response_schema({}, SuccessMessage.CREDENTIALS_REMOVED, status.HTTP_204_NO_CONTENT)
        except:
            return get_response_schema({}, ErrorMessage.BAD_REQUEST, status.HTTP_400_BAD_REQUEST)


class AdminSetupView(GenericAPIView):
    """ View: Create Admin (Only SuperAdmin can create) """

    permission_classes = [IsSuperAdmin]
    throttle_classes = [UserCreateThrottle]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
                'bio': openapi.Schema(type=openapi.TYPE_STRING, description='Biography'),
                'birth_date': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Birth date'),
                'location': openapi.Schema(type=openapi.TYPE_STRING, description='Location'),
                'website': openapi.Schema(type=openapi.TYPE_STRING, format='url', description='Website'),
                'profile_picture': openapi.Schema(type=openapi.TYPE_STRING, format='binary', description='Profile picture'),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
                'is_private': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is private'),
            }
        )
    )
    def post(self, request):
        with transaction.atomic():
            request.data['role'] = GlobalValues.ADMIN  # set admin role

            serializer = UserCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                user = get_user_model().objects.get(pk=serializer.data['pk'])
                response_serializer = UserDisplaySerializer(user)

                return get_response_schema(
                    response_serializer.data,
                    SuccessMessage.RECORD_CREATED,
                    status.HTTP_201_CREATED
                )

            return get_response_schema(
                serializer.errors,
                ErrorMessage.BAD_REQUEST,
                status.HTTP_400_BAD_REQUEST
            )


class AdminListFilter(ListAPIView):
    """View: Admin List Filter"""

    serializer_class = UserListFilterDisplaySerializer
    pagination_class = CustomPageNumberPagination

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):
        queryset = get_user_model().objects.filter(is_active=True, role_id = GlobalValues.ADMIN).order_by('-id')

        #Filter by first name
        if self.request.query_params.get('first_name'):
            queryset = queryset.filter(first_name__istartswith=self.request.query_params.get('first_name'))

        if self.request.query_params.get('last_name'):
            queryset = queryset.filter(last_name__istartswith=self.request.query_params.get('last_name'))

        if self.request.query_params.get('email'):
            queryset = queryset.filter(email__istartswith=self.request.query_params.get('email'))

        if self.request.query_params.get('username'):
            queryset = queryset.filter(username__istartswith=self.request.query_params.get('email'))

        if self.request.query_params.get('location'):
            queryset = queryset.filter(location__istartswith=self.request.query_params.get('email'))

        if self.request.query_params.get('birth_date'):
            queryset = queryset.filter(birth_date__date=self.request.query_params.get('birth_date'))

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('first_name', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='Filter by first name'),
            openapi.Parameter('last_name', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='Filter by last name'),
            openapi.Parameter('email', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Filter by email'),
            openapi.Parameter('username', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Filter by username'),
            openapi.Parameter('location', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Filter by location'),
            openapi.Parameter('birthdate', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Filter by birthdate', format=openapi.FORMAT_DATE),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

