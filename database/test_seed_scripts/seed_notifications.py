import random
from datetime import timedelta

from faker import Faker

from seed_data_connection import get_connection

fake = Faker()


# ---------------------------------------------------
# Delivery Status
# ---------------------------------------------------

DELIVERY_STATUS = [

    "SENT",
    "DELIVERED",
    "READ",
    "FAILED"

]


# ---------------------------------------------------
# Notification Templates
# ---------------------------------------------------

SUCCESS_MESSAGES = [

    (
        "Payment Successful",
        "Your payment has been completed successfully."
    ),

    (
        "Transaction Completed",
        "Your international payment was successful."
    )

]


FAILED_MESSAGES = [

    (
        "Payment Failed",
        "Your payment could not be processed."
    ),

    (
        "Transaction Failed",
        "The payment was declined by the provider."
    )

]


PENDING_MESSAGES = [

    (
        "Payment Pending",
        "Your payment is waiting for confirmation."
    )

]


PROCESSING_MESSAGES = [

    (
        "Payment Processing",
        "Your payment is currently being processed."
    )

]


REFUND_MESSAGES = [

    (
        "Refund Processed",
        "Your refund has been processed successfully."
    )

]


# ---------------------------------------------------
# Helper Function
# ---------------------------------------------------

def get_notification(status):

    if status == "SUCCESS":
        return random.choice(SUCCESS_MESSAGES)

    elif status == "FAILED":
        return random.choice(FAILED_MESSAGES)

    elif status == "PENDING":
        return random.choice(PENDING_MESSAGES)

    elif status == "PROCESSING":
        return random.choice(PROCESSING_MESSAGES)

    elif status == "REFUNDED":
        return random.choice(REFUND_MESSAGES)

    else:
        return (
            "Transaction Update",
            "Your transaction status has been updated."
        )

# ---------------------------------------------------
# Fetch Transactions
# ---------------------------------------------------

def fetch_transactions(cursor):

    cursor.execute("""

        SELECT

            transaction_id,

            user_id,

            merchant_name,

            original_amount,

            merchant_currency,

            status,

            created_at

        FROM transactions

    """)

    return cursor.fetchall()


# ---------------------------------------------------
# Generate Notification
# ---------------------------------------------------

def generate_notification(transaction):

    transaction_id = transaction[0]

    user_id = transaction[1]

    merchant_name = transaction[2]

    amount = transaction[3]

    currency = transaction[4]

    transaction_status = transaction[5]

    transaction_time = transaction[6]

    title, message = get_notification(
        transaction_status
    )

    # Add transaction details to the message
    message = (
        f"{message}\n\n"
        f"Merchant : {merchant_name}\n"
        f"Amount : {currency} {amount}"
    )

    delivery_status = random.choice(
        DELIVERY_STATUS
    )

    sent_at = transaction_time + timedelta(
        minutes=random.randint(1, 5)
    )

    read_at = None

    if delivery_status == "READ":

        read_at = sent_at + timedelta(
            minutes=random.randint(1, 120)
        )

    return (

        user_id,

        transaction_id,

        "PAYMENT",

        title,

        message,

        delivery_status,

        sent_at,

        read_at

    )

# ---------------------------------------------------
# Seed Notifications
# ---------------------------------------------------

def seed_notifications():

    conn = get_connection()

    cursor = conn.cursor()

    try:

        transactions = fetch_transactions(cursor)

        total_notifications = 0

        for transaction in transactions:

            notification = generate_notification(
                transaction
            )

            cursor.execute(
                """

                INSERT INTO notifications
                (

                    user_id,

                    transaction_id,

                    notification_type,

                    title,

                    message,

                    delivery_status,

                    sent_at,

                    read_at

                )

                VALUES
                (

                    %s,%s,%s,%s,%s,%s,%s,%s

                )

                """,

                notification

            )

            total_notifications += 1

        conn.commit()

        print(
            f"✅ Successfully inserted {total_notifications} notifications."
        )

    except Exception as e:

        conn.rollback()

        print("❌ Error:", e)

    finally:

        cursor.close()

        conn.close()


# ---------------------------------------------------
# Main Function
# ---------------------------------------------------

if __name__ == "__main__":

    seed_notifications()


