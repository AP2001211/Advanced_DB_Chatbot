# Advanced_DB_Chatbot
Natural Language to SQL Chatbot

**Overview of the Project**

This is a natural language to SQL chatbot that allows users to query a database using plain English. It generates SQL queries using LangChain and maintains session context using ChromaDB.

**Key Components**
- **LangChain** for Prompting & SQL Generation
- **ChromaDB** for Context Awareness
- **Frontend** with Streamlit
- **Backend** with Flask
- **Database Connectivity**

**How LangChain is Used**

- **Prompting with LangChain**  
    LangChain acts as an interface between user queries and the LLM (Large Language Model). The prompt template ensures that SQL queries are generated in a structured way. It extracts schema from the database and instructs the LLM to generate valid SQL.

- **LangChain Flow:**
  -User enters a query.
  -LangChain injects schema into a structured prompt.
  -LLM generates an SQL query.
  -The query is returned to the frontend.

### Backend Requirements (Flask)

To run the backend, you will need the following dependencies:

1. **Flask**: A lightweight web framework to handle HTTP requests.
2. **LangChain**: Used for structuring prompts and generating SQL queries.
3. **ChromaDB**: A vector database used to store session context and chat history.
4. **SQLAlchemy**: ORM for handling database connections.

You can install the backend requirements using the following command:

```bash
cd backend
pip install -r requirements.txt
```
Frontend Requirements (Streamlit)
To run the frontend, you will need the following dependencies:

Streamlit: A framework for creating interactive web applications.
Requests: To communicate with the backend API.
ChromaDB: For fetching and displaying context from the database.
You can install the frontend requirements using the following command:

```bash
cd frontend
pip install -r requirements.txt
```


How to Run the Project
1. Set up the Backend
To set up and run the backend:

- Navigate to the backend folder
- Install the required dependencies
- Run the Flask application

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The backend should now be running at http://localhost:5000. This will handle API requests from the frontend and process SQL queries using LangChain.

2. Set up the Frontend
To set up and run the frontend:

- Navigate to the frontend folder
- Install the required dependencies
- Run the Streamlit application

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
The frontend will now be running at http://localhost:8501, where you can interact with the chatbot and input natural language queries.

