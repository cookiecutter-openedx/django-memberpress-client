# -*- coding: utf-8 -*-
"""memberpress REST API Client plugin for Django - url scaffolding."""
from django.conf import settings
from django.urls import include, path


app_name = "memberpress_client"
urlpatterns = [
    # production, as a Django plugin running in a namespace
    path("api/v1/", include("memberpress_client.api.v1.urls")),
]

if settings.DEBUG:
    # only used for local development.
    from django.contrib import admin

    urlpatterns += [
        path("mp/api/v1/", include("memberpress_client.api.v1.urls")),
        path("admin/", admin.site.urls),
    ]
