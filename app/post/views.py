from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.throttling import AnonRateThrottle

from app.global_constants import SuccessMessage, ErrorMessage
from app.post.serializers import PostCreateSerializer
from app.utils import get_response_schema
from permissions import IsUser


class UserPostThrottle(AnonRateThrottle):
    """Custom throttle for Post endpoint"""
    rate = '5/hour'


# Create your views here.
class PostCreateAPIView(GenericAPIView):
    """ View: Create Post(Only Users)"""

    permission_classes = [IsUser]
    throttle_classes = [UserPostThrottle]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Content'),
                'image': openapi.Schema(type=openapi.TYPE_STRING, format='binary',
                                                  description='Profile picture'),
            }
        )
    )
    def post(self, request):
        with transaction.atomic():
            request.data['user'] = request.user.id

            serializer = PostCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return get_response_schema(serializer.data,SuccessMessage.RECORD_CREATED.value, status.HTTP_201_CREATED)

            return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)
