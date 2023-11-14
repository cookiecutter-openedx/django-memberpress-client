# -*- coding: utf-8 -*-
"""
Memberpress REST API Client plugin for Django - events classes. A collection of
strongly-typed, higher-order classes, all descended from MemberpressEvent, that
consist of varying combinations of Member, Membership, Transaction,
and Subscription objects.

This is part of the webhooks implementation. memberpress webhooks
post events to the "/mp/events" URL endpoint. the body of the request object
from memberpress contains a dict who's structure should match one of the
four dozen child classes of MemberpressEvent found in this module.

Usage:
from memberpress_client.events import get_event

memberpress_event = get_event(dict["event"])

Notes:
- **DO NOT** import MemberpressEvent nor its child classes.  Instead, use
  get_event(). This is intended to help avoid having to import dozens of child
  class into your module, not only for the sake of sanity but also better
  memory management.
"""
from datetime import datetime
import logging
from typing import TypeVar, Generic, Type

from memberpress_client.constants import (
    COMPLETE_TRANSACTION_DICT,
    COMPLETE_EVENT_DICT,
    PARTIAL_MEMBER_DICT,
    COMPLETE_FINANCIAL_SUBSCRIPTION_EVENT,
    COMPLETE_NONFINANCIAL_SUBSCRIPTION_EVENT,
    MemberpressEvents,
    MemberpressEventTypes,
)
from memberpress_client.memberpress import Memberpress
from memberpress_client.member import Member
from memberpress_client.membership import Membership
from memberpress_client.transaction import Transaction
from memberpress_client.subscription import Subscription


logger = logging.getLogger(__name__)


MemberpressEventChild = TypeVar("MemberpressEventChild", bound="MemberpressEvent")


