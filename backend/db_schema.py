import mysql.connector
import os

def get_db_connection():
    """
    Establish a database connection using environment variables.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "")
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def get_db_schema():
    """
    Retrieve the database schema dynamically.
    """
    connection = get_db_connection()
    if not connection:
        return {"error": "Could not connect to the database. Check configuration."}

    cursor = connection.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE();")
    tables = cursor.fetchall()
    schema = {}

    for (table,) in tables:
        cursor.execute(f"DESCRIBE {table}")
        columns = cursor.fetchall()
        schema[table] = [{"Field": col[0], "Type": col[1], "Null": col[2], "Key": col[3], "Default": col[4], "Extra": col[5]} for col in columns]

    cursor.close()
    connection.close()
    return schema
