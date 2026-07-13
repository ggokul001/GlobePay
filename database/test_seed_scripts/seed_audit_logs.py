import random

from faker import Faker

from seed_data_connection import get_connection

fake = Faker()


# ---------------------------------------------------
# Module Names
# ---------------------------------------------------

MODULES = [

    "Authentication",

    "Transactions",

    "Payment Methods",

    "Notifications",

    "User Profile",

    "KYC"

]


# ---------------------------------------------------
# Audit Action Templates
# ---------------------------------------------------

ACTION_DETAILS = {

    "LOGIN": [

        "User logged into GlobePay.",

        "Successful login from a registered device."

    ],

    "LOGOUT": [

        "User logged out successfully."

    ],

    "CREATE": [

        "Created a new transaction.",

        "Added a new payment method.",

        "Created a new profile record."

    ],

    "UPDATE": [

        "Updated profile information.",

        "Updated payment method.",

        "Updated KYC information."

    ],

    "DELETE": [

        "Removed a payment method.",

        "Deleted an inactive session."

    ],

    "PAYMENT": [

        "International payment processed.",

        "Payment completed successfully.",

        "Payment failed during processing.",

        "Refund issued successfully."

    ]

}


# ---------------------------------------------------
# Helper Function
# ---------------------------------------------------

def get_action_details(action_type):

    return random.choice(
        ACTION_DETAILS[action_type]
    )

# ---------------------------------------------------
# Fetch Users
# ---------------------------------------------------

def fetch_users(cursor):

    cursor.execute("""

        SELECT user_id

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

            status

        FROM transactions

    """)

    return cursor.fetchall()


# ---------------------------------------------------
# Generate Audit Record
# ---------------------------------------------------

def generate_audit_record(user_id, transaction=None):

    if transaction is None:

        action_type = random.choice([

            "LOGIN",
            "LOGOUT",
            "UPDATE",
            "DELETE"

        ])

        transaction_id = None

    else:

        transaction_id = transaction[0]

        action_type = random.choice([

            "PAYMENT",
            "CREATE",
            "UPDATE"

        ])

    module_name = random.choice(MODULES)

    action_details = get_action_details(
        action_type
    )

    ip_address = fake.ipv4_public()

    timestamp = fake.date_time_between(

        start_date="-30d",

        end_date="now"

    )

    return (

        user_id,

        transaction_id,

        action_type,

        module_name,

        action_details,

        ip_address,

        timestamp

    )

# ---------------------------------------------------
# Seed Audit Logs
# ---------------------------------------------------

def seed_audit_logs():

    conn = get_connection()

    cursor = conn.cursor()

    try:

        users = fetch_users(cursor)

        transactions = fetch_transactions(cursor)

        total_logs = 0

        # ---------------------------------------------------
        # Transaction-related audit logs
        # ---------------------------------------------------

        for transaction in transactions:

            user_id = transaction[1]

            audit_record = generate_audit_record(

                user_id,

                transaction

            )

            cursor.execute(
                """

                INSERT INTO audit_logs
                (

                    user_id,

                    transaction_id,

                    action_type,

                    module_name,

                    action_details,

                    ip_address,

                    timestamp

                )

                VALUES
                (

                    %s,%s,%s,%s,%s,%s,%s

                )

                """,

                audit_record

            )

            total_logs += 1

        # ---------------------------------------------------
        # User activity logs
        # ---------------------------------------------------

        for user in users:

            user_id = user[0]

            activity_count = random.randint(2, 5)

            for _ in range(activity_count):

                audit_record = generate_audit_record(

                    user_id,

                    None

                )

                cursor.execute(
                    """

                    INSERT INTO audit_logs
                    (

                        user_id,

                        transaction_id,

                        action_type,

                        module_name,

                        action_details,

                        ip_address,

                        timestamp

                    )

                    VALUES
                    (

                        %s,%s,%s,%s,%s,%s,%s

                    )

                    """,

                    audit_record

                )

                total_logs += 1

        conn.commit()

        print(
            f"✅ Successfully inserted {total_logs} audit logs."
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

    seed_audit_logs()

    