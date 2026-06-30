import os
import sys
from groq import Groq
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from groq import RateLimitError

# Hack to allow running as a script from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.config import GROQ_API_KEY
from backend.query.refusal import get_no_context_refusal

SYSTEM_PROMPT = """You are a facts-only mutual fund FAQ assistant. You MUST:
1. Answer ONLY from the provided context. Never fabricate information.
2. Keep your response to a MAXIMUM of 3 sentences.
3. Include EXACTLY ONE citation link (the source_url from the context).
4. End every response with: "Last updated from sources: <scraped_at date> <source_url>"
5. NEVER provide investment advice, opinions, or recommendations.
6. NEVER compare fund performance or calculate returns.
7. If the context does not contain the answer, say so honestly.

CONTEXT:
{retrieved_chunks}

USER QUESTION:
{user_query}
"""

_client = None

def get_groq_client():
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client

def format_chunks(chunks: list) -> str:
    formatted = []
    for i, c in enumerate(chunks):
        chunk_str = f"--- Chunk {i+1} ---\n"
        chunk_str += f"Source URL: {c.get('source_url', 'N/A')}\n"
        chunk_str += f"Scraped At: {c.get('scraped_at', 'N/A')}\n"
        chunk_str += f"Content:\n{c.get('text', '')}\n"
        formatted.append(chunk_str)
    return "\n".join(formatted)

@retry(
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(RateLimitError)
)
def call_groq_with_retry(client, messages, model="llama-3.3-70b-versatile"):
    return client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.1,
        max_tokens=300,
        top_p=0.9
    )

def generate_answer(query: str, chunks: list) -> dict:
    if not chunks:
        return get_no_context_refusal()
        
    formatted_context = format_chunks(chunks)
    prompt = SYSTEM_PROMPT.format(retrieved_chunks=formatted_context, user_query=query)
    
    client = get_groq_client()
    
    messages = [
        {"role": "system", "content": "You are a helpful mutual fund assistant."},
        {"role": "user", "content": prompt}
    ]
    
    try:
        response = call_groq_with_retry(client, messages)
        answer_text = response.choices[0].message.content.strip()
    except Exception as e:
        # Fallback if primary model fails
        try:
            response = call_groq_with_retry(client, messages, model="mixtral-8x7b-32768")
            answer_text = response.choices[0].message.content.strip()
        except Exception as fallback_e:
            answer_text = "I am currently experiencing high traffic and cannot generate an answer right now. Please try again later."
            return {
                "status": "error",
                "type": "error",
                "answer": answer_text,
                "source_url": None,
                "last_updated": None
            }
            
    # The prompt instructs LLM to provide source and last updated in the text
    # We also return it in the json schema for structured frontend use
    primary_chunk = chunks[0]
    
    return {
        "status": "success",
        "type": "factual",
        "answer": answer_text,
        "source_url": primary_chunk.get("source_url"),
        "last_updated": primary_chunk.get("scraped_at")
    }

if __name__ == "__main__":
    # Simple test
    test_chunks = [{
        "text": "The expense ratio of ICICI Prudential Large Cap Fund is 0.85%.",
        "source_url": "https://groww.in/mutual-funds/test",
        "scraped_at": "2026-06-30T00:00:00Z"
    }]
    res = generate_answer("What is the expense ratio?", test_chunks)
    print(res)
