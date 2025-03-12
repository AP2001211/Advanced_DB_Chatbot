import chromadb

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Create or load a collection for storing session context
collection = chroma_client.get_or_create_collection(name="chat_context")

def store_context(session_id, user_query, generated_query):
    """
    Store user query and generated query as context in ChromaDB.
    """
    collection.add(
        ids=[session_id], 
        documents=[{"user_query": user_query, "generated_query": generated_query}]
    )

def retrieve_context(session_id):
    """
    Retrieve context for a given session.
    """
    results = collection.get(ids=[session_id])
    if results['documents']:
        return results['documents'][0]  # Return the stored context
    return None
