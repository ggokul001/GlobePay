import random
from faker import Faker

from seed_data_connection import get_connection

fake = Faker()

PAYMENT_TYPES = [
    "CREDIT_CARD",
    "DEBIT_CARD",
    "BANK_ACCOUNT"
]

PROVIDERS = [
    "STRIPE",
    "ADYEN"
]

ACCOUNT_STATUS = [
    "ACTIVE",
    "INACTIVE",
    "SUSPENDED",
    "BLOCKED"
]


def generate_masked_account(payment_type):

    if payment_type in ["CREDIT_CARD", "DEBIT_CARD"]:
        return f"**** **** **** {random.randint(1000,9999)}"

    return f"XXXX{random.randint(100000,999999)}"


def seed_payment_methods(max_methods_per_user=3):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("SELECT user_id FROM users")

        users = cursor.fetchall()

        total_methods = 0

        for user in users:

            user_id = user[0]

            number_of_methods = random.randint(1, max_methods_per_user)

            for _ in range(number_of_methods):

                payment_type = random.choice(PAYMENT_TYPES)

                provider_name = random.choice(PROVIDERS)

                provider_token = fake.unique.uuid4()

                masked_account = generate_masked_account(payment_type)

                status = random.choice(ACCOUNT_STATUS)

                cursor.execute(
                    """
                    INSERT INTO payment_methods
                    (
                        user_id,
                        payment_type,
                        provider_name,
                        provider_token,
                        masked_account,
                        status
                    )

                    VALUES
                    (%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        user_id,
                        payment_type,
                        provider_name,
                        provider_token,
                        masked_account,
                        status
                    )
                )

                total_methods += 1

        conn.commit()

        print(f"✅ Successfully inserted {total_methods} payment methods.")

    except Exception as e:

        conn.rollback()

        print("❌ Error:", e)

    finally:

        cursor.close()
        conn.close()


if __name__ == "__main__":
    seed_payment_methods()