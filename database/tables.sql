-- ============================================================
-- USERS TABLE
-- Stores registered GlobePay users.
-- Central parent table for the entire system.
-- ============================================================

create table users(
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    full_name VARCHAR(100) NOT NULL,

    email VARCHAR(255) NOT NULL UNIQUE,

    phone_number VARCHAR(20) NOT NULL,

    country VARCHAR(100) NOT NULL,

    kyc_status kyc_status_enum
        NOT NULL
        DEFAULT 'PENDING',

    account_status account_status_enum
        NOT NULL
        DEFAULT 'ACTIVE',

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    updated_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW()
);

-- ============================================================
-- USER_SESSIONS TABLE
-- Stores login sessions for each user.
-- One User → Many Sessions
-- ============================================================

CREATE TABLE user_sessions (

    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    device_type VARCHAR(50) NOT NULL,

    device_id VARCHAR(255) NOT NULL,

    ip_address INET NOT NULL,

    login_time TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    expiry_time TIMESTAMPTZ NOT NULL,

    status session_status_enum
        NOT NULL
        DEFAULT 'ACTIVE',

    CONSTRAINT fk_user_sessions_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE

);

-- ============================================================
-- PAYMENT_METHODS TABLE
-- Stores user payment methods securely.
-- Raw card details are NEVER stored.
-- ============================================================

CREATE TABLE payment_methods (

    payment_method_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    payment_type payment_type_enum NOT NULL,

    provider_name payment_provider_enum NOT NULL,

    provider_token VARCHAR(255) NOT NULL UNIQUE,

    masked_account VARCHAR(25) NOT NULL,

    status account_status_enum
        NOT NULL
        DEFAULT 'ACTIVE',

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    deleted_at TIMESTAMPTZ,

    CONSTRAINT fk_payment_methods_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE

);

-- ============================================================
-- EXCHANGE_RATES TABLE
-- Stores foreign exchange rates fetched from providers.
-- ============================================================

CREATE TABLE exchange_rates (

    exchange_rate_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    source_currency CHAR(3) NOT NULL,

    target_currency CHAR(3) NOT NULL,

    provider_rate DECIMAL(18,8) NOT NULL,

    spread_percentage DECIMAL(5,4) NOT NULL,

    customer_rate DECIMAL(18,8) NOT NULL,

    provider_name payment_provider_enum NOT NULL,

    fetched_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    CONSTRAINT uq_exchange_rate
        UNIQUE (
            source_currency,
            target_currency,
            fetched_at
        )

);


-- ============================================================
-- TRANSACTIONS TABLE
-- Stores every GlobePay payment transaction.
-- Core business table of the system.
-- ============================================================

