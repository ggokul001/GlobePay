import random
import uuid
from decimal import Decimal
from faker import Faker

from seed_data_connection import get_connection

fake = Faker()


# ---------------------------------------
# Merchant Data
# ---------------------------------------

MERCHANTS = [

    ("Apple Store", "Singapore", "SGD"),
    ("Starbucks", "Singapore", "SGD"),
    ("Amazon", "United States", "USD"),
    ("Nike", "United States", "USD"),
    ("Adidas", "Germany", "EUR"),
    ("Carrefour", "France", "EUR"),
    ("Uniqlo", "Japan", "JPY"),
    ("IKEA", "Sweden", "SEK"),
    ("Lulu Hypermarket", "UAE", "AED"),
    ("Tesco", "United Kingdom", "GBP")

]


# ---------------------------------------
# Payment Networks
# ---------------------------------------

PAYMENT_NETWORKS = [

    "CARD",
    "BANK_TRANSFER",
    "UPI",
    "PAYNOW",
    "PROMPTPAY"

]


# ---------------------------------------
# Transaction Status
# ---------------------------------------

TRANSACTION_STATUS = [

    "SUCCESS",
    "SUCCESS",
    "SUCCESS",
    "SUCCESS",
    "SUCCESS",
    "PROCESSING",
    "PENDING",
    "FAILED",
    "REFUNDED"

]


# ---------------------------------------
# Helper Functions
# ---------------------------------------

def generate_original_amount():

    return round(
        random.uniform(10, 5000),
        2
    )


def generate_transaction_fee(amount):

    return round(
        amount * 0.015,
        2
    )


def generate_provider_transaction_id():

    return "TXN-" + fake.unique.bothify(
        text="##########"
    )


def generate_failure_reason(status):

    if status != "FAILED":
        return None

    return random.choice(

        [

            "Insufficient Balance",

            "Card Expired",

            "Bank Declined",

            "Network Timeout",

            "Fraud Detection"

        ]

    )

# ---------------------------------------
# Fetch Existing Database Records
# ---------------------------------------

def fetch_users(cursor):

    cursor.execute("""

        SELECT user_id

        FROM users

    """)

    return cursor.fetchall()


def fetch_payment_methods(cursor, user_id):

    cursor.execute("""

        SELECT
            payment_method_id,
            provider_name

        FROM payment_methods

        WHERE user_id = %s

    """, (user_id,))

    return cursor.fetchall()


def fetch_exchange_rates(cursor):

    cursor.execute("""

        SELECT

            exchange_rate_id,

            source_currency,

            target_currency,

            customer_rate,

            provider_name

        FROM exchange_rates

    """)

    return cursor.fetchall()


# ---------------------------------------
# Generate One Transaction
# ---------------------------------------

def generate_transaction(cursor, user_id):

    payment_methods = fetch_payment_methods(cursor, user_id)

    if not payment_methods:
        return None

    exchange_rates = fetch_exchange_rates(cursor)

    if not exchange_rates:
        return None

    payment_method = random.choice(payment_methods)

    payment_method_id = payment_method[0]

    exchange_rate = random.choice(exchange_rates)

    exchange_rate_id = exchange_rate[0]

    source_currency = exchange_rate[1]

    target_currency = exchange_rate[2]

    customer_rate = Decimal(str(exchange_rate[3]))

    provider_name = exchange_rate[4]

    merchant = random.choice(MERCHANTS)

    merchant_name = merchant[0]

    merchant_country = merchant[1]

    merchant_currency = merchant[2]

    original_amount = Decimal(
        str(generate_original_amount())
    )

    converted_amount = round(
        original_amount * customer_rate,
        2
    )

    transaction_fee = Decimal(
        str(generate_transaction_fee(float(original_amount)))
    )

    payment_network = random.choice(PAYMENT_NETWORKS)

    status = random.choice(TRANSACTION_STATUS)

    failure_reason = generate_failure_reason(status)

    provider_transaction_id = generate_provider_transaction_id()

    idempotency_key = str(uuid.uuid4())

    merchant_id = fake.unique.bothify(
        text="MERCHANT-#####"
    )

    return (

        user_id,

        payment_method_id,

        exchange_rate_id,

        merchant_name,

        merchant_id,

        merchant_country,

        merchant_currency,

        source_currency,

        payment_network,

        original_amount,

        converted_amount,

        transaction_fee,

        provider_name,

        provider_transaction_id,

        customer_rate,

        idempotency_key,

        failure_reason,

        status

    )

# ---------------------------------------
# Seed Transactions
# ---------------------------------------

def seed_transactions(max_transactions_per_user=10):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        users = fetch_users(cursor)

        total_transactions = 0

        for user in users:

            user_id = user[0]

            transaction_count = random.randint(
                1,
                max_transactions_per_user
            )

            for _ in range(transaction_count):

                transaction = generate_transaction(
                    cursor,
                    user_id
                )

                if transaction is None:
                    continue

                cursor.execute(
                    """

                    INSERT INTO transactions
                    (

                        user_id,

                        payment_method_id,

                        exchange_rate_id,

                        merchant_name,

                        merchant_id,

                        merchant_country,

                        merchant_currency,

                        user_currency,

                        payment_network,

                        original_amount,

                        converted_amount,

                        transaction_fee,

                        payment_provider,

                        provider_transaction_id,

                        applied_fx_rate,

                        idempotency_key,

                        failure_reason,

                        status

                    )

                    VALUES
                    (

                        %s,%s,%s,%s,%s,%s,%s,%s,

                        %s,%s,%s,%s,%s,%s,%s,

                        %s,%s,%s

                    )

                    """,

                    transaction

                )

                total_transactions += 1

        conn.commit()

        print(f"✅ Successfully inserted {total_transactions} transactions.")

    except Exception as e:

        conn.rollback()

        print("❌ Error:", e)

    finally:

        cursor.close()
        conn.close()

# ---------------------------------------
# Main Function
# ---------------------------------------

if __name__ == "__main__":

    seed_transactions()