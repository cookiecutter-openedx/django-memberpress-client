# -*- coding: utf-8 -*-
"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2022

memberpress REST API Client plugin for Django - App Configuration
"""
# python stuff
import logging

# django stuff
from django.apps import AppConfig


try:
    # hooks for openedx plugins
    # these imports only work when this plugin is installed
    # in an Open edX build.
    from edx_django_utils.plugins import PluginSettings, PluginURLs
    from openedx.core.djangoapps.plugins.constants import ProjectType, SettingsType
except ImportError:
    # for both development as well as deployment into a
    # non open edx Django platform.
    class PluginSettings:
        CONFIG = "config"
        RELATIVE_PATH = "relative/path/"

    class PluginURLs:
        CONFIG = "config"
        NAMESPACE = "namespace"
        REGEX = ("regex",)
        RELATIVE_PATH = "urls"

    class ProjectType:
        LMS = ""
        CMS = ""

    class SettingsType:
        PRODUCTION = ""
        COMMON = ""


log = logging.getLogger(__name__)


class MemberPressPluginConfig(AppConfig):
    name = "memberpress_client"
    label = "memberpress_client"

    # This is the text that appears in the Django admin console in all caps
    # as the title box encapsulating all Django app models that are registered
    # in admin.py.
    verbose_name = "memberpress REST API Client plugin"

    # See: https://edx.readthedocs.io/projects/edx-django-utils/en/latest/edx_django_utils.plugins.html
    plugin_app = {
        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: name,
                PluginURLs.REGEX: "^mp/",
                PluginURLs.RELATIVE_PATH: "urls",
            }
        },
        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.PRODUCTION: {PluginSettings.RELATIVE_PATH: "settings.production"},
                SettingsType.COMMON: {PluginSettings.RELATIVE_PATH: "settings.common"},
            }
        },
    }

    def ready(self):
        log.info("{label} is ready.".format(label=self.label))
