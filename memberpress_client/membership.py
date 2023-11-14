# -*- coding: utf-8 -*-
"""Memberpress Client API v1 views."""
# Python stuff
import logging
from datetime import datetime

# our stuff
from memberpress_client.client import MemberpressAPIClient
from memberpress_client.constants import COMPLETE_MEMBERSHIP_DICT

logger = logging.getLogger(__name__)


class Membership(MemberpressAPIClient):
    def __init__(self, membership=None) -> None:
        super().__init__()
        self.init()
        if type(membership) is dict:
            self.json = membership
        else:
            logger.warning("received an invalid membership object: {o}".format(o=membership))

    def init(self):
        super().init()

    @property
    def is_complete_dict(self) -> bool:
        """
        Validate that response is a json dict containing at least the keys in qc_keys.

        These are the dict keys returned by the
        MemberPress REST api "/me" endpoint for a subscribed user.
        """
        qc_keys = COMPLETE_MEMBERSHIP_DICT
        return self.is_valid_dict(self.member, qc_keys)

    @property
    def id(self) -> int:
        try:
            return int(self.json["id"])
        except Exception:  # noqa
            return None

    @property
    def title(self) -> str:
        return self.json.get("title")

    @property
    def content(self) -> str:
        return self.json.get("content")

    @property
    def excerpt(self) -> str:
        return self.json.get("excerpt")

    @property
    def date(self) -> datetime:
        return self.str2datetime(self.json.get("date", ""))

    @property
    def status(self) -> str:
        return self.json.get("status")

    @property
    def author(self) -> int:
        return self.str2int(self.json["author"])

    @property
    def date_gmt(self) -> datetime:
        return self.str2datetime(self.json.get("date_gmt"))

    @property
    def modified(self) -> datetime:
        return self.str2datetime(self.json.get("modified"))

    @property
    def modified_gmt(self) -> datetime:
        return self.str2datetime(self.json.get("modified_gmt", ""))

    @property
    def group(self) -> int:
        return self.str2int(self.json["group"])

    @property
    def price(self) -> float:
        return self.str2float(self.json["price"])

    @property
    def period(self) -> int:
        return self.str2int(self.json["period"])

    @property
    def period_type(self) -> str:
        return self.json.get("period_type")

    @property
    def signup_button_text(self) -> str:
        return self.json.get("signup_button_text")

    @property
    def limit_cycles(self) -> bool:
        return self.str2bool(self.json.get("limit_cycles"))

    @property
    def limit_cycles_num(self) -> int:
        return self.str2int(self.json["limit_cycles_num"])

    @property
    def limit_cycles_action(self) -> str:
        return self.json.get("limit_cycles_action")

    @property
    def limit_cycles_expires_after(self) -> int:
        return self.str2int(self.json["limit_cycles_expires_after"])

    @property
    def limit_cycles_expires_type(self) -> str:
        return self.json.get("limit_cycles_expires_type")

    @property
    def trial(self) -> int:
        return self.str2int(self.json["trial"])

    @property
    def trial_days(self) -> int:
        return self.str2int(self.json["trial_days"])

    @property
    def trial_amount(self) -> int:
        return self.str2int(self.json["trial_amount"])

    @property
    def trial_once(self) -> int:
        return self.str2int(self.json["trial_once"])

    @property
    def group_order(self) -> int:
        return self.str2int(self.json["group_order"])

    @property
    def is_highlighted(self) -> bool:
        retval = self.str2int(self.json["is_highlighted"])
        return True if retval == 1 else False

    @property
    def plan_code(self) -> str:
        return self.json.get("plan_code")

    @property
    def pricing_title(self) -> str:
        return self.json.get("pricing_title")

    @property
    def pricing_show_price(self) -> bool:
        return self.str2bool(self.json.get("pricing_show_price"))

    @property
    def pricing_display(self) -> str:
        return self.json.get("pricing_display")

    @property
    def custom_price(self) -> str:
        return self.json.get("custom_price")

    @property
    def pricing_heading_txt(self) -> str:
        return self.json.get("pricing_heading_txt")

    @property
    def pricing_footer_txt(self) -> str:
        return self.json.get("pricing_footer_txt")

    @property
    def pricing_button_txt(self) -> str:
        return self.json.get("pricing_button_txt")

    @property
    def pricing_button_position(self) -> str:
        return self.json.get("pricing_button_position")

    @property
    def pricing_benefits(self) -> list:
        return self.json.get("pricing_benefits")

    @property
    def register_price_action(self) -> str:
        return self.json.get("register_price_action")

    @property
    def register_price(self) -> str:
        return self.json.get("register_price")

    @property
    def thank_you_page_enabled(self) -> bool:
        return self.str2bool(self.json.get("thank_you_page_enabled"))

    @property
    def thank_you_page_type(self) -> str:
        return self.json.get("thank_you_page_type")

    @property
    def thank_you_message(self) -> str:
        return self.json.get("thank_you_message")

    @property
    def thank_you_page_id(self) -> int:
        return self.str2int(self.json["thank_you_page_id"])

    @property
    def custom_login_urls_enabled(self) -> int:
        return self.str2int(self.json["custom_login_urls_enabled"])

    @property
    def custom_login_urls_default(self) -> str:
        return self.json.get("custom_login_urls_default")

    @property
    def custom_login_urls(self) -> list:
        return self.json.get("custom_login_urls")

    @property
    def expire_type(self) -> str:
        return self.json.get("expire_type")

    @property
    def expire_after(self) -> int:
        return self.str2int(self.json["expire_after"])

    @property
    def expire_unit(self) -> str:
        return self.json.get("expire_unit")

    @property
    def expire_fixed(self) -> datetime:
        return self.str2datetime(self.json.get("expire_fixed"))

    @property
    def tax_exempt(self) -> bool:
        return self.str2bool(self.json.get("tax_exempt"))

    @property
    def tax_class(self) -> str:
        return self.json.get("tax_class")

    @property
    def allow_renewal(self) -> bool:
        return self.str2bool(self.json.get("allow_renewal"))

    @property
    def access_url(self) -> str:
        return self.json.get("access_url")

    @property
    def disable_address_fields(self) -> bool:
        return self.str2bool(self.json.get("disable_address_fields"))

    @property
    def simultaneous_subscriptions(self) -> bool:
        return self.str2bool(self.json.get("simultaneous_subscriptions"))

    @property
    def use_custom_template(self) -> bool:
        return self.str2bool(self.json.get("use_custom_template"))

    @property
    def custom_template(self) -> str:
        return self.json.get("custom_template")

    @property
    def customize_payment_methods(self) -> int:
        return self.str2int(self.json["customize_payment_methods"])

    @property
    def custom_payment_methods(self) -> list:
        return self.json.get("custom_payment_methods")

    @property
    def customize_profile_fields(self) -> bool:
        return self.str2bool(self.json.get("customize_profile_fields"))

    @property
    def custom_profile_fields(self) -> list:
        return self.json.get("custom_profile_fields")

    @property
    def cannot_purchase_message(self) -> str:
        return self.json.get("cannot_purchase_message")
