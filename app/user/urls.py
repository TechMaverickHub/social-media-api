from django.urls import path

from app.user.views import SuperAdminSetupView, UserLogin, UserLogout

urlpatterns = [
    path('super-admin-setup/', SuperAdminSetupView.as_view(), name='admin-setup'),

    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout'),

]
