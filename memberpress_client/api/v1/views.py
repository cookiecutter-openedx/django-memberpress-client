# -*- coding: utf-8 -*-
"""Memberpress Client API v1 views."""
import logging

from rest_framework.views import APIView
from django.http import HttpResponse

from memberpress_client.decorators import app_logger
from memberpress_client.events import get_event
from memberpress_client.models import MemberpressEventLog

logger = logging.getLogger(__name__)


class EventView(APIView):
    @app_logger
    def post(self, request):
        data = request.POST
        method = request.REQUEST_METHOD

        method = method
        event = get_event(data=data)
        try:
            username = event.username or request.user.username
        except Exception:  # noqa # noqa
            username = "missing"

        MemberpressEventLog(
            sender=request.REMOTE_HOST,
            username=username,
            event=event.event,
            event_type=event.event_type,
            is_valid=event.is_valid,
            json=event.json,
        ).save()
        return HttpResponse(status=201)
