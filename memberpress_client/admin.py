# -*- coding: utf-8 -*-
"""Memberpress Client admin."""
from django.contrib import admin
from memberpress_client.models import MemberpressEventLog


class MemberpressEventLogAdmin(admin.ModelAdmin):
    """Memberpress Webhook event log."""

    def has_change_permission(self, request, obj=None):
        return False

    search_fields = ()
    list_display = (
        "created",
        "event",
        "event_type",
        "is_valid",
        "is_processed",
        "username",
        "json",
    )


admin.site.register(MemberpressEventLog, MemberpressEventLogAdmin)
