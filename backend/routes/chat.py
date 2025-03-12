from flask import Blueprint, request, jsonify
from services.langchain_service import generate_sql_query
from services.chroma_service import get_session_context, update_session_context

chat_blueprint = Blueprint('chat', __name__)

@chat_blueprint.route('/', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("query")
    session_id = data.get("session_id")  # Ensure session_id is passed from frontend

    # Retrieve session context
    context = get_session_context(session_id)

    # Generate SQL query based on input and context
    generated_query = generate_sql_query(user_input, context, session_id)

    # Update session context
    update_session_context(session_id, user_input, generated_query)

    return jsonify({"generated_query": generated_query})
