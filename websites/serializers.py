from django.contrib.auth.models import User
from rest_framework import serializers

from .models import BlockedWebsite


class BlockedWebsiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlockedWebsite
        fields = ['domain', 'is_active']


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user