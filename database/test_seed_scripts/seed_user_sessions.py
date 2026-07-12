import random
from datetime import timedelta
from faker import Faker

from seed_data_connection import get_connection

fake = Faker()

DEVICE_TYPES = [
    "Android",
    "iPhone",
    "Windows",
    "MacBook",
    "Linux",
    "iPad"
]

SESSION_STATUS = [
    "ACTIVE",
    "EXPIRED",
    "REVOKED"
]


def seed_user_sessions(max_sessions_per_user=3):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # Fetch all existing users
        cursor.execute("SELECT user_id FROM users")

        users = cursor.fetchall()

        total_sessions = 0

        for user in users:

            user_id = user[0]

            number_of_sessions = random.randint(1, max_sessions_per_user)

            for _ in range(number_of_sessions):

                device_type = random.choice(DEVICE_TYPES)

                device_id = fake.uuid4()

                ip_address = fake.ipv4()

                login_time = fake.date_time_between(
                    start_date="-30d",
                    end_date="now"
                )

                expiry_time = login_time + timedelta(
                    days=random.randint(1,30)
                )

                status = random.choice(SESSION_STATUS)

                cursor.execute(
                    """
                    INSERT INTO user_sessions
                    (
                        user_id,
                        device_type,
                        device_id,
                        ip_address,
                        login_time,
                        expiry_time,
                        status
                    )

                    VALUES
                    (%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        user_id,
                        device_type,
                        device_id,
                        ip_address,
                        login_time,
                        expiry_time,
                        status
                    )
                )

                total_sessions += 1

        conn.commit()

        print(f"✅ Successfully inserted {total_sessions} user sessions.")

    except Exception as e:

        conn.rollback()

        print("❌ Error:", e)

    finally:

        cursor.close()
        conn.close()


if __name__ == "__main__":
    seed_user_sessions()