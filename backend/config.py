import os

class Config:
    # OpenAI API Key (To be set dynamically from frontend)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # MySQL Database Configuration (To be set dynamically from frontend)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "")

    # ChromaDB Storage Path
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
