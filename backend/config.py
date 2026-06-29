import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Embedding Model
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

# ChromaDB Config
CHROMA_DB_PATH = "backend/vectorstore"
COLLECTION_NAME = "fund_chunks"

# Chunking Config
CHUNK_SIZE = 400
CHUNK_OVERLAP = 50
