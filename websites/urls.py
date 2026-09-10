from django.urls import path
from .views import blocked_websites


urlpatterns = [
    path('websites/', blocked_websites, name='blocked-websites'),
]