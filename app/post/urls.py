from django.urls import path

from app.post.views import PostCreateAPIView, PostDetailAPI, PostListFilterAPIView
from app.user.views import SuperAdminSetupView, UserLogin, UserLogout, AdminSetupView, AdminListFilter, UserDetailAPI

urlpatterns = [

    path("", PostCreateAPIView.as_view(),name="post-create"),
    path('<str:pk>', PostDetailAPI.as_view(), name='post-detail'),
    path('list-filter/', PostListFilterAPIView.as_view(), name='post-list-filter'),

]
