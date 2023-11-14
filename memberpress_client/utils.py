# -*- coding: utf-8 -*-
"""Memberpress REST API Client plugin for Django - utility and helper functions."""

# python stuff
import json
import logging
import pytz
from unittest.mock import MagicMock
from requests import Response

# django stuff
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


# our  stuff

UTC = pytz.UTC
logger = logging.getLogger(__name__)

# to get past tests
try:
    User = get_user_model()
except Exception:  # noqa
    User = None


def masked_dict(obj) -> dict:
    """
    To mask sensitive key / value in log entries. Masks the value of specified key.

    obj: a dict or a string representation of a dict, or None
    """

    def redact(key: str, obj):
        if key in obj:
            obj[key] = "*** -- REDACTED -- ***"
        return obj

    obj = obj or {}
    obj = dict(obj)
    for key in settings.MEMBERPRESS_SENSITIVE_KEYS:
        obj = redact(key, obj)
    return obj


class MPJSONEncoder(json.JSONEncoder):
    """
    A custom encoder class.

    - smooth out bumps mostly related to test data.
    - ensure text returned is utf-8 encoded.
    - velvety smooth error handling, understanding that we mostly use
      this class for generating log data.
    """

    def default(self, obj):
        """Encode obj as JSON."""
        if isinstance(obj, bytes):
            return str(obj, encoding="utf-8")
        if isinstance(obj, MagicMock):
            return ""
        try:
            return json.JSONEncoder.default(self, obj)
        except Exception:  # noqa
            # obj probably is not json serializable.
            return ""


def get_user(username):
    """Retrieve a User object by username.

    Args:
        username (str): The username of the user to retrieve.

    Returns:
        User: The User object with the specified username.

    Raises:
        ObjectDoesNotExist: If no User object with the specified username exists.
    """
    try:
        return User.objects.get(username=username)
    except ObjectDoesNotExist:
        logger.warning("could not find a User object for username {username}".format(username=username))


def log_trace(caller: str, path: str, data: dict) -> None:
    """Add an application log entry for higher level defs that call the edxapp api."""
    logger.info(
        "memberpress_client.client.Client.{caller}() request: path={path}, data={data}".format(
            caller=caller, path=path, data=json.dumps(masked_dict(data), cls=MPJSONEncoder, indent=4)
        )
    )


def log_pretrip(caller: str, url: str, data: dict, operation: str = "") -> None:
    """Add an application log entry immediately prior to calling the edxapp api."""
    logger.info(
        "memberpress_client.client.Client.{caller}() {operation}, request: url={url}, data={data}".format(
            operation=operation,
            caller=caller,
            url=url,
            data=json.dumps(masked_dict(data), cls=MPJSONEncoder, indent=4),
        )
    )


def log_postrip(caller: str, path: str, response: Response, operation: str = "") -> None:
    """Log the api response immediately after calling the edxapp api."""
    status_code = response.status_code if response is not None else 599
    log_message = "memberpress_client.client.Client.{caller}() {operation}, response status_code={response_status_code}, path={path}".format(  # noqa
        operation=operation, caller=caller, path=path, response_status_code=status_code
    )  # noqa
    if 200 <= status_code <= 399:
        logger.info(log_message)
    else:
        try:
            response_content = (
                json.dumps(response.content, cls=MPJSONEncoder, indent=4)
                if response is not None
                else "No response object."
            )
            log_message += ", response_content={response_content}".format(response_content=response_content)
        except TypeError:
            # TypeError: cannot convert dictionary update sequence element #0 to a sequence
            # This happens occasionally. Appears to be a malformed dict in the response body.
            pass

        logger.error(log_message)
