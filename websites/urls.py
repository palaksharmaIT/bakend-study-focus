from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    blocked_websites,
    add_blocked_website,
    remove_blocked_website,
    register_user,
    start_focus_session,
    complete_focus_session,
    focus_session_history,
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

    # NEW: actually removes/deactivates a website on the backend
    # (frontend used to only remove it from local storage)
    path(
        'websites/remove/',
        remove_blocked_website,
        name='remove-blocked-website'
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

    # NEW: marks a session as completed on the backend
    path(
        'focus/<int:pk>/complete/',
        complete_focus_session,
        name='complete-focus-session'
    ),

    # NEW: lists the logged-in user's past focus sessions
    path(
        'focus/history/',
        focus_session_history,
        name='focus-session-history'
    ),
]