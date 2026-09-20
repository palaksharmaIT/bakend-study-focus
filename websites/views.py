from rest_framework.decorators import (
    api_view,
    permission_classes
)

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import BlockedWebsite,FocusSession
from django.utils import timezone


from .serializers import (
    BlockedWebsiteSerializer,
    RegisterSerializer,
    FocusSessionSerializer
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blocked_websites(request):

    websites = BlockedWebsite.objects.filter(
        Q(user=request.user) | Q(user__isnull=True),
        is_active=True
    )

    serializer = BlockedWebsiteSerializer(
        websites,
        many=True
    )

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_blocked_website(request):

    domain = request.data.get('domain', '').strip().lower()

    if not domain:
        return Response(
            {"error": "Domain is required."},
            status=400
        )

    website, created = BlockedWebsite.objects.get_or_create(
        user=request.user,
        domain=domain,
        defaults={
            "is_active": True
        }
    )

    if not created:

        if website.is_active:
            return Response(
                {"error": "Website is already blocked."},
                status=400
            )

        website.is_active = True
        website.save()

    serializer = BlockedWebsiteSerializer(website)

    return Response(
        serializer.data,
        status=201
    )


# ==============================
# REMOVE BLOCKED WEBSITE
# ==============================
# NEW: the frontend previously only removed websites from local
# chrome.storage, never from the backend, so the domain reappeared
# after the next sync. This endpoint deactivates the website for
# the logged-in user only (filtered by request.user, so a user
# can never remove another user's website).

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_blocked_website(request):

    domain = request.data.get('domain', '').strip().lower()

    if not domain:
        return Response(
            {"error": "Domain is required."},
            status=400
        )

    try:
        website = BlockedWebsite.objects.get(
            user=request.user,
            domain=domain
        )

    except BlockedWebsite.DoesNotExist:
        return Response(
            {"error": "Website not found."},
            status=404
        )

    website.is_active = False
    website.save()

    return Response(
        {
            "message": "Website removed.",
            "domain": domain
        },
        status=200
    )


@api_view(['POST'])
def register_user(request):

    serializer = RegisterSerializer(
        data=request.data
    )

    if serializer.is_valid():

        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully.",
                "username": user.username,
                "email": user.email
            },
            status=201
        )

    return Response(
        serializer.errors,
        status=400
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_focus_session(request):

    duration = request.data.get('duration')

    if not duration:
        return Response(
            {"error": "Duration is required."},
            status=400
        )

    try:
        duration = int(duration)
    except (TypeError, ValueError):
        return Response(
            {"error": "Duration must be an integer."},
            status=400
        )

    if duration <= 0:
        return Response(
            {"error": "Duration must be greater than 0."},
            status=400
        )

    session = FocusSession.objects.create(
        user=request.user,
        start_time=timezone.now(),
        duration=duration,
        completed=False
    )

    serializer = FocusSessionSerializer(session)

    return Response(
        serializer.data,
        status=201
    )


# ==============================
# COMPLETE FOCUS SESSION
# ==============================
# NEW: previously there was no way to tell the backend that a
# session finished — the frontend only flipped a local flag.
# `pk` is scoped to request.user so one user can never mark
# (or even discover) another user's session as complete.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_focus_session(request, pk):

    try:
        session = FocusSession.objects.get(
            pk=pk,
            user=request.user
        )

    except FocusSession.DoesNotExist:
        return Response(
            {"error": "Session not found."},
            status=404
        )

    if session.completed:
        return Response(
            {"error": "Session is already completed."},
            status=400
        )

    session.completed = True
    session.end_time = timezone.now()
    session.save()

    serializer = FocusSessionSerializer(session)

    return Response(
        serializer.data,
        status=200
    )


# ==============================
# FOCUS SESSION HISTORY
# ==============================
# NEW: simple listing endpoint so the extension (or a future
# stats page) can show past sessions. Only ever returns the
# logged-in user's own sessions.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def focus_session_history(request):

    sessions = FocusSession.objects.filter(
        user=request.user
    ).order_by('-created_at')[:50]

    serializer = FocusSessionSerializer(
        sessions,
        many=True
    )

    return Response(serializer.data)