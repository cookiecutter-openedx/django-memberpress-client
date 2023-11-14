# -*- coding: utf-8 -*-
"""
Memberpress REST API Client plugin for Django - decorators.

request_manager() - common logging and error handling for all REST api verbs
app_logger() - better logging for lms.log and cms.log
"""
# python stuff
import json
import functools
import logging
from requests.exceptions import HTTPError

# our stuff
from .utils import MPJSONEncoder, masked_dict

# module initializations
logger = logging.getLogger(__name__)


def request_manager(method):
    """
    Decorate a method to
    - retry on 401 http exceptions. Will attempt to refresh the token in this case, and try again.
    - catch and kill 429 exceptions.
    - catch and kill 415 exceptions.
    """

    def wrapper(*args, **kwargs):
        cls = args[0]  # noqa: F841
        operation = ""

        try:
            return method(*args, **kwargs)
        except HTTPError as e:
            # look for an operation description if it exists
            if "operation" in kwargs.keys():
                operation = " " + kwargs["operation"]

            # treat any exception as unhandled. however, we should add meta
            # data about the request to the stack trace. dump the request
            # headers and body using MPJSONEncoder so that
            # sensitive data is masked.
            request_body = json.dumps(e.response.content, cls=MPJSONEncoder, indent=4) if e.response is not None else ""
            request_headers = (
                json.dumps(masked_dict(dict(e.response.request.headers)), cls=MPJSONEncoder, indent=4)
                if e.response is not None and e.response.request is not None
                else ""
            )
            raise Exception(
                "memberpress_client.decorators.request_manager(){operation} an "
                "unhandled exception '{error_message}', was returned by {method}():"
                " {verb} {url}, headers={headers}, body={body}".format(
                    operation=operation,
                    method=method.__name__,
                    verb=e.response.request.method,
                    url=e.response.request.url,
                    headers=request_headers,
                    body=request_body,
                    error_message=str(e),
                )
            ) from e

    return wrapper


def app_logger(func):
    """
    Log the name of the module, class, and function being called,
    along with the positional and keyword arguments passed to the function.

    Args:
        func: The function to be decorated.

    Returns:
        The decorated function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        name_of_def = func.__name__
        logged_args = args
        kwargs_dict_repr = ""

        # try initializing variables assuming that we were called by a class method
        try:
            cls = args[0].__class__
            name_of_class = cls.__name__ + "()."
            name_of_module = cls.__module__
            # slice off the 'self' positional argument
            logged_args = args[1:]
        except Exception:  # noqa
            # We weren't called by a class method. Fall back to initializing variables for
            # a standard module function.
            name_of_class = ""
            name_of_module = func.__module__

        positional_args = [repr(a) for a in logged_args]

        if len(kwargs.keys()) > 0:
            kwargs_dict_repr = "keyword args: "
            kwargs_dict_repr += json.dumps(masked_dict(kwargs), cls=MPJSONEncoder, indent=4)

        logger.info(
            "app_logger: {name_of_module}.{name_of_class}{name_of_def}() {args} {kwargs}".format(
                name_of_module=name_of_module,
                name_of_class=name_of_class,
                name_of_def=name_of_def,
                args=positional_args if len(positional_args) > 0 else "",
                kwargs=kwargs_dict_repr,
            )
        )
        return func(*args, **kwargs)

    return wrapper
