import random
from faker import Faker
from seed_data_connection import get_connection

fake = Faker()

COUNTRIES = [
    "India",
    "Singapore",
    "United States",
    "United Kingdom",
    "Germany",
    "Australia",
    "Canada",
    "France",
    "Japan",
    "UAE"
]

KYC_STATUS = [
    "PENDING",
    "UNDER_REVIEW",
    "VERIFIED",
    "REJECTED"
]

ACCOUNT_STATUS = [
    "ACTIVE",
    "INACTIVE",
    "SUSPENDED",
    "BLOCKED"
]


def seed_users(total_users=10000):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        for _ in range(total_users):

            full_name = fake.name()

            email = fake.unique.email()

            phone_number = fake.unique.msisdn()[:15]

            country = random.choice(COUNTRIES)

            kyc_status = random.choice(KYC_STATUS)

            account_status = random.choice(ACCOUNT_STATUS)

            cursor.execute(
                """
                INSERT INTO users
                (
                    full_name,
                    email,
                    phone_number,
                    country,
                    kyc_status,
                    account_status
                )

                VALUES
                (%s,%s,%s,%s,%s,%s)
                """,

                (
                    full_name,
                    email,
                    phone_number,
                    country,
                    kyc_status,
                    account_status
                )
            )

        conn.commit()

        print(f"✅ Successfully inserted {total_users} users.")

    except Exception as e:

        conn.rollback()

        print("❌ Error :", e)

    finally:

        cursor.close()

        conn.close()


if __name__ == "__main__":
    seed_users()