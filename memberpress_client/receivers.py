# -*- coding: utf-8 -*-
"""Listen for signals published by edxapp."""

# Python
import logging

# Django
from django.dispatch import receiver

# Open edX
try:
    from openedx.core.djangoapps.signals.signals import COURSE_GRADE_NOW_PASSED
    from lms.djangoapps.certificates.generation_handler import generate_certificate_task

    RUNNING_LOCALLY = False
except ImportError:
    from django.dispatch import Signal

    COURSE_GRADE_NOW_PASSED = Signal()
    RUNNING_LOCALLY = True


# this repo
from memberpress_client.member import Member

log = logging.getLogger(__name__)


@receiver(COURSE_GRADE_NOW_PASSED, dispatch_uid="stepwisemath_passing_learner")
def listen_for_passing_grade(sender, user, course_id, **kwargs):  # pylint: disable=unused-argument
    """Listen for a signal indicating that the user has passed a course run."""
    log.info(
        "Enrolled student {username} has achieved a passing grade in the course {course_id} [{kwargs}]".format(
            username=user.username, course_id=course_id, kwargs=kwargs
        )
    )

    member = Member(username=user.username)
    if RUNNING_LOCALLY:
        return
    if member.is_trial_subscription:
        log.info(
            "Cannot generate certificate because enrolled student {username} is on a trial membership.".format(
                username=user.username
            )
        )
        return
    if not member.is_active_subscription:
        log.info(
            "Cannot generate certificate because subscription for enrolled student {username} is inactive.".format(
                username=user.username
            )
        )
        return

    log.info("Creating certificate generation task for student {username}.".format(username=user.username))
    generate_certificate_task(user=user, course_key=course_id)
