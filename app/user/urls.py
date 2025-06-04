from django.urls import path

from app.user.views import SuperAdminSetupView

urlpatterns = [
    path('super-admin-setup/', SuperAdminSetupView.as_view(), name='admin-setup'),
]
