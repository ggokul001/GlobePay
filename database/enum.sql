/*Used in: Users

Purpose: Indicates whether the user's account is active.*/

create type account_status_enum as enum(
    'ACTIVE',
    'INACTIVE',
    'SUSPENDED',
    'BLOCKED'   

);

/*Used in: Users

Purpose: Stores the KYC verification status.*/

create type kyc_status_enum as ENUM (
    'PENDING',
    'UNDER_REVIEW',
    'VERIFIED',
    'REJECTED'
);

/*Used in: UserSessions

Purpose: Represents the current login session state.*/

create type session_status_enum as enum(
    'ACTIVE',
    'EXPIRED',
    'REVOKED'
);

/*Used in: PaymentMethods

Purpose: Defines the payment method used.*/

create type payment_type_enum as enum(
    'CREDIT_CARD',
    'DEBIT_CARD',
    'BANK_ACCOUNT'
);

/*Used in: Transactions

Purpose: Tracks the payment lifecycle.*/

create type Transaction_status_enum as enum(
     'PENDING',
    'PROCESSING',
    'SUCCESS',
    'FAILED',
    'REFUNDED',
    'CANCELLED'
);

/*Used in: Transactions, QRScans

Purpose: Identifies which payment network is used.*/

create type payment_network_enum as enum(
    'UPI',
    'PAYNOW',
    'PROMPTPAY',
    'CARD',
    'BANK_TRANSFER'
);

/*Used in: Transactions, PaymentProviderLogs

Purpose: Identifies the payment gateway.*/

create type payment_provider_enum as enum(
    'STRIPE',
    'ADYEN'
);

/*Used in: Notifications

Purpose: Categorizes notifications.*/

create type notification_type_enum as enum(
    'PAYMENT',
    'SECURITY',
    'SYSTEM',
    'PROMOTION'
);

/*Used in: Notifications

Purpose: Tracks notification delivery.*/

create type notification_delivery_status_enum as enum(
    'PENDING',
    'SENT',
    'DELIVERED',
    'READ',
    'FAILED'

);

/*Used in: AuditLogs

Purpose: Records user actions.*/

create type audit_action_enum as enum(
    'CREATE',
    'UPDATE',
    'DELETE',
    'LOGIN',
    'LOGOUT',
    'PAYMENT'
);

/*Used in: PaymentProviderLogs

Purpose: Stores webhook event types from payment providers.*/

create type provider_event_enum as enum(
    'CHARGE_SUCCEEDED',
    'CHARGE_FAILED',
    'REFUND_COMPLETED',
    'WEBHOOK_RECEIVED'
);
