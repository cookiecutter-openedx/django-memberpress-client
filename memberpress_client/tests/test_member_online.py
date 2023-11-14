# -*- coding: utf-8 -*-
"""Memberpress Client API v1 tests."""
# python stuff
import logging
import os
import io
from time import sleep
import unittest
import json
from datetime import datetime

# our testing code starts here
# -----------------------------------------------------------------------------
from memberpress_client.member import Member  # noqa: E402
from memberpress_client.transaction import Transaction  # noqa: E402,F401
from memberpress_client.subscription import Subscription  # noqa: E402,F401
from memberpress_client.membership import Membership  # noqa: E402,F401

logger = logging.getLogger(__name__)

# setup test data
HERE = os.path.abspath(os.path.dirname(__file__))


def load_test_member(test_file):
    """Load test data from a file."""
    with io.open(os.path.join(HERE, "data", "api", test_file), "rt", encoding="utf8") as f:
        return f.read()


# test data
# -----------------------------------------------------------------------------
valid_member_response = json.loads(load_test_member("valid-member.json"), strict=False)
invalid_member_missing_subscriptions = json.loads(
    load_test_member("invalid-member-missing-subscriptions.json"), strict=False
)
invalid_member_no_trx = json.loads(load_test_member("invalid-member-no-trx.json"), strict=False)


class TestMember(unittest.TestCase):
    """Test Member class."""

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def test_online_1(self):
        member = Member(username="jon")

        if not member.ready:
            self.assertEqual(member.should_raise_paywall, False)

        while not member.ready:
            sleep(1)

        registered_at = datetime.strptime("2022-10-13 22:27:16", "%Y-%m-%d %H:%M:%S")

        # class properties
        self.assertEqual(member.request, None)
        self.assertEqual(member.ready, True)
        self.assertEqual(type(member.member), dict)
        self.assertEqual(member.id, 10)
        self.assertEqual(member.email, "jon.spurling@crstrategypartners.com")
        self.assertEqual(member.username, "jon")
        self.assertEqual(member.nicename, "jon")
        self.assertEqual(member.url, None)
        self.assertEqual(member.message, "")
        self.assertEqual(member.registered_at, registered_at)
        self.assertEqual(member.first_name, "Jon")
        self.assertEqual(member.last_name, "Spurling")
        self.assertEqual(member.display_name, "Jon Spurling")
        self.assertEqual(member.active_txn_count, 0)
        self.assertEqual(member.expired_txn_count, 0)
        self.assertEqual(member.trial_txn_count, 0)
        self.assertGreater(member.login_count, 0)

        # dict structural integrity
        self.assertEqual(member.is_complete_dict, False)
        self.assertEqual(member.is_minimum_member_dict, True)
        self.assertEqual(member.is_valid, True)

        self.assertEqual(member.active_memberships, [])
        self.assertEqual(member.recent_subscriptions, [])
        self.assertEqual(member.recent_transactions, [])
        self.assertEqual(member.first_transaction, None)
        self.assertEqual(member.latest_transaction, None)

        if member.active_memberships is not None:
            self.assertEqual(len(member.active_memberships), 0)

        if member.recent_subscriptions is not None:
            self.assertEqual(len(member.recent_subscriptions), 0)

        if member.recent_transactions is not None:
            self.assertEqual(len(member.recent_transactions), 0)

        # advanced class properties - business rule support
        self.assertEqual(member.is_active_subscription, False)
        self.assertEqual(member.is_trial_subscription, False)
        self.assertEqual(member.should_raise_paywall, True)
