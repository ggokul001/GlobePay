from seed_data_connection import get_connection

print("🚀 Starting Database Connection Test...")

conn = get_connection()

if conn:
    print("✅ Database is ready!")

    cursor = conn.cursor()

    cursor.execute("SELECT version();")

    version = cursor.fetchone()

    print("📌 PostgreSQL Version:")
    print(version[0])

    cursor.close()
    conn.close()

    print("🔒 Connection Closed Successfully!")

else:
    print("❌ Failed to connect to the database.")