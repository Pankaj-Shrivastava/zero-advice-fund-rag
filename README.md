# Zero-Advice Fund RAG

A factual, Retrieval-Augmented Generation (RAG) system for mutual fund information. This system provides factual answers about specific mutual funds based exclusively on official data, strictly refusing to provide investment advice or handle personal information (PII).

## Architecture Overview

The system is designed with four core layers:
1. **Ingestion Layer (Python/Playwright)**: Scrapes fund pages from Groww, parses HTML to clean text, chunks data, and stores embeddings in a local ChromaDB.
2. **Query Pipeline (Python)**: Uses a classifier (regex/heuristic) to filter PII and advisory questions. Factual questions trigger retrieval from ChromaDB, followed by response generation via Groq API (LLaMA 3).
3. **Frontend (React)**: A modern, responsive chat interface that displays factual information alongside clear disclaimers, citations, and update timestamps.
4. **Scheduler (GitHub Actions)**: Automates the ingestion pipeline to run daily at 10:30 AM IST to ensure fresh data.

For a detailed view, see [Architecture Decisions](docs/architecture.md) and [Decisions Log](docs/decisions.md).

## Supported Mutual Funds (Corpus)

Currently, the system is seeded with the following 10 funds from ICICI Prudential and HDFC Mutual Fund:
- ICICI Prudential Large Cap Fund
- ICICI Prudential Flexicap Fund
- ICICI Prudential Midcap Fund
- ICICI Prudential Indo Asia Equity Fund
- ICICI Prudential ELSS Tax Saver
- HDFC Mid-Cap Fund
- HDFC Small Cap Fund
- HDFC Silver ETF FoF
- HDFC ELSS Tax Saver Fund
- HDFC Large and Mid Cap Fund

## Project Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Groq API Key (Sign up at [Groq Console](https://console.groq.com/))

### 1. Backend Setup
```bash
# Navigate to project root
cd zero-advice-fund-rag

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
playwright install --with-deps chromium

# Set up environment variables
cp backend/.env.example backend/.env
# Edit backend/.env and add your GROQ_API_KEY
```

### 2. Run Data Ingestion (Optional)
If you want to pull the latest data manually:
```bash
python -m backend.scripts.run_ingestion
```
*(The repository already contains pre-indexed data in `backend/vectorstore` so this step is optional).*

### 3. Start the Backend API
```bash
uvicorn backend.api.main:app --reload --port 8000
```
The API will be available at http://localhost:8000.

### 4. Frontend Setup
Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```
The application will be available at http://localhost:5173.

## Testing
End-to-end tests are written with `pytest`. To run them:
```bash
# From project root (with venv activated)
pytest tests/e2e_test.py -v
```

## Known Limitations
- The bot cannot answer subjective questions (e.g., "Is this a good fund?") or provide comparative analysis ("Which fund is better?").
- The bot only knows about the 10 mutual funds listed above.
- Daily ingestion depends on GitHub Actions and may be delayed by a few minutes depending on runner availability.
