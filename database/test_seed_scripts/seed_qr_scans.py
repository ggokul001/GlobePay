import random

from faker import Faker

from seed_data_connection import get_connection

fake = Faker()


# ---------------------------------------------------
# QR Scan Status Templates
# ---------------------------------------------------

SCAN_FAILURE_REASONS = {

    "FAILED": [

        "Invalid QR format",

        "Unsupported payment network",

        "Corrupted QR code",

        "Currency not supported"

    ],

    "EXPIRED": [

        "Merchant QR expired",

        "QR code is no longer valid"

    ]

}


# ---------------------------------------------------
# Merchant Categories
# ---------------------------------------------------

MERCHANT_TYPES = [

    "Restaurant",

    "Hotel",

    "Supermarket",

    "Taxi",

    "Airport",

    "Shopping Mall",

    "Cafe",

    "Pharmacy"

]


# ---------------------------------------------------
# Generate QR Payload
# ---------------------------------------------------

def generate_raw_qr_data(

        merchant_id,

        merchant_name,

        currency,

        payment_network

):

    return (

        f"GPAY|"

        f"{merchant_id}|"

        f"{merchant_name}|"

        f"{currency}|"

        f"{payment_network}"

    )


# ---------------------------------------------------
# Generate Failure Reason
# ---------------------------------------------------

def generate_failure_reason(scan_status):

    if scan_status == "SUCCESS":

        return None

    return random.choice(

        SCAN_FAILURE_REASONS[scan_status]

    )

# ---------------------------------------------------
# Fetch Users
# ---------------------------------------------------

def fetch_users(cursor):

    cursor.execute("""

        SELECT

            user_id

        FROM users

    """)

    return cursor.fetchall()


# ---------------------------------------------------
# Fetch Transactions
# ---------------------------------------------------

def fetch_transactions(cursor):

    cursor.execute("""

        SELECT

            transaction_id,

            user_id,

            merchant_name,

            merchant_id,

            merchant_country,

            payment_network,

            merchant_currency

        FROM transactions

    """)

    return cursor.fetchall()


# ---------------------------------------------------
# Generate QR Scan Record
# ---------------------------------------------------

def generate_qr_scan_record(transaction):

    transaction_id = transaction[0]

    user_id = transaction[1]

    merchant_name = transaction[2]

    merchant_id = transaction[3]

    merchant_country = transaction[4]

    payment_network = transaction[5]

    currency = transaction[6]

    scan_status = random.choices(

        ["SUCCESS", "FAILED", "EXPIRED"],

        weights=[90, 7, 3],

        k=1

    )[0]

    failure_reason = generate_failure_reason(

        scan_status

    )

    linked_transaction_id = (

        transaction_id

        if scan_status == "SUCCESS"

        else None

    )

    raw_qr_data = generate_raw_qr_data(

        merchant_id,

        merchant_name,

        currency,

        payment_network

    )

    scanned_at = fake.date_time_between(

        start_date="-30d",

        end_date="now"

    )

    return (

        user_id,

        linked_transaction_id,

        raw_qr_data,

        merchant_name,

        merchant_id,

        merchant_country,

        payment_network,

        currency,

        scan_status,

        failure_reason,

        scanned_at

    )

# ---------------------------------------------------
# Seed QR Scans
# ---------------------------------------------------

def seed_qr_scans():

    conn = get_connection()

    cursor = conn.cursor()

    try:

        transactions = fetch_transactions(cursor)

        total_qr_scans = 0

        for transaction in transactions:

            qr_record = generate_qr_scan_record(
                transaction
            )

            cursor.execute(
                """

                INSERT INTO qr_scans
                (

                    user_id,

                    linked_transaction_id,

                    raw_qr_data,

                    merchant_name,

                    merchant_id,

                    merchant_country,

                    payment_network,

                    currency,

                    scan_status,

                    failure_reason,

                    scanned_at

                )

                VALUES
                (

                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s

                )

                """,

                qr_record

            )

            total_qr_scans += 1

        conn.commit()

        print(
            f"✅ Successfully inserted {total_qr_scans} QR scan records."
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

    seed_qr_scans()

    