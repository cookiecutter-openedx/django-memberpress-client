# -*- coding: utf-8 -*-
"""Memberpress Client API v1 views."""
# Python stuff
import logging
from datetime import datetime

# our stuff
from memberpress_client.client import MemberpressAPIClient
from memberpress_client.constants import COMPLETE_SUBSCRIPTION_DICT

logger = logging.getLogger(__name__)


class Subscription(MemberpressAPIClient):
    """Memberpress Subscription API v1 views."""

    def __init__(self, subscription=None) -> None:
        super().__init__()
        self.init()
        if type(subscription) is dict:
            self.json = subscription
        else:
            logger.warning("received an invalid subscription object: {o}".format(o=subscription))

    def init(self):
        super().init()

    @property
    def is_complete_dict(self) -> bool:
        """
        Validate that response is a json dict containing at least the keys in qc_keys.

        These are the dict keys returned by the
        MemberPress REST api "/me" endpoint for a subscribed user.
        """
        qc_keys = COMPLETE_SUBSCRIPTION_DICT
        return self.is_valid_dict(self.json, qc_keys)

    @property
    def coupon(self) -> int:
        return self.str2int(self.json["coupon"])

    @property
    def membership(self) -> int:
        return self.str2int(self.json["membership"])

    @property
    def member(self) -> int:
        return self.str2int(self.json["member"])

    @property
    def id(self) -> int:
        return self.str2int(self.json["id"])

    @property
    def subscriber_id(self) -> str:
        return self.json.get("subscr_id", None)

    @property
    def gateway(self) -> str:
        return self.json.get("gateway", None)

    @property
    def price(self) -> float:
        return self.str2float(self.json["price"])

    @property
    def period(self) -> int:
        return self.str2int(self.json["period"])

    @property
    def period_type(self) -> str:
        return self.json.get("period_type", None)

    @property
    def limit_cycles(self) -> bool:
        return self.str2bool(self.json["limit_cycles"])

    @property
    def limit_cycles_num(self) -> int:
        return self.str2int(self.json["limit_cycles_num"])

    @property
    def limit_cycles_action(self) -> str:
        return self.json.get("limit_cycles_action", None)

    @property
    def limit_cycles_expires_after(self) -> int:
        return self.str2int(self.json["limit_cycles_expires_after"])

    @property
    def limit_cycles_expires_type(self) -> str:
        return self.json.get("limit_cycles_expires_type", None)

    @property
    def prorated_trial(self) -> int:
        return self.str2int(self.json["prorated_trial"])

    @property
    def trial(self) -> int:
        return self.str2int(self.json["trial"])

    @property
    def trial_days(self) -> int:
        return self.str2int(self.json["trial_days"])

    @property
    def trial_amount(self) -> float:
        return self.str2int(self.json["trial_amount"])

    @property
    def trial_tax_amount(self) -> float:
        return self.str2float(self.json["trial_tax_amount"])

    @property
    def trial_total(self) -> float:
        return self.str2float(self.json["trial_total"])

    @property
    def status(self) -> str:
        return self.json.get("status", None)

    @property
    def created_at(self) -> datetime:
        return self.str2datetime(self.json.get("created_at"))

    @property
    def total(self) -> float:
        return self.str2float(self.json["total"])

    @property
    def tax_rate(self) -> float:
        return self.str2float(self.json["tax_rate"])

    @property
    def tax_amount(self) -> float:
        return self.str2float(self.json["tax_amount"])

    @property
    def tax_desc(self) -> str:
        return self.json.get("tax_desc", None)

    @property
    def tax_class(self) -> str:
        return self.json.get("tax_class", None)

    @property
    def cc_last4(self) -> int:
        return self.str2int(self.json["cc_last4"])

    @property
    def cc_exp_month(self) -> int:
        return self.str2int(self.json["cc_exp_month"])

    @property
    def cc_exp_year(self) -> int:
        return self.str2int(self.json["cc_exp_year"])

    @property
    def token(self) -> str:
        return self.json.get("token", None)

    @property
    def tax_compound(self) -> int:
        return self.str2int(self.json["tax_compound"])

    @property
    def tax_shipping(self) -> int:
        return self.str2int(self.json["tax_shipping"])

    @property
    def response(self) -> str:
        return self.json.get("response", None)
