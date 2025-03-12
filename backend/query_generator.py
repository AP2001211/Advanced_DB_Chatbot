from services.langchain_service import generate_sql_query
from db_schema import get_db_schema

def generate_query(user_input, session_id):
    """
    Generate an SQL query based on user input and the current database schema.
    """
    schema = get_db_schema()
    
    if "error" in schema:
        return {"error": "Failed to retrieve database schema. Ensure the database connection is properly configured."}

    return generate_sql_query(user_input, schema, session_id)
