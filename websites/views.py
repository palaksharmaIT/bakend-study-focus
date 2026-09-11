from rest_framework.decorators import (
    api_view,
    permission_classes
)

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import BlockedWebsite

from .serializers import (
    BlockedWebsiteSerializer,
    RegisterSerializer
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