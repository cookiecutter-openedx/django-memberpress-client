"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2022

memberpress REST API Client plugin for Django - Member class
"""

# Python stuff
import logging
from datetime import datetime
import requests

# our stuff
from memberpress_client.client import MemberpressAPIClient
from memberpress_client.subscription import Subscription
from memberpress_client.transaction import Transaction
from memberpress_client.membership import Membership
from memberpress_client.constants import (
    MemberPressAPI_Endpoints,
    MemberPressAPI_Operations,
    COMPLETE_MEMBER_DICT,
    MINIMUM_MEMBER_DICT,
)

logger = logging.getLogger(__name__)


class Member(MemberpressAPIClient):
    """
    memberpress REST API client
    """

    _request = None
    _username = None

    _recent_subscriptions = None
    _recent_transactions = None
    _first_transaction = None
    _latest_transaction = None
    _active_memberships = None

    def __init__(self, username=None, user=None, request=None, response=None, user_id=None) -> None:
        """
        username <str>: a Wordpress username
        user <obj>: a Django user object
        request <requests> a Django requests.request object
        response <json> the json reponse from memberpress REST API
        user_id <int>: a Wordpress user ID
        """
        super().__init__()
        self.init()
        self.request = request
        self.json = response

        # 5th priority username
        if response:
            try:
                self._username = response["username"]
            except Exception:
                pass

        # 4rd priority username
        if request:
            try:
                self._username = request.user.username
            except Exception:
                pass

        # 3nd priority username
        if user:
            try:
                self._username = user.username
            except Exception:
                pass

        # 2st priority username
        if username:
            self._username = username

        # 1st priority user ID
        if user_id:
            self._user_id = user_id

        self.validate()

        if self.username:
            # invoke the getter
            self.member

    def init(self):
        super().init()
        self._request = None
        self._user_id = None
        self._username = None
        self._is_valid = False
        self._recent_subscriptions = None
        self._recent_transactions = None
        self._first_transaction = None
        self._latest_transaction = None
        self._active_memberships = None

    def validate(self) -> None:
        super().validate()

        def list_diff(list_1: list, list_2: list) -> list:
            diff = list(set(list_2) - set(list_1))
            return ",".join(diff)

        if not self.username:
            self._is_valid = False
            return

        if not self.member:
            logger.error("member property is not set for username {username}".format(username=self.username))
            self._is_valid = False

        if type(self.member) != dict:
            logger.error(
                "was expecting member object of type dict but received an object of type {t}".format(
                    t=type(self.member)
                )
            )
            self._is_valid = False

        if self.is_complete_dict:
            logger.debug("validated member response object for username {username}.".format(username=self.username))
            self._is_valid = True
            return

        if self.is_minimum_member_dict:
            self._is_valid = True
            return

        missing = list_diff(MINIMUM_MEMBER_DICT, self.member.keys())
        logger.warning(
            "member response object for username {username} is missing the following required keys: {missing}".format(
                username=self.username, missing=missing
            )
        )

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, value):
        if type(value) == requests.request or value is None:
            self.init()
            self._request = value
            self.validate()
        else:
            raise TypeError("Was expecting value of type request but received object of type {t}".format(t=type(value)))

    @property
    def member(self) -> dict:
        """
        implements a single-shot attempt at retreiving a member dict from the rest api.
        if all works as hoped then then set the property to the rest api dict result.

        Any errors or validation failures will result in self.member returning
        an empty dict {} for the life of the object instance.
        """
        # note: need to use private _username in order to avoid recursion.
        if (self._user_id or self._username) and not self.json and not self.locked:
            """
            expected result is a dict if `user_id` is provided, or list containing
            one or more dicts if `username` is used to search for the member.
            """
            path = MemberPressAPI_Endpoints.MEMBERPRESS_API_MEMBER_PATH(user_id=self._user_id, username=self._username)
            retval = self.get(path=path, operation=MemberPressAPI_Operations.GET_MEMBER)

            if type(retval) == list and len(retval) == 1:
                retval = retval[0]

            if type(retval) == list and len(retval) > 1:
                for d in retval:
                    if d.get("username") == self.username:
                        retval = d
                        break

            if type(retval) != dict:
                logger.warning("member() was expecting a return type of dict but received {t}.".format(t=type(retval)))
                retval = None

            self.json = retval
        # convert NoneType to a dict so that other class properties
        # can safely use the form, val = self.member.get("blah")
        return self.json or {}

    @property
    def id(self) -> int:
        return self.str2int(self.member.get("id"))

    @property
    def email(self) -> str:
        return self.str2email(self.member.get("email"))

    @property
    def username(self) -> str:
        if self._username:
            return self._username
        return self.member.get("username", None)

    @property
    def nicename(self) -> str:
        return self.member.get("nicename", None)

    @property
    def url(self) -> str:
        return self.str2url(self.member.get("url"))

    @property
    def message(self) -> str:
        return self.member.get("message", None)

    @property
    def registered_at(self) -> datetime:
        return self.str2datetime(self.member.get("registered_at"))

    @property
    def first_name(self) -> str:
        return self.member.get("first_name", None)

    @property
    def last_name(self) -> str:
        return self.member.get("last_name", None)

    @property
    def display_name(self) -> str:
        return self.member.get("display_name", None)

    @property
    def active_txn_count(self) -> int:
        """
        the number of historical financial transactions (ie Stripe, PayPal, etc.)
        that exist for this member.
        """
        return self.str2int(self.member.get("active_txn_count"))

    @property
    def expired_txn_count(self) -> int:
        """
        the number of historical financial transactions (ie Stripe, PayPal, etc.)
        that exist for this member with an expiration date in the past.
        """
        return self.str2int(self.member.get("expired_txn_count"))

    @property
    def trial_txn_count(self) -> int:
        """
        the number of free trials that exist for this member.
        """
        return self.str2int(self.member.get("trial_txn_count"))

    @property
    def login_count(self) -> int:
        """
        the number of times that this member has logged in to the
        Wordpress site hosting the memberpress REST API plugin.
        """
        return self.str2int(self.member.get("login_count"))

    @property
    def recent_subscriptions(self) -> list:
        if not self._recent_subscriptions and self.is_valid:
            recent_subscriptions = self.data.get("recent_subscriptions", [])
            self._recent_subscriptions = self.list_factory(recent_subscriptions, Subscription)
        return self._recent_subscriptions

    @property
    def recent_transactions(self) -> list:
        if not self._recent_transactions and self.is_valid:
            transactions = self.data.get("recent_transactions", [])
            self._recent_transactions = self.list_factory(transactions, Transaction)
        return self._recent_transactions

    @property
    def active_memberships(self) -> list:
        if not self._active_memberships and self.is_valid:
            memberships = self.data.get("active_memberships", [])
            self._active_memberships = self.list_factory(memberships, Membership)
        return self._active_memberships

    """
    ---------------------------------------------------------------------------
                                Computed properties
    ---------------------------------------------------------------------------
    """

    @property
    def is_complete_dict(self) -> bool:
        """
        validate that response is a json dict containing at least
        the keys in qc_keys. These are the dict keys returned by the
        MemberPress REST api "/me" endpoint for a subscribed user.
        """
        qc_keys = COMPLETE_MEMBER_DICT
        return self.is_valid_dict(self.member, qc_keys)

    @property
    def is_minimum_member_dict(self) -> bool:
        """
        validate that response is a json dict containing at least
        the minimum required keys in qc_keys. These are the dict keys
        containing information about the identity of the member and
        the status of the member's subscription.
        """
        qc_keys = MINIMUM_MEMBER_DICT
        return self.is_valid_dict(self.member, qc_keys)

    @property
    def first_transaction(self) -> Transaction:
        transaction_json = self.member.get("first_txn", None)
        if not self._first_transaction and transaction_json and self.is_valid:
            self._first_transaction = Transaction(transaction_json)
        return self._first_transaction

    @property
    def latest_transaction(self) -> Transaction:
        transaction_json = self.member.get("latest_txn", None)
        if not self._latest_transaction and transaction_json and self.is_valid:
            self._latest_transaction = Transaction(transaction_json)
        return self._latest_transaction

    @property
    def address(self) -> dict:
        return self.member.get("address", {}) if self.is_valid else {}

    @property
    def profile(self) -> dict:
        return self.member.get("profile", {}) if self.is_valid else {}

    """
    ---------------------------------------------------------------------------
                                Business Rule Implementations
    ---------------------------------------------------------------------------
    """

    @property
    def is_active_subscription(self) -> bool:
        if not self.is_valid:
            return False

        for subscription in self.recent_subscriptions:
            if subscription.status == "active":
                return True

        return False

    @property
    def is_trial_subscription(self) -> bool:
        if not self.is_valid:
            return False

        now = datetime.now()
        for membership in self.active_memberships:
            expire_date = membership.expire_fixed or now
            if expire_date >= now:
                return True

        return False

    @property
    def should_raise_paywall(self) -> bool:
        if self.is_active_subscription or self.is_trial_subscription:
            return False
        return self.ready
