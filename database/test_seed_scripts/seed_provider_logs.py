import random
import json

from faker import Faker

from seed_data_connection import get_connection

fake = Faker()


# ---------------------------------------------------
# Provider Response Templates
# ---------------------------------------------------

PROVIDER_RESPONSES = {

    "SUCCESS": [

        "Payment approved",

        "Transaction completed successfully",

        "Charge captured successfully"

    ],

    "FAILED": [

        "Card declined",

        "Insufficient balance",

        "Authentication failed",

        "Invalid merchant"

    ],

    "PENDING": [

        "Awaiting provider confirmation",

        "Webhook pending"

    ],

    "TIMEOUT": [

        "Gateway timeout",

        "Provider timeout"

    ]

}


# ---------------------------------------------------
# Generate Provider Payload
# ---------------------------------------------------

def generate_payload(

        transaction_id,

        provider_name,

        event_type,

        response_status

):

    payload = {

        "transaction_id": str(transaction_id),

        "provider_name": provider_name,

        "event_type": event_type,

        "response_status": response_status,

        "provider_reference": fake.uuid4(),

        "processed_at": fake.iso8601()

    }

    return json.dumps(payload)


# ---------------------------------------------------
# Generate Response Message
# ---------------------------------------------------

def generate_response_message(status):

    return random.choice(

        PROVIDER_RESPONSES[status]

    )

# ---------------------------------------------------
# Fetch Transactions
# ---------------------------------------------------

def fetch_transactions(cursor):

    cursor.execute("""

        SELECT

            transaction_id,

            payment_provider,

            status

        FROM transactions

    """)

    return cursor.fetchall()


# ---------------------------------------------------
# Generate Provider Log Record
# ---------------------------------------------------

def generate_provider_log_record(transaction):

    transaction_id = transaction[0]

    provider_name = transaction[1]

    transaction_status = transaction[2]

    # ---------------------------------------
    # Response Status
    # ---------------------------------------

    if transaction_status == "SUCCESS":

        response_status = "SUCCESS"
        event_type = "charge_succeeded"

    elif transaction_status == "FAILED":

        response_status = "FAILED"
        event_type = "charge_failed"

    elif transaction_status == "PENDING":

        response_status = "PENDING"
        event_type = "webhook_received"

    else:

        response_status = random.choice(
            [
                "SUCCESS",
                "FAILED",
                "PENDING",
                "TIMEOUT"
            ]
        )

        if response_status == "SUCCESS":

            event_type = "charge_succeeded"

        elif response_status == "FAILED":

            event_type = "charge_failed"

        elif response_status == "PENDING":

            event_type = "webhook_received"

        else:

            event_type = random.choice(
                [
                    "charge_failed",
                    "refund_completed",
                    "webhook_received"
                ]
            )

    response_message = generate_response_message(
        response_status
    )

    raw_payload = generate_payload(

        transaction_id,

        provider_name,

        event_type,

        response_status

    )

    received_at = fake.date_time_between(

        start_date="-30d",

        end_date="now"

    )

    return (

        transaction_id,

        provider_name,

        event_type,

        raw_payload,

        response_status,

        response_message,

        received_at

    )

# ---------------------------------------------------
# Seed Payment Provider Logs
# ---------------------------------------------------

def seed_payment_provider_logs():

    conn = get_connection()

    cursor = conn.cursor()

    try:

        transactions = fetch_transactions(cursor)

        total_logs = 0

        for transaction in transactions:

            provider_log = generate_provider_log_record(
                transaction
            )

            cursor.execute(
                """

                INSERT INTO payment_provider_logs
                (

                    transaction_id,

                    provider_name,

                    event_type,

                    raw_payload,

                    response_status,

                    response_message,

                    received_at

                )

                VALUES
                (

                    %s,%s,%s,%s,%s,%s,%s

                )

                """,

                provider_log

            )

            total_logs += 1

        conn.commit()

        print(
            f"✅ Successfully inserted {total_logs} payment provider log records."
        )

    except Exception as e:

        conn.rollback()

        print(f"❌ Error: {e}")

    finally:

        cursor.close()

        conn.close()

# ---------------------------------------------------
# Main Function
# ---------------------------------------------------

if __name__ == "__main__":

    seed_payment_provider_logs()