class MemberpressEvent(Generic[MemberpressEventChild], Memberpress):
    """Event base class."""

    _event = None  # a string. example: "after-cc-expires-reminder"
    _event_type = None  # a string. example: "subscription"
    _member = None  # a member object
    _membership = None  # a membership object
    _transaction = None  # a transaction object
    _subscription = None  # a subscription object
    _is_valid = False  # set in validate()

    def __init__(self, data: dict) -> None:
        self.init()
        self.json = data

    @classmethod
    def factory(cls: Type[MemberpressEventChild], data: dict) -> MemberpressEventChild:
        return cls(data=data)

    def init(self):
        super().init()
        self._event = None
        self._event_type = None
        self._member = None
        self._membership = None
        self._transaction = None
        self._subscription = None
        self._is_valid = False

    def validate(self):
        """
        - parent class validations
        - integrity checks inside the event dict
        - structural integrity of the event dict
        """
        super().validate()
        if not self.is_valid:
            return

        if self.event != self.json.get("event", "missing event"):
            self._is_valid = False
            logger.warning("received a dict with inconsistent or missing 'event' key.")
            return

        if self.event_type != self.json.get("type", "missing event type"):
            self._is_valid = False
            logger.warning("received a dict with inconsistent or missing 'type' key.")
            return

        # this is the outer dict structure that all events share
        if not self.valid_base_keys:
            self._is_valid = False
            logger.warning("received a dict with no 'data' key.")
            return

        if not self.valid_event_keys:
            self._is_valid = False
            return

        self._is_valid = True

    @property
    def valid_base_keys(self):
        # all events have these three keys
        base_keys = ["event", "type", "data"]
        return self.is_valid_dict(self.json, qc_keys=base_keys)

    @property
    def valid_event_keys(self):
        # self.qc_keys is set in __init__() in the child classes
        # and contains the event-specific objects contained in
        # json["data"]
        if not self.qc_keys:
            return False
        return self.is_valid_dict(self.data, qc_keys=self.qc_keys)

    @property
    def has_member(self) -> bool:
        return MemberpressEventTypes.MEMBER in self.qc_keys

    @property
    def has_membership(self) -> bool:
        return MemberpressEventTypes.MEMBERSHIP in self.qc_keys

    @property
    def has_transaction(self) -> bool:
        return MemberpressEventTypes.TRANSACTION in self.qc_keys

    @property
    def has_subscription(self) -> bool:
        return MemberpressEventTypes.SUBSCRIPTION in self.qc_keys

    @property
    def event(self) -> str:
        return self._event

    @event.setter
    def event(self, value):
        if value is None:
            self._event = value
            return

        if type(value) is str:
            if value in MemberpressEvents.all():
                self._event = value
            else:
                logger.warning("event() received an unknown event type {value}".format(value=value))
        else:
            logger.warning("was expecting a value of type str but received type {t}".format(t=type(value)))

    @property
    def event_type(self) -> str:
        return self._event_type

    @event_type.setter
    def event_type(self, value):
        if value is None:
            self._event_type = value
            return

        if type(value) is str:
            if value in MemberpressEventTypes.all():
                self._event_type = value
            else:
                logger.warning("event_type() received an unknown event type {value}".format(value=value))
        else:
            logger.warning("was expecting a value of type str but received type {t}".format(t=type(value)))

    @property
    def membership(self) -> Membership:
        if self.has_membership and not self._membership:
            membership_dict = self.data.get(MemberpressEventTypes.MEMBERSHIP, {})
            self._membership = Membership(membership=membership_dict)
        return self._membership

    @property
    def member(self) -> Member:
        if self.has_member and not self._member:
            # note that the member dict resides in either of two locations
            # depending on the kind of event we received.
            member_dict = (
                self.data
                if self.event_type == MemberpressEventTypes.MEMBER
                else self.data.get(MemberpressEventTypes.MEMBER, {})
            )
            self._member = Member(response=member_dict)
        return self._member

    @property
    def transaction(self) -> Transaction:
        if self.has_transaction and not self._transaction:
            # note that the transaction object resides inside the body of the
            # of the data dict.
            transaction_dict = self.data
            self._transaction = Transaction(transaction=transaction_dict)
        return self._transaction

    @property
    def subscription(self) -> Subscription:
        if self.has_subscription and not self._subscription:
            subscription_dict = self.data.get(MemberpressEventTypes.SUBSCRIPTION, {})
            self._subscription = Subscription(subscription=subscription_dict)
        return self._subscription

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

    # -------------------------------------------------------------------------
    # Event attributes
    # -------------------------------------------------------------------------

    @property
    def active_txn_count(self) -> int:
        return self.str2int(self.data.get("active_txn_count"))

    @property
    def address(self) -> dict:
        return self.data.get("address", {})

    @property
    def amount(self) -> float:
        return self.str2float(self.data.get("amount", 0.00))

    @property
    def cc_exp_month(self) -> int:
        return self.str2int(self.data.get("cc_exp_month"))

    @property
    def cc_exp_year(self) -> int:
        return self.str2int(self.data.get("cc_exp_year"))

    @property
    def cc_last4(self) -> int:
        return self.str2int(self.data.get("cc_last4"))

    @property
    def corporate_account_id(self) -> int:
        return self.str2int(self.data.get("corporate_account_id"))

    @property
    def coupon(self) -> int:
        return self.str2int(self.data.get("coupon"))

    @property
    def created_at(self) -> datetime:
        return self.str2datetime(self.data.get("created_at"))

    @property
    def display_name(self) -> str:
        return self.data.get("display_name", "")

    @property
    def email(self) -> str:
        return self.str2email(self.data.get("email"))

    @property
    def expired_txn_count(self) -> int:
        return self.str2int(self.data.get("expired_txn_count"))

    @property
    def expires_at(self) -> datetime:
        return self.str2datetime(self.data.get("expires_at"))

    @property
    def first_name(self) -> str:
        return self.data.get("first_name")

    @property
    def gateway(self) -> str:
        return self.data.get("gateway")

    @property
    def id(self) -> int:
        return self.str2int(self.data.get("id"))

    @property
    def last_name(self) -> str:
        return self.data.get("last_name")

    @property
    def limit_cycles(self) -> bool:
        return self.str2bool(self.data.get("limit_cycles", "false"))

    @property
    def limit_cycles_action(self) -> str:
        return self.data.get("limit_cycles_action")

    @property
    def limit_cycles_expires_after(self) -> int:
        return self.str2int(self.data.get("limit_cycles_expires_after"))

    @property
    def limit_cycles_expires_type(self) -> str:
        return self.data.get("limit_cycles_expires_type")

    @property
    def limit_cycles_num(self) -> int:
        return self.str2int(self.data.get("limit_cycles_num"))

    @property
    def login_count(self) -> int:
        return self.str2int(self.data.get("login_count"))

    @property
    def message(self) -> str:
        return self.data.get("message")

    @property
    def nicename(self) -> str:
        return self.data.get("nicename")

    @property
    def parent_transaction_id(self) -> int:
        return self.str2int(self.data.get("parent_transaction_id"))

    @property
    def period(self) -> int:
        return self.str2int(self.data.get("period"))

    @property
    def period_type(self) -> str:
        return self.data.get("period_type")

    @property
    def price(self) -> float:
        return self.str2float(self.data.get("price"))

    @property
    def profile(self) -> dict:
        return self.data.get("profile", {})

    @property
    def prorated(self) -> int:
        return self.str2int(self.data.get("prorated"))

    @property
    def prorated_trial(self) -> int:
        return self.str2int(self.data.get("prorated_trial"))

    @property
    def rebill(self) -> bool:
        return self.str2bool(self.json.get("rebill"))

    @property
    def registered_at(self) -> datetime:
        return self.str2datetime(self.data.get("registered_at")) if self.username else None

    @property
    def response(self):
        return self.data.get("response")

    @property
    def status(self) -> str:
        return self.data.get("status")

    @property
    def sub_count(self) -> int:
        return self.str2int(self.data.get("sub_count"))

    @property
    def subscr_id(self) -> str:
        return self.data.get("subscr_id")

    @property
    def subscription_payment_index(self) -> bool:
        return self.str2bool(self.json.get("subscription_payment_index"))

    @property
    def tax_amount(self) -> float:
        return self.str2float(self.data.get("tax_amount"))

    @property
    def tax_class(self) -> str:
        return self.data.get("tax_class")

    @property
    def tax_compound(self) -> int:
        return self.str2int(self.data.get("tax_compound"))

    @property
    def tax_desc(self) -> str:
        return self.data.get("tax_desc")

    @property
    def tax_rate(self) -> float:
        return self.str2float(self.data.get("tax_rate"))

    @property
    def tax_shipping(self) -> int:
        return self.str2int(self.data.get("tax_shipping"))

    @property
    def token(self) -> str:
        return self.data.get("token")

    @property
    def total(self) -> float:
        return self.str2float(self.data.get("total"))

    @property
    def trans_num(self) -> str:
        return self.data.get("trans_num")

    @property
    def trial(self) -> int:
        return self.str2int(self.data.get("trial"))

    @property
    def trial_amount(self) -> float:
        return self.str2float(self.data.get("trial_amount"))

    @property
    def trial_days(self) -> int:
        return self.str2int(self.data.get("trial_days"))

    @property
    def trial_tax_amount(self) -> float:
        return self.str2float(self.data.get("trial_tax_amount"))

    @property
    def trial_total(self) -> float:
        return self.str2float(self.data.get("trial_total"))

    @property
    def trial_txn_count(self) -> int:
        return self.str2int(self.data.get("trial_txn_count"))

    @property
    def txn_type(self) -> str:
        return self.data.get("txn_type")

    @property
    def url(self) -> str:
        return self.str2url(self.data.get("url"))

    @property
    def username(self) -> str:
        return self.data.get("username")


