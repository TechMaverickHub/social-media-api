from django.urls import path

from app.user.views import AdminSetupView

urlpatterns = [
    path('admin-setup/', AdminSetupView.as_view(), name='admin-setup'),
]
