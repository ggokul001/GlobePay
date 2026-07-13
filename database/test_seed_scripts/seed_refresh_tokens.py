import random
import secrets

from datetime import timedelta

from faker import Faker

from seed_data_connection import get_connection

fake = Faker()


# ---------------------------------------------------
# Helper Function
# ---------------------------------------------------

def generate_refresh_token():

    """
    Generate a cryptographically secure
    refresh token.
    """

    return secrets.token_urlsafe(64)


# ---------------------------------------------------
# Generate Expiry Date
# ---------------------------------------------------

def generate_expiry_date(created_at):

    """
    Refresh tokens remain valid
    for 30 days.
    """

    return created_at + timedelta(days=30)


# ---------------------------------------------------
# Generate Revoked Date
# ---------------------------------------------------

def generate_revoked_date(created_at, expiry_date):

    """
    Around 10% of refresh tokens
    will be revoked before expiry.
    """

    should_revoke = random.random() < 0.10

    if not should_revoke:

        return None

    return fake.date_time_between(

        start_date=created_at,

        end_date=expiry_date

    )

# ---------------------------------------------------
# Fetch User Sessions
# ---------------------------------------------------

def fetch_user_sessions(cursor):

    cursor.execute("""

        SELECT

            session_id,

            user_id,

            login_time,

            expiry_time,

            status

        FROM user_sessions

    """)

    return cursor.fetchall()


# ---------------------------------------------------
# Generate Refresh Token Record
# ---------------------------------------------------

def generate_refresh_token_record(session):

    session_id = session[0]

    user_id = session[1]

    login_time = session[2]

    session_status = session[4]

    created_at = login_time

    expiry_date = generate_expiry_date(
        created_at
    )

    refresh_token = generate_refresh_token()

    revoked_at = None

    # If the session is inactive,
    # always revoke the refresh token.
    if session_status != "ACTIVE":

        revoked_at = fake.date_time_between(

            start_date=created_at,

            end_date=expiry_date

        )

    else:

        revoked_at = generate_revoked_date(

            created_at,

            expiry_date

        )

    return (

        user_id,

        session_id,

        refresh_token,

        expiry_date,

        revoked_at,

        created_at

    )

# ---------------------------------------------------
# Seed Refresh Tokens
# ---------------------------------------------------

def seed_refresh_tokens():

    conn = get_connection()

    cursor = conn.cursor()

    try:

        sessions = fetch_user_sessions(cursor)

        total_tokens = 0

        for session in sessions:

            token_record = generate_refresh_token_record(
                session
            )

            cursor.execute(
                """

                INSERT INTO refresh_tokens
                (

                    user_id,

                    session_id,

                    refresh_token,

                    expiry_date,

                    revoked_at,

                    created_at

                )

                VALUES
                (

                    %s,%s,%s,%s,%s,%s

                )

                """,

                token_record

            )

            total_tokens += 1

        conn.commit()

        print(
            f"✅ Successfully inserted {total_tokens} refresh tokens."
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

    seed_refresh_tokens()
