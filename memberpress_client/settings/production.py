# -*- coding: utf-8 -*-
"""Common Pluggable Django App settings."""


def plugin_settings(settings):
    """Injects local settings into django settings."""
    settings.MEMBERPRESS_API_KEY = "set-me-please"  # noqa: F841
    settings.MEMBERPRESS_API_BASE_URL = "https://set-me-please.com/"  # noqa: F841
