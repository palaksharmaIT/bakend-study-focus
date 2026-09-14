from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    blocked_websites,
    add_blocked_website,
    register_user,
    start_focus_session
)

urlpatterns = [
    path(
        'websites/',
        blocked_websites,
        name='blocked-websites'
    ),

    path(
        'websites/add/',
        add_blocked_website,
        name='add-blocked-website'
    ),

    path(
        'auth/register/',
        register_user,
        name='register'
    ),

    path(
        'auth/login/',
        TokenObtainPairView.as_view(),
        name='token-obtain-pair'
    ),

    path(
        'auth/refresh/',
        TokenRefreshView.as_view(),
        name='token-refresh'
    ),
    path(
        'focus/start/',
        start_focus_session,
        name='start-focus-session'
    ),
]