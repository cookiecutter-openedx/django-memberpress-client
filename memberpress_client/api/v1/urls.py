# -*- coding: utf-8 -*-
"""Memberpress Client API v1 urls."""
from django.urls import path
from memberpress_client.api.v1 import views

app_name = "memberpress_client_api"
urlpatterns = [
    path("events/", views.EventView.as_view(), name="events"),
]
