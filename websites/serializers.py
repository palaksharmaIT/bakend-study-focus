from rest_framework import serializers
from .models import BlockedWebsite


class BlockedWebsiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlockedWebsite
        fields = ['domain', 'is_active']