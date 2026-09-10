from django.contrib import admin
from .models import BlockedWebsite


@admin.register(BlockedWebsite)
class BlockedWebsiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('domain',)