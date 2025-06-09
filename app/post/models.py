import uuid

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class Post(models.Model):


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign Keys
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='user_posts',
                             related_query_name='user_post')

    # Fields
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)

    # Additional field declarations
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)