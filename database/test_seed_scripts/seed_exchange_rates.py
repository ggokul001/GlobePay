from seed_data_connection import get_connection

EXCHANGE_RATES = [

    ("INR","USD",0.01165,2.00,"STRIPE"),
    ("USD","INR",85.85000,1.20,"ADYEN"),

    ("INR","SGD",0.01560,1.50,"STRIPE"),
    ("SGD","INR",64.10000,1.80,"ADYEN"),

    ("USD","SGD",1.28300,1.30,"STRIPE"),
    ("SGD","USD",0.77900,1.40,"ADYEN"),

    ("EUR","USD",1.17000,1.20,"STRIPE"),
    ("USD","EUR",0.85400,1.10,"ADYEN"),

    ("EUR","INR",100.25000,1.60,"STRIPE"),
    ("INR","EUR",0.00997,1.80,"ADYEN"),

]


def seed_exchange_rates():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        total = 0

        for row in EXCHANGE_RATES:

            source_currency = row[0]
            target_currency = row[1]
            provider_rate = row[2]
            spread_percentage = row[3]
            provider_name = row[4]

            customer_rate = provider_rate - (
                provider_rate * (spread_percentage / 100)
            )

            cursor.execute(
                """
                INSERT INTO exchange_rates
                (
                    source_currency,
                    target_currency,
                    provider_rate,
                    spread_percentage,
                    customer_rate,
                    provider_name
                )

                VALUES
                (%s,%s,%s,%s,%s,%s)
                """,
                (
                    source_currency,
                    target_currency,
                    provider_rate,
                    spread_percentage,
                    customer_rate,
                    provider_name
                )
            )

            total += 1

        conn.commit()

        print(f"✅ Successfully inserted {total} exchange rates.")

    except Exception as e:

        conn.rollback()

        print("❌ Error :", e)

    finally:

        cursor.close()
        conn.close()


if __name__ == "__main__":
    seed_exchange_rates()