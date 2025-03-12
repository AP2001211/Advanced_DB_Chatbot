import streamlit as st
import requests
import re

# Backend URL
BACKEND_URL = "http://127.0.0.1:5000"

# Initialize session state
if "db_configured" not in st.session_state:
    st.session_state.db_configured = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "latest_query" not in st.session_state:
    st.session_state.latest_query = None  # Stores the most recent query but not in chat history

# Sidebar: Database Configuration
st.sidebar.header("Database Configuration")
openai_key = st.sidebar.text_input("OpenAI API Key", type="password")
db_host = st.sidebar.text_input("Database Host", "localhost")
db_user = st.sidebar.text_input("Database User", "root")
db_password = st.sidebar.text_input("Database Password", type="password")
db_name = st.sidebar.text_input("Database Name")

if st.sidebar.button("Save Configuration"):
    response = requests.post(f"{BACKEND_URL}/set_db_config", json={
        "openai_api_key": openai_key,
        "db_host": db_host,
        "db_user": db_user,
        "db_password": db_password,
        "db_name": db_name
    })
    
    if response.status_code == 200:
        st.session_state.db_configured = True
        st.sidebar.success("Configuration Saved!")

# Main Chat Interface
if st.session_state.db_configured:
    st.title("Chat with Database")

    # Display Chat History
    st.subheader("Chat History")
    if st.button("Load Chat History"):
        response = requests.get(f"{BACKEND_URL}/get_chat_history", params={"session_id": "test_session"})
        if response.status_code == 200:
            st.session_state.chat_history = response.json().get("chat_history", [])

    for entry in st.session_state.chat_history:
        user_query = entry.get("user_query", "Unknown Query")
        generated_query = entry.get("generated_query", "No Response")

        # Extract SQL query
        sql_match = re.search(r"```(.*?)```", generated_query, re.DOTALL)
        if sql_match:
            sql_query = sql_match.group(1).strip()
            description = generated_query.replace(sql_match.group(0), "").strip()
        else:
            sql_query = "No SQL query detected"
            description = generated_query

        with st.expander(f"User Query: {user_query}"):
            st.text_area("Generated SQL Query:", value=sql_query, height=80, disabled=True)
            st.text_area("Description:", value=description, height=100, disabled=True)

    # Button to Clear Chat History
    if st.button("Clear Chat History"):
        response = requests.post(f"{BACKEND_URL}/clear_chat_history", json={"session_id": "test_session"})
        if response.status_code == 200:
            # Reset history state
            st.session_state.chat_history = []
            st.session_state.latest_query = None
            st.session_state.history_loaded = False  # Prevents old history from still displaying
            st.success("Chat history cleared!")

            # Rerun the script to refresh UI (without losing credentials)
            st.rerun()

    # User Input Section
    user_query = st.text_input("Enter your natural language query:")
    
    if st.button("Generate SQL Query"):
        response = requests.post(f"{BACKEND_URL}/generate_query", json={
            "query": user_query,
            "session_id": "test_session"
        })
        
        if response.status_code == 200:
            generated_response = response.json().get("generated_query", "")

            # Extract SQL query using regex
            if generated_response:
                sql_match = re.search(r"```(.*?)```", generated_response, re.DOTALL)
                if sql_match:
                    sql_query = sql_match.group(1).strip()
                    description = generated_response.replace(sql_match.group(0), "").strip()
                else:
                    sql_query = "No SQL query detected"
                    description = generated_response
            else:
                sql_query = "No response received"
                description = "The backend did not return a valid query."

            # Move previous latest_query to chat history before updating latest_query
            if st.session_state.latest_query:
                st.session_state.chat_history.append(st.session_state.latest_query)

            # Store the new query as the latest query
            st.session_state.latest_query = {
                "user_query": user_query,
                "generated_query": generated_response
            }

            st.rerun()

    # Display the latest query (not in chat history yet)
    if st.session_state.latest_query:
        st.subheader("Latest Query")
        user_query = st.session_state.latest_query["user_query"]
        generated_query = st.session_state.latest_query["generated_query"]

        sql_match = re.search(r"```(.*?)```", generated_query, re.DOTALL) if generated_query else None
        sql_query = sql_match.group(1).strip() if sql_match else "No SQL query detected"
        description = generated_query.replace(sql_match.group(0), "").strip() if sql_match else generated_query

        st.text_area("Generated SQL Query:", value=sql_query, height=100, disabled=False)
        st.text_area("Description:", value=description, height=150, disabled=False)

else:
    st.warning("Please configure the database connection first.")
