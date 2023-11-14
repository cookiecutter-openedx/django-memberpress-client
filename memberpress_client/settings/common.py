# -*- coding: utf-8 -*-
"""
Common Pluggable Django App settings.

Handling of environment variables, see: https://django-environ.readthedocs.io/en/latest/
to convert .env to yml see: https://django-environ.readthedocs.io/en/latest/tips.html#docker-style-file-based-variables
"""
from path import Path as path
import environ
import os

env = environ.Env(
    # set casting, default value
    MEMBERPRESS_API_KEY=(str, "set-me-please"),
    MEMBERPRESS_API_BASE_URL=(str, "https://yourdomain.com"),
    MEMBERPRESS_API_KEY_NAME=(str, "MEMBERPRESS-API-KEY"),
    MEMBERPRESS_CACHE_EXPIRATION=(int, 60 * 60 * 24),
    MEMBERPRESS_SENSITIVE_KEYS=(
        list,
        [
            "password",
            "token",
            "client_id",
            "client_secret",
            "Authorization",
            "secret",
        ],
    ),
)

# path to this file.
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_ROOT = path(__file__).abspath().dirname().dirname()  # /blah/blah/blah/.../memberpress_client
REPO_ROOT = APP_ROOT.dirname()  # /blah/blah/blah/.../django-memberpress-client
TEMPLATES_DIR = APP_ROOT / "templates"

environ.Env.read_env(os.path.join(REPO_ROOT, ".env"))


def plugin_settings(settings):
    """Injects local settings into django settings."""
    settings.MEMBERPRESS_API_KEY = env("MEMBERPRESS_API_KEY")
    settings.MEMBERPRESS_API_BASE_URL = env("MEMBERPRESS_API_BASE_URL")
    settings.MEMBERPRESS_API_KEY_NAME = env("MEMBERPRESS_API_KEY_NAME")  # noqa: F841
    settings.MEMBERPRESS_CACHE_EXPIRATION = env("MEMBERPRESS_CACHE_EXPIRATION")  # noqa: F841
    settings.MEMBERPRESS_SENSITIVE_KEYS = env("MEMBERPRESS_SENSITIVE_KEYS")  # noqa: F841

    settings.MAKO_TEMPLATE_DIRS_BASE.extend([TEMPLATES_DIR])
