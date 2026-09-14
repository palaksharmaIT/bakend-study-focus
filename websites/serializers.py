from rest_framework import serializers

from .models import BlockedWebsite, FocusSession
from django.contrib.auth.models import User


# ==============================
# Blocked Website Serializer
# ==============================

class BlockedWebsiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlockedWebsite

        fields = [
            'id',
            'domain',
            'is_active',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]


# ==============================
# Register Serializer
# ==============================

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password',
        ]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

        return user


# ==============================
# Focus Session Serializer
# ==============================

class FocusSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = FocusSession

        fields = [
            'id',
            'start_time',
            'end_time',
            'duration',
            'completed',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'start_time',
            'end_time',
            'completed',
            'created_at',
        ]