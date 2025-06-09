from rest_framework import serializers

from app.post.models import Post


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('user', 'title', 'content', 'image')
        extra_kwargs = {
            'user': {'write_only': True}
        }