CREATE TABLE transactions (

    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    payment_method_id UUID NOT NULL,

    exchange_rate_id UUID NOT NULL,

    merchant_name VARCHAR(150) NOT NULL,

    merchant_id VARCHAR(100) NOT NULL,

    merchant_country VARCHAR(100) NOT NULL,

    merchant_currency CHAR(3) NOT NULL,

    user_currency CHAR(3) NOT NULL,

    payment_network payment_network_enum NOT NULL,

    original_amount DECIMAL(18,2) NOT NULL,

    converted_amount DECIMAL(18,2) NOT NULL,

    transaction_fee DECIMAL(18,2)
        NOT NULL
        DEFAULT 0.00,

    payment_provider payment_provider_enum NOT NULL,

    provider_transaction_id VARCHAR(100)
        NOT NULL
        UNIQUE,

    applied_fx_rate DECIMAL(18,8) NOT NULL,

    idempotency_key UUID
        NOT NULL
        UNIQUE,

    failure_reason VARCHAR(255),

    status transaction_status_enum
        NOT NULL
        DEFAULT 'PENDING',

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    CONSTRAINT fk_transactions_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_transactions_payment_method
        FOREIGN KEY (payment_method_id)
        REFERENCES payment_methods(payment_method_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_transactions_exchange_rate
        FOREIGN KEY (exchange_rate_id)
        REFERENCES exchange_rates(exchange_rate_id)
        ON DELETE RESTRICT

);

-- ============================================================
-- NOTIFICATIONS TABLE
-- Stores all notifications sent to GlobePay users.
-- ============================================================

CREATE TABLE notifications (

    notification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    notification_type notification_type_enum NOT NULL,

    title VARCHAR(150) NOT NULL,

    message TEXT NOT NULL,

    delivery_status notification_delivery_status_enum
        NOT NULL
        DEFAULT 'PENDING',

    sent_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    read_at TIMESTAMPTZ,

    CONSTRAINT fk_notifications_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE

);

-- ============================================================
-- AUDIT_LOGS TABLE
-- Stores all important user actions for security,
-- compliance, and forensic investigations.
-- ============================================================

CREATE TABLE audit_logs (

    audit_log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    action_type audit_action_enum NOT NULL,

    module_name VARCHAR(100) NOT NULL,

    ip_address INET NOT NULL,

    timestamp TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    CONSTRAINT fk_audit_logs_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE

);

-- ============================================================
-- REFRESH_TOKENS TABLE
-- Stores JWT refresh tokens for authenticated users.
-- Each token belongs to one user session.
-- ============================================================

CREATE TABLE refresh_tokens (

    token_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    session_id UUID NOT NULL,

    refresh_token TEXT
        NOT NULL
        UNIQUE,

    expiry_date TIMESTAMPTZ NOT NULL,

    created_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    CONSTRAINT fk_refresh_tokens_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_refresh_tokens_session
        FOREIGN KEY (session_id)
        REFERENCES user_sessions(session_id)
        ON DELETE CASCADE

);

-- ============================================================
-- QR_SCANS TABLE
-- Stores every QR code scanned by GlobePay users.
-- Used for analytics, fraud detection and troubleshooting.
-- ============================================================

CREATE TABLE qr_scans (

    qr_scan_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    linked_transaction_id UUID,

    raw_qr_data TEXT NOT NULL,

    merchant_name VARCHAR(150) NOT NULL,

    merchant_id VARCHAR(100) NOT NULL,

    merchant_country VARCHAR(100) NOT NULL,

    payment_network payment_network_enum NOT NULL,

    currency CHAR(3) NOT NULL,

    scanned_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    CONSTRAINT fk_qr_scans_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_qr_scans_transaction
        FOREIGN KEY (linked_transaction_id)
        REFERENCES transactions(transaction_id)
        ON DELETE SET NULL

);

-- ============================================================
-- PAYMENT_PROVIDER_LOGS TABLE
-- Stores webhook events received from payment providers.
-- Used for reconciliation, debugging and monitoring.
-- ============================================================

CREATE TABLE payment_provider_logs (

    provider_log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    transaction_id UUID NOT NULL,

    provider_name payment_provider_enum NOT NULL,

    event_type provider_event_enum NOT NULL,

    raw_payload JSONB NOT NULL,

    received_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    CONSTRAINT fk_provider_logs_transaction
        FOREIGN KEY (transaction_id)
        REFERENCES transactions(transaction_id)
        ON DELETE CASCADE

);

-- ============================================================
-- FX_RATE_REQUESTS TABLE
-- Stores every FX quote shown before payment confirmation.
-- Used for analytics and conversion-rate measurement.
-- ============================================================

CREATE TABLE fx_rate_requests (

    fx_request_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    source_currency CHAR(3) NOT NULL,

    target_currency CHAR(3) NOT NULL,

    requested_amount DECIMAL(18,2) NOT NULL,

    displayed_rate DECIMAL(18,8) NOT NULL,

    requested_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW(),

    converted_to_transaction BOOLEAN
        NOT NULL
        DEFAULT FALSE,

    CONSTRAINT fk_fx_requests_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE

);

-- ============================================================
-- SYSTEM_CONFIGURATIONS TABLE
-- Stores global application configurations.
-- Independent table with no foreign keys.
-- ============================================================

CREATE TABLE system_configurations (

    config_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    config_key VARCHAR(100)
        NOT NULL
        UNIQUE,

    config_value TEXT
        NOT NULL,

    updated_at TIMESTAMPTZ
        NOT NULL
        DEFAULT NOW()

);



