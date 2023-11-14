# -*- coding: utf-8 -*-
"""Memberpress Client API v1 views."""
# python stuff
import os
import io
import unittest
import json
from datetime import datetime


# our testing code starts here
# -----------------------------------------------------------------------------
from memberpress_client.member import Member  # noqa: E402
from memberpress_client.transaction import Transaction  # noqa: E402,F401
from memberpress_client.subscription import Subscription  # noqa: E402,F401
from memberpress_client.membership import Membership  # noqa: E402,F401

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
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def test_none_member_1(self):
        member = Member(request=None, response=None)  # noqa: F841

    def test_none_member_2(self):
        member = Member(request=None, response=None)
        # class properties
        self.assertEqual(member.request, None)
        self.assertEqual(member.ready, False)
        self.assertEqual(member.member, {})
        self.assertEqual(member.id, None)
        self.assertEqual(member.email, None)
        self.assertEqual(member.username, None)
        self.assertEqual(member.nicename, None)
        self.assertEqual(member.url, None)
        self.assertEqual(member.message, None)
        self.assertEqual(member.registered_at, None)
        self.assertEqual(member.first_name, None)
        self.assertEqual(member.last_name, None)
        self.assertEqual(member.display_name, None)
        self.assertEqual(member.active_txn_count, None)
        self.assertEqual(member.expired_txn_count, None)
        self.assertEqual(member.trial_txn_count, None)
        self.assertEqual(member.login_count, None)

        # dict structural integrity
        self.assertEqual(member.is_complete_dict, False)
        self.assertEqual(member.is_minimum_member_dict, False)
        self.assertEqual(member.is_valid, False)
        self.assertEqual(member.active_memberships, None)
        self.assertEqual(member.recent_subscriptions, None)
        self.assertEqual(member.recent_transactions, None)
        self.assertEqual(member.first_transaction, None)
        self.assertEqual(member.latest_transaction, None)
        self.assertEqual(member.address, {})
        self.assertEqual(member.profile, {})

        # advanced class properties - business rule support
        self.assertEqual(member.is_active_subscription, False)
        self.assertEqual(member.is_trial_subscription, False)

    def test_offline_1(self):
        member = Member(request=None, response=valid_member_response)
        registered_at = datetime.strptime("2022-10-07 22:21:58", "%Y-%m-%d %H:%M:%S")

        # class properties
        self.assertEqual(member.request, None)
        self.assertEqual(member.ready, True)
        self.assertEqual(type(member.member), dict)
        self.assertEqual(member.id, 8)
        self.assertEqual(member.email, "jon.spurling@crstrategypartners.com")
        self.assertEqual(member.username, "JonSpurling81")
        self.assertEqual(member.nicename, "jonspurling81")
        self.assertEqual(member.url, None)
        self.assertEqual(member.message, "")
        self.assertEqual(member.registered_at, registered_at)
        self.assertEqual(member.first_name, "Jon")
        self.assertEqual(member.last_name, "Spurling")
        self.assertEqual(member.display_name, "Jon Spurling")
        self.assertEqual(member.active_txn_count, 1)
        self.assertEqual(member.expired_txn_count, 0)
        self.assertEqual(member.trial_txn_count, 1)
        self.assertEqual(member.login_count, 1)

        # dict structural integrity
        self.assertEqual(member.is_complete_dict, True)
        self.assertEqual(member.is_minimum_member_dict, True)
        self.assertEqual(member.is_valid, True)

        self.assertEqual(type(member.active_memberships), list)
        self.assertEqual(type(member.recent_subscriptions), list)
        self.assertEqual(type(member.recent_transactions), list)
        self.assertEqual(type(member.first_transaction), Transaction)
        self.assertEqual(type(member.latest_transaction), Transaction)

        self.assertEqual(len(member.active_memberships), 1)
        self.assertEqual(len(member.recent_subscriptions), 1)
        self.assertEqual(len(member.recent_transactions), 1)

        # advanced class properties - business rule support
        self.assertEqual(member.is_active_subscription, True)
        self.assertEqual(member.is_trial_subscription, False)

    def test_offline_2(self):
        member = Member(request=None, response=invalid_member_missing_subscriptions)
        self.assertEqual(member.is_active_subscription, False)
        self.assertEqual(member.is_trial_subscription, False)

    def test_offline_3(self):
        member = Member(request=None, response=invalid_member_no_trx)

        self.assertEqual(member.is_complete_dict, False)
        self.assertEqual(member.is_minimum_member_dict, False)
        self.assertEqual(member.is_active_subscription, False)
        self.assertEqual(member.is_trial_subscription, False)

    def test_offline_4_first_transaction(self):
        member = Member(request=None, response=valid_member_response)
        trx = member.first_transaction

        self.assertEqual(trx.is_complete_dict, True)
        self.assertEqual(type(trx.json), dict)
        self.assertEqual(trx.membership, 2420)
        self.assertEqual(trx.member, 8)
        self.assertEqual(trx.coupon, 0)
        self.assertEqual(trx.subscription, 1)
        self.assertEqual(trx.id, 1)
        self.assertEqual(trx.amount, 0.00)
        self.assertEqual(trx.total, 0.00)
        self.assertEqual(trx.tax_amount, 0.00)
        self.assertEqual(trx.tax_rate, 0.000)
        self.assertEqual(trx.tax_desc, "")
        self.assertEqual(trx.tax_class, "standard")
        self.assertEqual(trx.trans_num, "sub_1LqOxIJ1UGflvSOWjTJpb6Sk")
        self.assertEqual(trx.status, "confirmed")
        self.assertEqual(trx.txn_type, "subscription_confirmation")
        self.assertEqual(trx.gateway, "rj1l52-6bw")
        self.assertEqual(trx.prorated, 0)
        self.assertEqual(trx.created_at, datetime.strptime("2022-10-07 22:21:58", "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(trx.expires_at, datetime.strptime("2022-10-14 23:59:59", "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(trx.corporate_account_id, 0)
        self.assertEqual(trx.parent_transaction_id, 0)
        self.assertEqual(trx.tax_compound, 0)
        self.assertEqual(trx.tax_shipping, 1)
        self.assertEqual(trx.response, None)
        self.assertEqual(trx.status, "confirmed")
        self.assertEqual(trx.member, 8)
        self.assertEqual(trx.prorated, 0)
        self.assertEqual(trx.gateway, "rj1l52-6bw")
        self.assertEqual(trx.parent_transaction_id, 0)

    def test_offline_5_recent_subscription(self):
        scr = Subscription(subscription=valid_member_response["recent_subscriptions"][0])
        self.assertEqual(scr.coupon, 0)
        self.assertEqual(scr.membership, 2420)
        self.assertEqual(scr.member, 8)
        self.assertEqual(scr.id, 1)
        self.assertEqual(scr.subscriber_id, "sub_1LqOxIJ1UGflvSOWjTJpb6Sk")
        self.assertEqual(scr.gateway, "rj1l52-6bw")
        self.assertEqual(scr.price, 9.00)
        self.assertEqual(scr.period, 1)
        self.assertEqual(scr.period_type, "months")
        self.assertEqual(scr.limit_cycles, 0)
        self.assertEqual(scr.limit_cycles_num, 2)
        self.assertEqual(scr.limit_cycles_action, "expire")
        self.assertEqual(scr.limit_cycles_expires_after, 1)
        self.assertEqual(scr.limit_cycles_expires_type, "days")
        self.assertEqual(scr.prorated_trial, 0)
        self.assertEqual(scr.trial, 1)
        self.assertEqual(scr.trial_days, 7)
        self.assertEqual(scr.trial_amount, None)
        self.assertEqual(scr.trial_tax_amount, 0.00)
        self.assertEqual(scr.trial_total, 0.00)
        self.assertEqual(scr.status, "active")
        self.assertEqual(scr.created_at, datetime.strptime("2022-10-07 22:23:48", "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(scr.total, 9.00)
        self.assertEqual(scr.tax_rate, 0.000)
        self.assertEqual(scr.tax_amount, 0.00)
        self.assertEqual(scr.tax_desc, "")
        self.assertEqual(scr.tax_class, "standard")
        self.assertEqual(scr.cc_last4, 5673)
        self.assertEqual(scr.cc_exp_month, 12)
        self.assertEqual(scr.cc_exp_year, 2026)
        self.assertEqual(scr.token, "")
        self.assertEqual(scr.tax_compound, 0)
        self.assertEqual(scr.tax_shipping, 1)
        self.assertEqual(scr.response, None)

    def test_offline_6_membership(self):
        mbr = Membership(membership=valid_member_response["active_memberships"][0])
        self.assertEqual(mbr.id, 2420)
        self.assertEqual(mbr.title, "Student")
        self.assertEqual(mbr.excerpt, "")
        self.assertEqual(mbr.date, datetime.strptime("2022-10-04 03:37:31", "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(mbr.status, "publish")
        self.assertEqual(mbr.author, 4)
        self.assertEqual(mbr.date_gmt, datetime.strptime("2022-10-04 03:37:31", "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(mbr.modified, datetime.strptime("2022-10-12 16:10:02", "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(mbr.modified_gmt, datetime.strptime("2022-10-12 16:10:02", "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(mbr.group, 2438)
        self.assertEqual(mbr.price, 9.00)
        self.assertEqual(mbr.period, 1)
        self.assertEqual(mbr.period_type, "months")
        self.assertEqual(mbr.signup_button_text, "Sign Up")
        self.assertEqual(mbr.limit_cycles, False)
        self.assertEqual(mbr.limit_cycles_num, 2)
        self.assertEqual(mbr.limit_cycles_action, "expire")
        self.assertEqual(mbr.limit_cycles_expires_after, 1)
        self.assertEqual(mbr.limit_cycles_expires_type, "days")
        self.assertEqual(mbr.trial, 1)
        self.assertEqual(mbr.trial_days, 7)
        self.assertEqual(mbr.trial_amount, 0)
        self.assertEqual(mbr.trial_once, 1)
        self.assertEqual(mbr.group_order, 1)
        self.assertEqual(mbr.is_highlighted, 1)
        self.assertEqual(mbr.plan_code, "")
        self.assertEqual(mbr.pricing_title, "Student")
        self.assertEqual(mbr.pricing_show_price, True)
        self.assertEqual(mbr.pricing_display, "auto")
        self.assertEqual(mbr.custom_price, "")
        self.assertEqual(mbr.pricing_heading_txt, "Get the math help you need, every Step of the way.")
        self.assertEqual(mbr.pricing_footer_txt, "")
        self.assertEqual(mbr.pricing_button_txt, "Sign Up")
        self.assertEqual(mbr.pricing_button_position, "footer")
        self.assertEqual(type(mbr.pricing_benefits), list)
        self.assertEqual(mbr.register_price_action, "default")
        self.assertEqual(mbr.register_price, "")
        self.assertEqual(mbr.thank_you_page_enabled, False)
        self.assertEqual(mbr.thank_you_page_type, "message")
        self.assertEqual(mbr.thank_you_message, "")
        self.assertEqual(mbr.thank_you_page_id, 0)
        self.assertEqual(mbr.custom_login_urls_enabled, 1)
        self.assertEqual(mbr.custom_login_urls_default, "")
        self.assertEqual(type(mbr.custom_login_urls), list)
        self.assertEqual(mbr.expire_type, "none")
        self.assertEqual(mbr.expire_after, 1)
        self.assertEqual(mbr.expire_unit, "days")
        self.assertEqual(mbr.expire_fixed, datetime.strptime("2022-10-12", "%Y-%m-%d"))
        self.assertEqual(mbr.tax_exempt, False)
        self.assertEqual(mbr.tax_class, "standard")
        self.assertEqual(mbr.allow_renewal, False)
        self.assertEqual(mbr.access_url, "")
        self.assertEqual(mbr.disable_address_fields, False)
        self.assertEqual(mbr.simultaneous_subscriptions, False)
        self.assertEqual(mbr.use_custom_template, False)
        self.assertEqual(mbr.custom_template, "100-width.php")
        self.assertEqual(mbr.customize_payment_methods, 1)
        self.assertEqual(type(mbr.custom_payment_methods), list)
        self.assertEqual(mbr.customize_profile_fields, False)
        self.assertEqual(type(mbr.custom_profile_fields), list)
        self.assertEqual(mbr.cannot_purchase_message, "You don't have access to purchase this item.")


if __name__ == "__main__":
    unittest.main()
