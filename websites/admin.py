from django.contrib import admin
from .models import BlockedWebsite, FocusSession


@admin.register(BlockedWebsite)
class BlockedWebsiteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'domain',
        'is_active',
        'created_at',
    )

    list_filter = (
        'user',
        'is_active',
    )

    search_fields = (
        'user__username',
        'domain',
    )


@admin.register(FocusSession)
class FocusSessionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'duration',
        'completed',
        'start_time',
        'end_time',
        'created_at',
    )

    list_filter = (
        'completed',
        'user',
    )

    search_fields = (
        'user__username',
    )