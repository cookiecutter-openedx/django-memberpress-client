# -*- coding: utf-8 -*-
"""Memberpress Client API v1 views."""
# python stuff
import os
import io
import unittest
import json


# our testing code starts here
# -----------------------------------------------------------------------------
from memberpress_client.member import Member  # noqa: E402

# setup test data
HERE = os.path.abspath(os.path.dirname(__file__))


def load_test_member(test_file):
    """Load test data from a file."""
    with io.open(os.path.join(HERE, "data", "api", test_file), "rt", encoding="utf8") as f:
        return f.read()


# test data
# -----------------------------------------------------------------------------
valid_member_nosubscription = json.loads(load_test_member("valid-member-no-subscription.json"), strict=False)


class TestMember(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def test_offline_1(self):
        member = Member(request=None, response=valid_member_nosubscription)
        # registered_at = datetime.strptime("2022-10-07 22:21:58", "%Y-%m-%d %H:%M:%S")

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
        # self.assertAlmostEqual(member.registered_at, registered_at)
        self.assertEqual(member.first_name, "Jon")
        self.assertEqual(member.last_name, "Spurling")
        self.assertEqual(member.display_name, "Jon Spurling")
        self.assertEqual(member.active_txn_count, 0)
        self.assertEqual(member.expired_txn_count, 0)
        self.assertEqual(member.trial_txn_count, 0)
        self.assertEqual(member.login_count, 0)

        # dict structural integrity
        self.assertEqual(member.is_complete_dict, False)
        self.assertEqual(member.is_minimum_member_dict, True)
        self.assertEqual(member.is_valid, True)

        self.assertEqual(type(member.active_memberships), list)
        self.assertEqual(type(member.recent_subscriptions), list)
        self.assertEqual(type(member.recent_transactions), list)
        self.assertEqual(member.first_transaction, None)
        self.assertEqual(member.latest_transaction, None)

        self.assertEqual(len(member.active_memberships), 0)
        self.assertEqual(len(member.recent_subscriptions), 0)
        self.assertEqual(len(member.recent_transactions), 0)

        # advanced class properties - business rule support
        self.assertEqual(member.is_active_subscription, False)
        self.assertEqual(member.is_trial_subscription, False)


if __name__ == "__main__":
    unittest.main()
