"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2022

memberpress REST API Client plugin for Django - plugin constants
"""

# django stuff
from django.conf import settings
from django.utils.functional import classproperty


class MemberpressTransactionTypes:
    SUBSCRIPTION_CONFIRMATION = "subscription_confirmation"
    PAYMENT = "payment"


class TypeBase:
    @classmethod
    def all(self):
        """
        generate a list of all class variable values
        """
        return [
            getattr(self, value)
            for value in [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        ]


class MemberpressEventTypes(TypeBase):
    TRANSACTION = "transaction"
    SUBSCRIPTION = "subscription"
    MEMBER = "member"
    MEMBERSHIP = "membership"


class MemberpressEvents(TypeBase):
    AFTER_CC_EXPIRES_REMINDER = "after-cc-expires-reminder"
    AFTER_MEMBER_SIGNUP_REMINDER = "after-member-signup-reminder"
    AFTER_SIGNUP_ABANDONED_REMINDER = "after-signup-abandoned-reminder"
    AFTER_SUB_EXPIRES_REMINDER = "after-sub-expires-reminder"
    BEFORE_CC_EXPIRES_REMINDER = "before-cc-expires-reminder"
    BEFORE_SUB_EXPIRES_REMINDER = "before-sub-expires-reminder"
    BEFORE_SUB_RENEWS_REMINDER = "before-sub-renews-reminder"
    BEFORE_SUB_TRIAL_ENDS = "before-sub-trial-ends"
    LOGIN = "login"
    MEMBER_ACCOUNT_UPDATED = "member-account-updated"
    MEMBER_ADDED = "member-added"
    MEMBER_DELETED = "member-deleted"
    MEMBER_SIGNUP_COMPLETED = "member-signup-completed"
    MPCA_COURSE_COMPLETED = "mpca-course-completed"
    MPCA_COURSE_STARTED = "mpca-course-started"
    MPCA_LESSON_COMPLETED = "mpca-lesson-completed"
    MPCA_LESSON_STARTED = "mpca-lesson-started"
    MPCA_QUIZ_ATTEMPT_COMPLETED = "mpca-quiz-attempt-completed"
    NON_RECURRING_TRANSACTION_COMPLETED = "non-recurring-transaction-completed"
    NON_RECURRING_TRANSACTION_EXPIRED = "non-recurring-transaction-expired"
    OFFLINE_PAYMENT_COMPLETE = "offline-payment-complete"
    OFFLINE_PAYMENT_PENDING = "offline-payment-pending"
    OFFLINE_PAYMENT_REFUNDED = "offline-payment-refunded"
    RECURRING_TRANSACTION_COMPLETED = "recurring-transaction-completed"
    RECURRING_TRANSACTION_EXPIRED = "recurring-transaction-expired"
    RECURRING_TRANSACTION_FAILED = "recurring-transaction-failed"
    RENEWAL_TRANSACTION_COMPLETED = "renewal-transaction-completed"
    SUB_ACCOUNT_ADDED = "sub-account-added"
    SUB_ACCOUNT_REMOVED = "sub-account-removed"
    SUBSCRIPTION_CREATED = "subscription-created"
    SUBSCRIPTION_DOWNGRADED_TO_ONE_TIME = "subscription-downgraded-to-one-time"
    SUBSCRIPTION_DOWNGRADED_TO_RECURRING = "subscription-downgraded-to-recurring"
    SUBSCRIPTION_DOWNGRADED = "subscription-downgraded"
    SUBSCRIPTION_EXPIRED = "subscription-expired"
    SUBSCRIPTION_PAUSED = "subscription-paused"
    SUBSCRIPTION_RESUMED = "subscription-resumed"
    SUBSCRIPTION_STOPPED = "subscription-stopped"
    SUBSCRIPTION_UPGRADED_TO_ONE_TIME = "subscription-upgraded-to-one-time"
    SUBSCRIPTION_UPGRADED_TO_RECURRING = "subscription-upgraded-to-recurring"
    SUBSCRIPTION_UPGRADED = "subscription-upgraded"
    TRANSACTION_COMPLETED = "transaction-completed"
    TRANSACTION_EXPIRED = "transaction-expired"
    TRANSACTION_FAILED = "transaction-failed"
    TRANSACTION_REFUNDED = "transaction-refunded"
    UNIDENTIFIED_EVENT = "unidentified-event"


MEMBERPRESS_EVENT_TYPES = (
    (MemberpressEventTypes.MEMBER, MemberpressEventTypes.MEMBER),
    (MemberpressEventTypes.MEMBERSHIP, MemberpressEventTypes.MEMBERSHIP),
    (MemberpressEventTypes.SUBSCRIPTION, MemberpressEventTypes.SUBSCRIPTION),
    (MemberpressEventTypes.TRANSACTION, MemberpressEventTypes.TRANSACTION),
)

MEMBERPRESS_EVENTS = (
    (MemberpressEvents.AFTER_CC_EXPIRES_REMINDER, MemberpressEvents.AFTER_CC_EXPIRES_REMINDER),
    (MemberpressEvents.AFTER_MEMBER_SIGNUP_REMINDER, MemberpressEvents.AFTER_MEMBER_SIGNUP_REMINDER),
    (MemberpressEvents.AFTER_SIGNUP_ABANDONED_REMINDER, MemberpressEvents.AFTER_SIGNUP_ABANDONED_REMINDER),
    (MemberpressEvents.AFTER_SUB_EXPIRES_REMINDER, MemberpressEvents.AFTER_SUB_EXPIRES_REMINDER),
    (MemberpressEvents.BEFORE_CC_EXPIRES_REMINDER, MemberpressEvents.BEFORE_CC_EXPIRES_REMINDER),
    (MemberpressEvents.BEFORE_SUB_EXPIRES_REMINDER, MemberpressEvents.BEFORE_SUB_EXPIRES_REMINDER),
    (MemberpressEvents.BEFORE_SUB_RENEWS_REMINDER, MemberpressEvents.BEFORE_SUB_RENEWS_REMINDER),
    (MemberpressEvents.BEFORE_SUB_TRIAL_ENDS, MemberpressEvents.BEFORE_SUB_TRIAL_ENDS),
    (MemberpressEvents.LOGIN, MemberpressEvents.LOGIN),
    (MemberpressEvents.MEMBER_ACCOUNT_UPDATED, MemberpressEvents.MEMBER_ACCOUNT_UPDATED),
    (MemberpressEvents.MEMBER_ADDED, MemberpressEvents.MEMBER_ADDED),
    (MemberpressEvents.MEMBER_DELETED, MemberpressEvents.MEMBER_DELETED),
    (MemberpressEvents.MEMBER_SIGNUP_COMPLETED, MemberpressEvents.MEMBER_SIGNUP_COMPLETED),
    (MemberpressEvents.MPCA_COURSE_COMPLETED, MemberpressEvents.MPCA_COURSE_COMPLETED),
    (MemberpressEvents.MPCA_COURSE_STARTED, MemberpressEvents.MPCA_COURSE_STARTED),
    (MemberpressEvents.MPCA_LESSON_COMPLETED, MemberpressEvents.MPCA_LESSON_COMPLETED),
    (MemberpressEvents.MPCA_LESSON_STARTED, MemberpressEvents.MPCA_LESSON_STARTED),
    (MemberpressEvents.MPCA_QUIZ_ATTEMPT_COMPLETED, MemberpressEvents.MPCA_QUIZ_ATTEMPT_COMPLETED),
    (MemberpressEvents.NON_RECURRING_TRANSACTION_COMPLETED, MemberpressEvents.NON_RECURRING_TRANSACTION_COMPLETED),
    (MemberpressEvents.NON_RECURRING_TRANSACTION_EXPIRED, MemberpressEvents.NON_RECURRING_TRANSACTION_EXPIRED),
    (MemberpressEvents.OFFLINE_PAYMENT_COMPLETE, MemberpressEvents.OFFLINE_PAYMENT_COMPLETE),
    (MemberpressEvents.OFFLINE_PAYMENT_PENDING, MemberpressEvents.OFFLINE_PAYMENT_PENDING),
    (MemberpressEvents.OFFLINE_PAYMENT_REFUNDED, MemberpressEvents.OFFLINE_PAYMENT_REFUNDED),
    (MemberpressEvents.RECURRING_TRANSACTION_COMPLETED, MemberpressEvents.RECURRING_TRANSACTION_COMPLETED),
    (MemberpressEvents.RECURRING_TRANSACTION_EXPIRED, MemberpressEvents.RECURRING_TRANSACTION_EXPIRED),
    (MemberpressEvents.RECURRING_TRANSACTION_FAILED, MemberpressEvents.RECURRING_TRANSACTION_FAILED),
    (MemberpressEvents.RENEWAL_TRANSACTION_COMPLETED, MemberpressEvents.RENEWAL_TRANSACTION_COMPLETED),
    (MemberpressEvents.SUB_ACCOUNT_ADDED, MemberpressEvents.SUB_ACCOUNT_ADDED),
    (MemberpressEvents.SUB_ACCOUNT_REMOVED, MemberpressEvents.SUB_ACCOUNT_REMOVED),
    (MemberpressEvents.SUBSCRIPTION_CREATED, MemberpressEvents.SUBSCRIPTION_CREATED),
    (MemberpressEvents.SUBSCRIPTION_DOWNGRADED_TO_ONE_TIME, MemberpressEvents.SUBSCRIPTION_DOWNGRADED_TO_ONE_TIME),
    (MemberpressEvents.SUBSCRIPTION_DOWNGRADED_TO_RECURRING, MemberpressEvents.SUBSCRIPTION_DOWNGRADED_TO_RECURRING),
    (MemberpressEvents.SUBSCRIPTION_DOWNGRADED, MemberpressEvents.SUBSCRIPTION_DOWNGRADED),
    (MemberpressEvents.SUBSCRIPTION_EXPIRED, MemberpressEvents.SUBSCRIPTION_EXPIRED),
    (MemberpressEvents.SUBSCRIPTION_PAUSED, MemberpressEvents.SUBSCRIPTION_PAUSED),
    (MemberpressEvents.SUBSCRIPTION_RESUMED, MemberpressEvents.SUBSCRIPTION_RESUMED),
    (MemberpressEvents.SUBSCRIPTION_STOPPED, MemberpressEvents.SUBSCRIPTION_STOPPED),
    (MemberpressEvents.SUBSCRIPTION_UPGRADED_TO_ONE_TIME, MemberpressEvents.SUBSCRIPTION_UPGRADED_TO_ONE_TIME),
    (MemberpressEvents.SUBSCRIPTION_UPGRADED_TO_RECURRING, MemberpressEvents.SUBSCRIPTION_UPGRADED_TO_RECURRING),
    (MemberpressEvents.SUBSCRIPTION_UPGRADED, MemberpressEvents.SUBSCRIPTION_UPGRADED),
    (MemberpressEvents.TRANSACTION_COMPLETED, MemberpressEvents.TRANSACTION_COMPLETED),
    (MemberpressEvents.TRANSACTION_EXPIRED, MemberpressEvents.TRANSACTION_EXPIRED),
    (MemberpressEvents.TRANSACTION_FAILED, MemberpressEvents.TRANSACTION_FAILED),
    (MemberpressEvents.TRANSACTION_REFUNDED, MemberpressEvents.TRANSACTION_REFUNDED),
    (MemberpressEvents.UNIDENTIFIED_EVENT, MemberpressEvents.UNIDENTIFIED_EVENT),
)


MEMBERPRESS_OPERATION_PREFIX = "memberpress_api_operation_"
OPERATION_GET_MEMBER = MEMBERPRESS_OPERATION_PREFIX + "get_member"


class MemberPressAPI_Operations:
    __slots__ = ()
    GET_MEMBER = OPERATION_GET_MEMBER


class MemberPressAPI_Endpoints:
    """
    written by: mcdaniel
    date:       oct-2022
    Codify the data models of the api endpoints and data dicts
    referenced by MemberPress REST API
    """

    # -------------------------------------------------------------------------
    # api end points originating from https://stepwisemath.ai/wp-json/mp/v1/
    # -------------------------------------------------------------------------

    @classproperty
    def MEMBERPRESS_API_BASE(cls):
        return f"{settings.MEMBERPRESS_API_BASE_URL}wp-json/mp/v1/"

    @classproperty
    def MEMBERPRESS_API_ME_PATH(cls):
        return f"{cls.MEMBERPRESS_API_BASE}me/"

    # -------------------------------------------------------------------------
    # curl "https://set-me-please.com/wp-json/mp/v1/members/123456" -H "MEMBERPRESS-API-KEY: set-me-please", or
    # curl "https://set-me-please.com/wp-json/mp/v1/members?search=mcdaniel" -H "MEMBERPRESS-API-KEY: set-me-please"
    # -------------------------------------------------------------------------
    def MEMBERPRESS_API_MEMBER_PATH(user_id=None, username=None):
        # if both values are provided, user_id is preferred over username
        suffix = None
        if user_id:
            suffix = f"members/{user_id}" 
        elif username:
            suffix = f"members?search={username}"
        if not suffix:
            raise ValueError("A filter criterion is required.")
        return MemberPressAPI_Endpoints.MEMBERPRESS_API_BASE + suffix


COMPLETE_MEMBER_DICT = [
    "id",
    "email",
    "username",
    "nicename",
    "url",
    "message",
    "registered_at",
    "first_name",
    "last_name",
    "display_name",
    "active_memberships",
    "active_txn_count",
    "expired_txn_count",
    "trial_txn_count",
    "sub_count",
    "login_count",
    "first_txn",
    "latest_txn",
    "address",
    "profile",
    "recent_transactions",
    "recent_subscriptions",
]
MINIMUM_MEMBER_DICT = ["username", "recent_transactions", "recent_subscriptions", "active_memberships"]

PARTIAL_MEMBER_DICT = [
    "id",
    "email",
    "username",
    "nicename",
    "url",
    "message",
    "registered_at",
    "first_name",
    "last_name",
    "display_name",
    "active_memberships",
    "active_txn_count",
    "expired_txn_count",
    "trial_txn_count",
    "sub_count",
    "login_count",
    "address",
    "profile",
    "recent_transactions",
    "recent_subscriptions",
]


COMPLETE_SUBSCRIPTION_DICT = [
    "coupon",
    "membership",
    "member",
    "id",
    "subscr_id",
    "gateway",
    "price",
    "period",
    "period_type",
    "limit_cycles",
    "limit_cycles_num",
    "limit_cycles_action",
    "limit_cycles_expires_after",
    "limit_cycles_expires_type",
    "prorated_trial",
    "trial",
    "trial_days",
    "trial_amount",
    "trial_tax_amount",
    "trial_total",
    "status",
    "created_at",
    "total",
    "tax_rate",
    "tax_amount",
    "tax_desc",
    "tax_class",
    "cc_last4",
    "cc_exp_month",
    "cc_exp_year",
    "token",
    "tax_compound",
    "tax_shipping",
    "response",
]

COMPLETE_TRANSACTION_DICT = [
    "membership",
    "member",
    "coupon",
    "subscription",
    "id",
    "amount",
    "total",
    "tax_amount",
    "tax_rate",
    "tax_desc",
    "tax_class",
    "trans_num",
    "status",
    "txn_type",
    "gateway",
    "prorated",
    "created_at",
    "expires_at",
    "corporate_account_id",
    "parent_transaction_id",
    "tax_compound",
    "tax_shipping",
    "response",
]

COMPLETE_EVENT_DICT = [
    "coupon",
    "id",
    "subscr_id",
    "gateway",
    "price",
    "period",
    "period_type",
    "limit_cycles",
    "limit_cycles_num",
    "limit_cycles_action",
    "limit_cycles_expires_after",
    "limit_cycles_expires_type",
    "prorated_trial",
    "trial",
    "trial_days",
    "trial_amount",
    "trial_tax_amount",
    "trial_total",
    "status",
    "created_at",
    "total",
    "tax_rate",
    "tax_amount",
    "tax_desc",
    "tax_class",
    "cc_last4",
    "cc_exp_month",
    "cc_exp_year",
    "token",
    "tax_compound",
    "tax_shipping",
    "response",
]

COMPLETE_MEMBERSHIP_DICT = [
    "id",
    "title",
    "content",
    "excerpt",
    "date",
    "status",
    "author",
    "date_gmt",
    "modified",
    "modified_gmt",
    "group",
    "price",
    "period",
    "period_type",
    "signup_button_text",
    "limit_cycles",
    "limit_cycles_num",
    "limit_cycles_action",
    "limit_cycles_expires_after",
    "limit_cycles_expires_type",
    "trial",
    "trial_days",
    "trial_amount",
    "trial_once",
    "group_order",
    "is_highlighted",
    "plan_code",
    "pricing_title",
    "pricing_show_price",
    "pricing_display",
    "custom_price",
    "pricing_heading_txt",
    "pricing_footer_txt",
    "pricing_button_txt",
    "pricing_button_position",
    "pricing_benefits",
    "register_price_action",
    "register_price",
    "thank_you_page_enabled",
    "thank_you_page_type",
    "thank_you_message",
    "thank_you_page_id",
    "custom_login_urls_enabled",
    "custom_login_urls_default",
    "custom_login_urls",
    "expire_type",
    "expire_after",
    "expire_unit",
    "expire_fixed",
    "tax_exempt",
    "tax_class",
    "allow_renewal",
    "access_url",
    "disable_address_fields",
    "simultaneous_subscriptions",
    "use_custom_template",
    "custom_template",
    "customize_payment_methods",
    "custom_payment_methods",
    "customize_profile_fields",
    "custom_profile_fields",
    "cannot_purchase_message",
]

COMPLETE_FINANCIAL_SUBSCRIPTION_EVENT = [
    "coupon",
    "id",
    "amount",
    "total",
    "tax_amount",
    "tax_rate",
    "tax_desc",
    "tax_class",
    "trans_num",
    "status",
    "txn_type",
    "gateway",
    "prorated",
    "created_at",
    "expires_at",
    "corporate_account_id",
    "parent_transaction_id",
    "tax_compound",
    "tax_shipping",
    "response",
    "rebill",
    "subscription_payment_index",
]

COMPLETE_NONFINANCIAL_SUBSCRIPTION_EVENT = [
    "coupon",
    "id",
    "subscr_id",
    "gateway",
    "price",
    "period",
    "period_type",
    "limit_cycles",
    "limit_cycles_num",
    "limit_cycles_action",
    "limit_cycles_expires_after",
    "limit_cycles_expires_type",
    "prorated_trial",
    "trial",
    "trial_days",
    "trial_amount",
    "trial_tax_amount",
    "trial_total",
    "status",
    "created_at",
    "total",
    "tax_rate",
    "tax_amount",
    "tax_desc",
    "tax_class",
    "cc_last4",
    "cc_exp_month",
    "cc_exp_year",
    "token",
    "tax_compound",
    "tax_shipping",
    "response",
]
