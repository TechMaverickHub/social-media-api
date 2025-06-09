import logging

from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.core.views import CustomPageNumberPagination
from app.global_constants import SuccessMessage, ErrorMessage
from app.post.models import Post
from app.post.serializers import PostCreateSerializer, PostDisplaySerializer, PostListFilterDisplaySerializer
from app.utils import get_response_schema
from permissions import IsUser

logger = logging.getLogger('django')

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

class PostDetailAPI(GenericAPIView):

    permission_classes = [IsUser]

    def get_object(self, pk):

        user_queryset = (Post.objects.select_related('user')
                         .filter(pk=pk,is_active=True,user_id=self.request.user.id)
                         .only('title', 'content', 'image'))
        if user_queryset:
            return user_queryset[0]
        return None

    def get(self, request, pk):
        logger.info(f"Post accessed by user: {request.user}. Requested user ID: {pk}")

        if not pk:
            logger.warning("Bad request: No primary key provided.")
            return get_response_schema({}, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

        post = self.get_object(pk)
        if not post:
            logger.error(f"Error retrieving post with ID {pk}", exc_info=True)
            return get_response_schema(
                {},
                ErrorMessage.NOT_FOUND.value,
                status.HTTP_404_NOT_FOUND
            )

        serializer = PostDisplaySerializer(post)
        logger.info(f"Successfully retrieved post with ID {pk}")
        return get_response_schema(
            serializer.data,
            SuccessMessage.RECORD_RETRIEVED.value,
            status.HTTP_200_OK
        )


class PostListFilterAPIView(ListAPIView):
    """ View: Post List Filter"""

    serializer_class = PostListFilterDisplaySerializer
    pagination_class = CustomPageNumberPagination

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser]

    def get_queryset(self):

        query_params = self.request.query_params

        # Only fetch necessary fields to optimize performance
        queryset = Post.objects.select_related('user').filter(
            is_active=True,
            user_id = self.request.user.id
        ).only(
            'user','title', 'content', 'image'
        ).order_by('-created')

        # Extract filters
        title = query_params.get('title')
        content = query_params.get('content')

        # Apply filters
        if title:
            queryset = queryset.filter(title__istartswith=title)
        if content:
            queryset = queryset.filter(content__istartswith=content)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='Filter by title'),
            openapi.Parameter('content', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description='Filter by content'),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)