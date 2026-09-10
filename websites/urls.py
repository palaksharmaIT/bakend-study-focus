from django.urls import path
from .views import blocked_websites, register_user


urlpatterns = [
    path('websites/', blocked_websites, name='blocked-websites'),
    path('auth/register/', register_user, name='register'),
]