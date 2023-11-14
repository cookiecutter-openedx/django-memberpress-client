# -*- coding: utf-8 -*-
"""Memberpress Client API v1 views."""
# Python stuff
import logging
from datetime import datetime

# our stuff
from memberpress_client.client import MemberpressAPIClient
from memberpress_client.constants import COMPLETE_TRANSACTION_DICT

logger = logging.getLogger(__name__)


class Transaction(MemberpressAPIClient):
    def __init__(self, transaction=None) -> None:
        super().__init__()
        self.init()
        if type(transaction) is dict:
            self.json = transaction
        else:
            logger.warning("received an invalid transaction object: {o}".format(o=transaction))

    def init(self):
        super().init()

    @property
    def is_complete_dict(self) -> bool:
        """
        Validate that response is a json dict containing at least the keys in qc_keys.

        These are the dict keys returned by the MemberPress REST api "/me" endpoint for a subscribed user.
        """
        qc_keys = COMPLETE_TRANSACTION_DICT
        return self.is_valid_dict(self.json, qc_keys)

    @property
    def membership(self) -> int:
        return self.str2int(self.json["membership"])

    @property
    def member(self) -> int:
        return self.str2int(self.json["member"])

    @property
    def coupon(self) -> int:
        return self.str2int(self.json["coupon"])

    @property
    def subscription(self) -> int:
        return self.str2int(self.json["subscription"])

    @property
    def transaction(self) -> int:
        return self.str2int(self.json["transaction"])

    @property
    def id(self) -> int:
        return self.str2int(self.json["id"])

    @property
    def amount(self) -> float:
        return self.str2float(self.json["amount"])

    @property
    def total(self) -> float:
        return self.str2float(self.json["total"])

    @property
    def tax_amount(self) -> float:
        return self.str2float(self.json["tax_amount"])

    @property
    def tax_rate(self) -> float:
        return self.str2float(self.json["tax_rate"])

    @property
    def tax_desc(self) -> str:
        return self.json.get("tax_desc", None)

    @property
    def tax_class(self) -> str:
        return self.json.get("tax_class", None)

    @property
    def trans_num(self) -> str:
        return self.json.get("trans_num", None)

    @property
    def status(self) -> str:
        return self.json.get("status", None)

    @property
    def txn_type(self) -> str:
        return self.json.get("txn_type", None)

    @property
    def gateway(self) -> str:
        return self.json.get("gateway", None)

    @property
    def prorated(self) -> int:
        return self.str2int(self.json["prorated"])

    @property
    def created_at(self) -> datetime:
        return self.str2datetime(self.json.get("created_at"))

    @property
    def expires_at(self) -> datetime:
        return self.str2datetime(self.json.get("expires_at"))

    @property
    def corporate_account_id(self) -> int:
        return self.str2int(self.json["corporate_account_id"])

    @property
    def parent_transaction_id(self) -> int:
        return self.str2int(self.json["parent_transaction_id"])

    @property
    def tax_compound(self) -> int:
        return self.str2int(self.json["tax_compound"])

    @property
    def tax_shipping(self) -> int:
        return self.str2int(self.json["tax_shipping"])

    @property
    def response(self) -> str:
        return self.json.get("response", None)
