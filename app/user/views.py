from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from app.global_constants import SuccessMessage, ErrorMessage, GlobalValues
from app.user.serializers import UserDisplaySerializer, UserCreateSerializer
from app.utils import get_response_schema


class SuperAdminSetupView(GenericAPIView):
    """ View: Admin setup """

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
                'is_private': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is private'),
            }
        )
    )
    def post(self, request):
        with transaction.atomic():
            request.data['role'] = GlobalValues.SUPER_ADMIN.value

            serializer = UserCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                user = get_user_model().objects.get(pk=serializer.data['pk'])
                response_serializer = UserDisplaySerializer(user)

                return get_response_schema(response_serializer.data, SuccessMessage.RECORD_CREATED.value,
                                           status.HTTP_201_CREATED, )

            return get_response_schema(serializer.data, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)


class UserLogin(GenericAPIView):
    """ View: User login """

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
        email = request.data.get('email')

        user = get_user_model().objects.filter(email=email, is_active=True).first()

        if user is None:
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        if user.check_password(request.data.get('password')):
            login(request, user)

            # Get token details
            refresh = RefreshToken.for_user(user)

            # Get user details
            user_data = UserDisplaySerializer(user)

            return_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data.data
            }

            return get_response_schema(return_data, SuccessMessage.CREDENTIALS_MATCHED.value, status.HTTP_200_OK)

        return_data = {
            settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: [ErrorMessage.PASSWORD_MISMATCH.value]
        }

        return get_response_schema(return_data, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)


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

            return get_response_schema({}, SuccessMessage.CREDENTIALS_REMOVED.value, status.HTTP_204_NO_CONTENT)
        except:
            return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)