class MEAfterCCExpiresReminder(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.AFTER_CC_EXPIRES_REMINDER
        self.event_type = MemberpressEventTypes.SUBSCRIPTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
        ] + COMPLETE_EVENT_DICT
        self.validate()


class MEAfterMemberSignupReminder(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.AFTER_MEMBER_SIGNUP_REMINDER
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEAfterSignupAbandonedReminder(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.AFTER_SIGNUP_ABANDONED_REMINDER
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEAfterSubExpiresReminder(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.AFTER_SUB_EXPIRES_REMINDER
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEBeforeCCExpiresReminder(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.BEFORE_CC_EXPIRES_REMINDER
        self.event_type = MemberpressEventTypes.SUBSCRIPTION
        self.qc_keys = [MemberpressEventTypes.MEMBERSHIP, MemberpressEventTypes.MEMBER] + COMPLETE_EVENT_DICT
        self.validate()


class MEBeforeSubExpiresReminder(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.BEFORE_SUB_EXPIRES_REMINDER
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEBeforeSubRenewsReminder(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.BEFORE_SUB_RENEWS_REMINDER
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEBeforeSubTrialEnds(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.BEFORE_SUB_TRIAL_ENDS
        self.event_type = MemberpressEventTypes.SUBSCRIPTION
        self.qc_keys = [MemberpressEventTypes.MEMBERSHIP, MemberpressEventTypes.MEMBER] + COMPLETE_EVENT_DICT
        self.validate()


class MELogin(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.LOGIN
        self.event_type = MemberpressEventTypes.MEMBER
        self.qc_keys = [] + PARTIAL_MEMBER_DICT
        self.validate()


class MEMemberAccountUpdated(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MEMBER_ACCOUNT_UPDATED
        self.event_type = MemberpressEventTypes.MEMBER
        self.qc_keys = [] + PARTIAL_MEMBER_DICT
        self.validate()


class MEMemberAdded(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MEMBER_ADDED
        self.event_type = MemberpressEventTypes.MEMBER
        self.qc_keys = [] + PARTIAL_MEMBER_DICT
        self.validate()


class MEMemberDeleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MEMBER_DELETED
        self.event_type = MemberpressEventTypes.MEMBER
        self.qc_keys = [] + PARTIAL_MEMBER_DICT
        self.validate()


class MEMemberSignupCompleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MEMBER_SIGNUP_COMPLETED
        self.event_type = MemberpressEventTypes.MEMBER
        self.qc_keys = [] + PARTIAL_MEMBER_DICT
        self.validate()


class MEMPCACourseCompleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MPCA_COURSE_COMPLETED
        self.event_type = MemberpressEventTypes.MEMBER
        self.qc_keys = [] + PARTIAL_MEMBER_DICT
        self.validate()


class MEMPCACourseStarted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MPCA_COURSE_STARTED
        self.event_type = MemberpressEventTypes.MEMBER
        self.qc_keys = [] + PARTIAL_MEMBER_DICT
        self.validate()


class MEMPCALessonCompleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MPCA_LESSON_COMPLETED
        self.event_type = MemberpressEventTypes.MEMBER
        self.qc_keys = [] + PARTIAL_MEMBER_DICT
        self.validate()


class MEMPCALessonStarted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MPCA_LESSON_STARTED
        self.event_type = MemberpressEventTypes.MEMBER
        self.qc_keys = [] + PARTIAL_MEMBER_DICT
        self.validate()


class MEMPCALQuizAttemptCompleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.MPCA_QUIZ_ATTEMPT_COMPLETED
        self.event_type = MemberpressEventTypes.MEMBER
        self.qc_keys = [] + PARTIAL_MEMBER_DICT
        self.validate()


class MENonRecurringTransactionCompleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.NON_RECURRING_TRANSACTION_COMPLETED
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MENonRecurringTransactionExpired(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.NON_RECURRING_TRANSACTION_EXPIRED
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEOfflinePaymentComplete(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.OFFLINE_PAYMENT_COMPLETE
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEOfflinePaymentPending(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.OFFLINE_PAYMENT_PENDING
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEOfflinePaymentRefunded(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.OFFLINE_PAYMENT_REFUNDED
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MERecurringTransactionCompleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.RECURRING_TRANSACTION_COMPLETED
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MERecurringTransactionExpired(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.RECURRING_TRANSACTION_EXPIRED
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MERecurringTransactionFailed(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.RECURRING_TRANSACTION_FAILED
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MERenewalTransactionCompleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.RENEWAL_TRANSACTION_COMPLETED
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubAccountAdded(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUB_ACCOUNT_ADDED
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubAccountRemoved(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUB_ACCOUNT_REMOVED
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubscriptionCreated(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_CREATED
        self.event_type = MemberpressEventTypes.SUBSCRIPTION
        self.qc_keys = [MemberpressEventTypes.MEMBERSHIP, MemberpressEventTypes.MEMBER] + COMPLETE_EVENT_DICT
        self.validate()


class MESubscriptionDowngradedToOneTime(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_DOWNGRADED_TO_ONE_TIME
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_FINANCIAL_SUBSCRIPTION_EVENT
        self.validate()


class MESubscriptionDowngradedToRecurring(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_DOWNGRADED_TO_RECURRING
        self.event_type = MemberpressEventTypes.SUBSCRIPTION
        self.qc_keys = [MemberpressEventTypes.MEMBERSHIP, MemberpressEventTypes.MEMBER] + COMPLETE_EVENT_DICT
        self.validate()


class MESubscriptionDowngraded(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_DOWNGRADED
        self.event_type = MemberpressEventTypes.SUBSCRIPTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
        ] + COMPLETE_NONFINANCIAL_SUBSCRIPTION_EVENT
        self.validate()


class MESubscriptionExpired(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_EXPIRED
        self.event_type = MemberpressEventTypes.SUBSCRIPTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
        ] + COMPLETE_NONFINANCIAL_SUBSCRIPTION_EVENT
        self.validate()


class MESubscriptionPaused(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_PAUSED
        self.event_type = MemberpressEventTypes.SUBSCRIPTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
        ] + COMPLETE_NONFINANCIAL_SUBSCRIPTION_EVENT
        self.validate()


class MESubscriptionResumed(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_RESUMED
        self.event_type = MemberpressEventTypes.SUBSCRIPTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
        ] + COMPLETE_NONFINANCIAL_SUBSCRIPTION_EVENT
        self.validate()


class MESubscriptionStopped(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_STOPPED
        self.event_type = MemberpressEventTypes.SUBSCRIPTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
        ] + COMPLETE_NONFINANCIAL_SUBSCRIPTION_EVENT
        self.validate()


class MESubscriptionUpgradedToOneTime(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_UPGRADED_TO_ONE_TIME
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MESubscriptionUpgradedToRecurring(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_UPGRADED_TO_RECURRING
        self.event_type = MemberpressEventTypes.SUBSCRIPTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
        ] + COMPLETE_NONFINANCIAL_SUBSCRIPTION_EVENT
        self.validate()


class MESubscriptionUpgraded(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.SUBSCRIPTION_UPGRADED
        self.event_type = MemberpressEventTypes.SUBSCRIPTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
        ] + COMPLETE_NONFINANCIAL_SUBSCRIPTION_EVENT
        self.validate()


class METransactionCompleted(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.TRANSACTION_COMPLETED
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class METransactionExpired(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.TRANSACTION_EXPIRED
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class METransactionFailed(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.TRANSACTION_FAILED
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class METransactionRefunded(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.TRANSACTION_REFUNDED
        self.event_type = MemberpressEventTypes.TRANSACTION
        self.qc_keys = [
            MemberpressEventTypes.MEMBERSHIP,
            MemberpressEventTypes.MEMBER,
            MemberpressEventTypes.SUBSCRIPTION,
        ] + COMPLETE_TRANSACTION_DICT
        self.validate()


class MEUnidentifiedEvent(MemberpressEvent):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.event = MemberpressEvents.UNIDENTIFIED_EVENT
        self.event_type = ""
        self.qc_keys = []
        self.validate()


MEMBERPRESS_EVENT_CLASSES = {
    MemberpressEvents.AFTER_CC_EXPIRES_REMINDER: MEAfterCCExpiresReminder,
    MemberpressEvents.AFTER_MEMBER_SIGNUP_REMINDER: MEAfterMemberSignupReminder,
    MemberpressEvents.AFTER_SIGNUP_ABANDONED_REMINDER: MEAfterSignupAbandonedReminder,
    MemberpressEvents.AFTER_SUB_EXPIRES_REMINDER: MEAfterSubExpiresReminder,
    MemberpressEvents.BEFORE_CC_EXPIRES_REMINDER: MEBeforeCCExpiresReminder,
    MemberpressEvents.BEFORE_SUB_EXPIRES_REMINDER: MEBeforeSubExpiresReminder,
    MemberpressEvents.BEFORE_SUB_RENEWS_REMINDER: MEBeforeSubRenewsReminder,
    MemberpressEvents.BEFORE_SUB_TRIAL_ENDS: MEBeforeSubTrialEnds,
    MemberpressEvents.LOGIN: MELogin,
    MemberpressEvents.MEMBER_ACCOUNT_UPDATED: MEMemberAccountUpdated,
    MemberpressEvents.MEMBER_ADDED: MEMemberAdded,
    MemberpressEvents.MEMBER_DELETED: MEMemberDeleted,
    MemberpressEvents.MEMBER_SIGNUP_COMPLETED: MEMemberSignupCompleted,
    MemberpressEvents.MPCA_COURSE_COMPLETED: MEMPCACourseCompleted,
    MemberpressEvents.MPCA_COURSE_STARTED: MEMPCACourseStarted,
    MemberpressEvents.MPCA_LESSON_COMPLETED: MEMPCALessonCompleted,
    MemberpressEvents.MPCA_LESSON_STARTED: MEMPCALessonStarted,
    MemberpressEvents.MPCA_QUIZ_ATTEMPT_COMPLETED: MEMPCALQuizAttemptCompleted,
    MemberpressEvents.NON_RECURRING_TRANSACTION_COMPLETED: MENonRecurringTransactionCompleted,
    MemberpressEvents.NON_RECURRING_TRANSACTION_EXPIRED: MENonRecurringTransactionExpired,
    MemberpressEvents.OFFLINE_PAYMENT_COMPLETE: MEOfflinePaymentComplete,
    MemberpressEvents.OFFLINE_PAYMENT_PENDING: MEOfflinePaymentPending,
    MemberpressEvents.OFFLINE_PAYMENT_REFUNDED: MEOfflinePaymentRefunded,
    MemberpressEvents.RECURRING_TRANSACTION_COMPLETED: MERecurringTransactionCompleted,
    MemberpressEvents.RECURRING_TRANSACTION_EXPIRED: MERecurringTransactionExpired,
    MemberpressEvents.RECURRING_TRANSACTION_FAILED: MERecurringTransactionFailed,
    MemberpressEvents.RENEWAL_TRANSACTION_COMPLETED: MERenewalTransactionCompleted,
    MemberpressEvents.SUB_ACCOUNT_ADDED: MESubAccountAdded,
    MemberpressEvents.SUB_ACCOUNT_REMOVED: MESubAccountRemoved,
    MemberpressEvents.SUBSCRIPTION_CREATED: MESubscriptionCreated,
    MemberpressEvents.SUBSCRIPTION_DOWNGRADED_TO_ONE_TIME: MESubscriptionDowngradedToOneTime,
    MemberpressEvents.SUBSCRIPTION_DOWNGRADED_TO_RECURRING: MESubscriptionDowngradedToRecurring,
    MemberpressEvents.SUBSCRIPTION_DOWNGRADED: MESubscriptionDowngraded,
    MemberpressEvents.SUBSCRIPTION_EXPIRED: MESubscriptionExpired,
    MemberpressEvents.SUBSCRIPTION_PAUSED: MESubscriptionPaused,
    MemberpressEvents.SUBSCRIPTION_RESUMED: MESubscriptionResumed,
    MemberpressEvents.SUBSCRIPTION_STOPPED: MESubscriptionStopped,
    MemberpressEvents.SUBSCRIPTION_UPGRADED_TO_ONE_TIME: MESubscriptionUpgradedToOneTime,
    MemberpressEvents.SUBSCRIPTION_UPGRADED_TO_RECURRING: MESubscriptionUpgradedToRecurring,
    MemberpressEvents.SUBSCRIPTION_UPGRADED: MESubscriptionUpgraded,
    MemberpressEvents.TRANSACTION_COMPLETED: METransactionCompleted,
    MemberpressEvents.TRANSACTION_EXPIRED: METransactionExpired,
    MemberpressEvents.TRANSACTION_FAILED: METransactionFailed,
    MemberpressEvents.TRANSACTION_REFUNDED: METransactionRefunded,
    MemberpressEvents.UNIDENTIFIED_EVENT: MEUnidentifiedEvent,
}


def get_event(data: dict) -> MemberpressEventChild:
    """Return a MemberpressEventChild object based on the data provided.

    Args:
        data (dict): A dictionary containing the data for the event.

    Returns:
        MemberpressEventChild: An instance of a MemberpressEventChild subclass.
    """
    event = data.get("event", None) or MemberpressEvents.UNIDENTIFIED_EVENT
    cls = MEMBERPRESS_EVENT_CLASSES[event]
    return cls.factory(data=data)
