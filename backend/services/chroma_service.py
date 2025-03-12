import chromadb
import json

# Initialize ChromaDB client (Ensure the path is correct)
try:
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection(name="chat_context")
except Exception as e:
    print(f"Error initializing ChromaDB client: {e}")
    collection = None

def store_context(session_id, user_query, generated_query):
    """
    Store user query and generated SQL query as context in ChromaDB.
    """
    if collection is None:
        print("ChromaDB collection not initialized properly.")
        return
    
    data = {"user_query": user_query, "generated_query": generated_query}
    
    # Convert dictionary to JSON string and upsert
    try:
        collection.upsert(
            ids=[session_id], 
            documents=[json.dumps(data)]  # Store as JSON string
        )
    except Exception as e:
        print(f"Error storing context in ChromaDB: {e}")

def retrieve_context(session_id):
    """
    Retrieve context for a given session.
    """
    if collection is None:
        print("ChromaDB collection not initialized properly.")
        return "No previous context"
    
    try:
        results = collection.get(ids=[session_id])
        
        if results and "documents" in results and results["documents"]:
            stored_data = json.loads(results["documents"][0])  # Convert JSON string back to dictionary
            return f"User Query: {stored_data['user_query']}, Generated SQL: {stored_data['generated_query']}"
        
        return "No previous context"
    
    except Exception as e:
        print(f"Error retrieving context from ChromaDB: {e}")
        return "No previous context"


# New functions to match the imports in chat.py

def get_session_context(session_id):
    """
    Retrieve session context for a given session.
    This function is a wrapper around `retrieve_context`.
    """
    return retrieve_context(session_id)

def update_session_context(session_id, user_query, generated_query):
    """
    Update session context with the new user query and generated SQL.
    This function is a wrapper around `store_context`.
    """
    store_context(session_id, user_query, generated_query)

def get_chat_history(session_id):
    """
    Retrieve full chat history for a given session.
    """
    results = collection.get(ids=[session_id])

    chat_history = []
    if results and "documents" in results:
        for doc in results["documents"]:
            try:
                # Ensure each document is correctly parsed as JSON
                parsed_doc = json.loads(doc) if isinstance(doc, str) else doc
                chat_history.append(parsed_doc)
            except json.JSONDecodeError:
                chat_history.append({"user_query": "Unknown", "generated_query": "Invalid Data"})

    return chat_history

def clear_chat_history(session_id):
    """
    Clears chat history for a given session.
    """
    collection.delete(ids=[session_id])
