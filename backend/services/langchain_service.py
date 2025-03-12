from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from services.chroma_service import retrieve_context, store_context
import os

# Initialize LLM with API Key from environment variables

def create_llm():
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    if not openai_api_key:
        raise ValueError("API Key not set in environment variables")
    llm = ChatOpenAI(model_name="gpt-4", openai_api_key=openai_api_key)
    return llm

def generate_sql_query(user_query, schema, session_id):
    """
    Generates an SQL query based on user input, schema, and session context.
    """
    # Retrieve previous context
    previous_context = retrieve_context(session_id)

    # Define prompt template
    prompt_template = PromptTemplate(
        input_variables=["context", "schema", "query"],
        template=(
            "You are an expert SQL query generator. "
            "Given the following database schema: {schema}, "
            "and the previous conversation context: {context}, "
            "generate an SQL query that fulfills this request: {query}. "
            "Ensure the query is syntactically correct and optimized."
        )
    )

    # Format the prompt
    prompt = prompt_template.format(
        schema=schema,
        context=previous_context if previous_context else "No previous context",
        query=user_query
    )
    llm = create_llm()
    # Generate SQL query
    generated_query = llm.predict(prompt)

    # Store context for future queries
    store_context(session_id, user_query, generated_query)

    return generated_query
