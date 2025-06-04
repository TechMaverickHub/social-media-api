from django.contrib.auth import get_user_model
from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView

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
                'profile_picture': openapi.Schema(type=openapi.TYPE_STRING, format='binary', description='Profile picture'),
                'is_private': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is private'),
            }
        )
    )
    def post(self, request):
        with transaction.atomic():

            request.data['role'] =  GlobalValues.SUPER_ADMIN.value

            serializer = UserCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                user = get_user_model().objects.get(pk=serializer.data['pk'])
                response_serializer = UserDisplaySerializer(user)

                return get_response_schema(response_serializer.data, SuccessMessage.RECORD_CREATED.value, status.HTTP_201_CREATED,)

            return get_response_schema(serializer.data,ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)
