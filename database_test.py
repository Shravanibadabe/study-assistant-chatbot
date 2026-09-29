from database import get_connection


try:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT version();")

    version = cursor.fetchone()

    print("Neon PostgreSQL connected successfully!")

    print(version[0])

    cursor.close()
    connection.close()

except Exception as e:

    print("Database connection failed:")
    print(e)