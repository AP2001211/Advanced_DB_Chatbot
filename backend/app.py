from flask import Flask, jsonify, request
from routes.chat import chat_blueprint
from routes.schema import schema_blueprint
from query_generator import generate_query
from config import Config
import os
from dotenv import load_dotenv
from services.chroma_service import clear_chat_history, get_chat_history


app = Flask(__name__)
load_dotenv()
app.config.from_object(Config)

# Register Blueprints
app.register_blueprint(chat_blueprint, url_prefix='/chat')
app.register_blueprint(schema_blueprint, url_prefix='/schema')

@app.route('/set_db_config', methods=['POST'])
def set_db_config():
    """
    Endpoint to dynamically update database and OpenAI API configurations.
    """
    data = request.json
    os.environ["DB_HOST"] = data.get("db_host", "localhost")
    os.environ["DB_USER"] = data.get("db_user", "root")
    os.environ["DB_PASSWORD"] = data.get("db_password", "")
    os.environ["DB_NAME"] = data.get("db_name", "")
    os.environ["OPENAI_API_KEY"] = data.get("openai_api_key", "")

    return jsonify({"message": "Database configuration updated successfully"})

def get_db_config():
    """
    Returns the current database configuration from environment variables.
    """
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", ""),
    }

@app.route('/get_db_config', methods=['GET'])
def get_db_config_endpoint():
    """
    API endpoint to fetch the currently set database configurations.
    """
    return jsonify(get_db_config())

# Query Generation API
@app.route('/generate_query', methods=['POST'])
def generate_query_endpoint():
    """
    API endpoint to generate an SQL query using LangChain.
    """
    data = request.json
    user_input = data.get("query")
    session_id = data.get("session_id")

    generated_query = generate_query(user_input, session_id)
    
    return jsonify({"generated_query": generated_query})

@app.route('/get_chat_history', methods=['GET'])
def get_chat_history_endpoint():
    session_id = request.args.get("session_id", "test_session")
    history = get_chat_history(session_id)
    return jsonify({"chat_history": history})

@app.route('/clear_chat_history', methods=['POST'])
def clear_chat_history_endpoint():
    session_id = request.json.get("session_id", "test_session")
    clear_chat_history(session_id)
    return jsonify({"message": "Chat history cleared successfully"})

if __name__ == '__main__':
    app.run(debug=True)
