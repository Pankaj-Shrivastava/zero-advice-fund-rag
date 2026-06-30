import os
import sys
import logging
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.query.retriever import get_model, get_collection
from backend.query.pipeline import process_query

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the machine learning model and database connection
    logger.info("Initializing BGE Embedding Model and ChromaDB client...")
    try:
        get_model()
        get_collection()
        logger.info("Initialization complete. Ready to accept queries.")
    except Exception as e:
        logger.error(f"Failed to initialize models/DB: {e}")
    yield
    # Clean up resources if needed
    logger.info("Shutting down resources.")

app = FastAPI(
    title="Zero-Advice Fund RAG API",
    description="API for factual mutual fund querying",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str = Field(..., max_length=250, min_length=1, description="User's query")
    context_fund: Optional[str] = Field(default=None, description="The fund scheme from the previous turn context")

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/query")
async def query_endpoint(req: QueryRequest):
    try:
        if not req.question or not req.question.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty.")
            
        result = process_query(req.question.strip(), req.context_fund)
        
        # If pipeline returned an error structure
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result.get("answer", "Internal pipeline error"))
            
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the query.")

FUNDS_CACHE = []

def load_funds():
    global FUNDS_CACHE
    if not FUNDS_CACHE:
        try:
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../ingestion/parsed_data.json'))
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                unique_funds = {}
                for item in data:
                    scheme = item.get("scheme")
                    if scheme and scheme not in unique_funds:
                        category = item.get("category", "Mutual Fund")
                        unique_funds[scheme] = f"Equity • {category}" if "Cap" in category else category
                        
                FUNDS_CACHE = [{"name": k, "type": v} for k, v in unique_funds.items()]
            else:
                logger.error(f"parsed_data.json not found at {file_path}")
        except Exception as e:
            logger.error(f"Error loading funds: {e}")
    return FUNDS_CACHE

@app.get("/api/funds")
async def get_funds_endpoint():
    funds = load_funds()
    return {"funds": funds}
