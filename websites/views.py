from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import BlockedWebsite
from .serializers import BlockedWebsiteSerializer


@api_view(['GET'])
def blocked_websites(request):

    websites = BlockedWebsite.objects.filter(is_active=True)

    serializer = BlockedWebsiteSerializer(
        websites,
        many=True
    )

    return Response(serializer.data)