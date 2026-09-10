from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import BlockedWebsite
from .serializers import (
    BlockedWebsiteSerializer,
    RegisterSerializer
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blocked_websites(request):

    websites = BlockedWebsite.objects.filter(is_active=True)

    serializer = BlockedWebsiteSerializer(
        websites,
        many=True
    )

    return Response(serializer.data)


@api_view(['POST'])
def register_user(request):

    serializer = RegisterSerializer(data=request.data)

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