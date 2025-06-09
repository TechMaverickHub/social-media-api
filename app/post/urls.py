from django.urls import path

from app.post.views import PostCreateAPIView
from app.user.views import SuperAdminSetupView, UserLogin, UserLogout, AdminSetupView, AdminListFilter, UserDetailAPI

urlpatterns = [

    path("", PostCreateAPIView.as_view(),name="post-create")




]
