import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM Configuration
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4.1-nano")  # Default OpenAI model
    
    # Embedding Configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")  # Default OpenAI embedding model
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Vector Database Configuration
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_db")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Knowledge Base Configuration
    KNOWLEDGE_FOLDER = os.getenv("KNOWLEDGE_FOLDER", "./knowledge_files")
    
    # Agent Configuration
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # User Profile Configuration
    DEFAULT_USER_PROFILE = {
        "expertise_level": "intermediate",
        "background": "technical",
        "preferred_detail_level": "moderate"
    } 