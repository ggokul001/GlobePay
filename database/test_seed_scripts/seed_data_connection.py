import psycopg2

DB_HOST = "localhost"
DB_PORT = "5433"          # Change if your PostgreSQL uses a different port
DB_NAME = "Globepay_dev"      # Your database name
DB_USER = "postgres"
DB_PASSWORD = "#include"


def get_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        print("✅ Connected to PostgreSQL successfully!")

        return conn

    except Exception as e:
        print("❌ Database Connection Failed")
        print(e)
        return None