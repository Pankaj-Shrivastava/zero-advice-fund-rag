# Project Context — Zero-Advice Fund RAG

## What Is This Project?

A **facts-only FAQ assistant** for mutual fund schemes, built using a **Retrieval-Augmented Generation (RAG)** pipeline. The product context is modeled after **Groww** — a retail investment platform. The assistant answers objective, verifiable queries about mutual funds by retrieving information exclusively from **Groww mutual fund pages** — no PDFs, no external AMC/AMFI/SEBI documents.

> **Core principle:** Accuracy over intelligence. No investment advice, opinions, or recommendations — ever.

---

## Who Is It For?

| Audience | Use Case |
|---|---|
| **Retail investors** | Comparing mutual fund schemes using factual data (expense ratios, exit loads, SIP minimums, etc.) |
| **Customer support / content teams** | Handling repetitive, factual mutual fund queries at scale |

---

## Corpus & Data Sources

### Selected AMCs & Schemes

The RAG chatbot covers **10 mutual fund schemes** across **2 AMCs** — **ICICI Prudential** and **HDFC** — with diversity across large-cap, mid-cap, small-cap, flexi-cap, ELSS, and thematic categories.

#### ICICI Prudential Mutual Fund (5 schemes)

| # | Scheme | Category | Groww URL |
|---|--------|----------|-----------|
| 1 | ICICI Prudential Large Cap Fund – Direct Growth | Large Cap | [Link](https://groww.in/mutual-funds/icici-prudential-large-cap-fund-direct-growth) |
| 2 | ICICI Prudential Flexicap Fund – Direct Growth | Flexi Cap | [Link](https://groww.in/mutual-funds/icici-prudential-flexicap-fund-direct-growth) |
| 3 | ICICI Prudential Midcap Fund – Direct Growth | Mid Cap | [Link](https://groww.in/mutual-funds/icici-prudential-midcap-fund-direct-growth) |
| 4 | ICICI Prudential Indo Asia Equity Fund – Direct Growth | Thematic / International | [Link](https://groww.in/mutual-funds/icici-prudential-indo-asia-equity-fund-direct-growth) |
| 5 | ICICI Prudential ELSS Tax Saver – Direct Plan Growth | ELSS (Tax Saver) | [Link](https://groww.in/mutual-funds/icici-prudential-elss-tax-saver-direct-plan-growth) |

#### HDFC Mutual Fund (5 schemes)

| # | Scheme | Category | Groww URL |
|---|--------|----------|-----------|
| 6 | HDFC Mid-Cap Fund – Direct Growth | Mid Cap | [Link](https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth) |
| 7 | HDFC Small Cap Fund – Direct Growth | Small Cap | [Link](https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth) |
| 8 | HDFC Silver ETF FoF – Direct Growth | Commodity / Thematic | [Link](https://groww.in/mutual-funds/hdfc-silver-etf-fof-direct-growth) |
| 9 | HDFC ELSS Tax Saver Fund – Direct Plan Growth | ELSS (Tax Saver) | [Link](https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth) |
| 10 | HDFC Large and Mid Cap Fund – Direct Growth | Large & Mid Cap | [Link](https://groww.in/mutual-funds/hdfc-large-and-mid-cap-fund-direct-growth) |

### Corpus Definition

The **10 Groww fund page URLs** listed above are the **sole data source** for the RAG pipeline. Each page contains scheme-level facts such as expense ratio, exit load, minimum SIP amount, riskometer category, benchmark index, and fund manager details. No PDFs, no AMC factsheets, no AMFI/SEBI documents are ingested.

### Allowed Sources

- **Only** the 10 Groww mutual fund URLs listed above.
- **No** PDFs, AMC documents, third-party blogs, or aggregator sites.

---

## What the Assistant Must Do

### Answer Facts-Only Queries

Example query types:

- Expense ratio of a scheme
- Exit load details
- Minimum SIP amount
- ELSS lock-in period
- Riskometer classification
- Benchmark index
- Process to download statements or capital gains reports

### Response Format Rules

1. **Max 3 sentences** per response.
2. **Exactly one citation link** per response.
3. Every response must include a footer:
   ```
   Last updated from sources: <date> <source_link>
   ```

### Refusal Handling

The assistant must **refuse** non-factual or advisory queries (e.g., *"Should I invest in this fund?"*, *"Which fund is better?"*).

Refusal responses should:

- Be polite and clearly worded.
- Reinforce the facts-only limitation.
- Provide a relevant educational link (e.g., AMFI or SEBI resource).

---

## Constraints

### Privacy & Security

The system must **never** collect, store, or process:

- PAN or Aadhaar numbers
- Account numbers
- OTPs
- Email addresses or phone numbers
- Any PII

### Content Restrictions

- No investment advice or recommendations.
- No performance comparisons or return calculations.
- For performance-related queries → link to the official factsheet only.

### Transparency

- Responses must be short, factual, and verifiable.
- Every answer must include a source link and last-updated date.

---

## User Interface (React-Based)

The UI should include:

- A **welcome message** with a very short product introduction.
- **Three example questions** to guide users.
- A **visible disclaimer**, clearly evident to the user:
  > *"Facts-only. No investment advice."*

---

## Architecture

**RAG (Retrieval-Augmented Generation)** approach:

1. **Ingest** — Scrape and index the 10 Groww fund pages.
2. **Retrieve** — On each user query, retrieve the most relevant chunks from the indexed corpus.
3. **Generate** — Use an LLM to compose a concise, source-backed answer from the retrieved context.

---

## Tech Stack (All Free / Open-Source)

| Layer | Technology | Cost | Notes |
|-------|-----------|------|-------|
| **LLM** | **Groq** (e.g., Llama 3 / Mixtral via Groq API) | Free tier | Fast inference; free API with rate limits |
| **Embedding** | **BGE** (`BAAI/bge-small-en-v1.5` or `bge-base-en-v1.5`) | Free | Open-source; runs locally via `sentence-transformers` |
| **Vector Store** | **ChromaDB** | Free | Lightweight, local, persistent |
| **Scraping** | Python (`requests` + `BeautifulSoup` / `Playwright`) | Free | Open-source |
| **Backend API** | Python (FastAPI) | Free | Open-source |
| **Frontend** | React (Vite) | Free | Open-source |
| **Orchestration** | LangChain (optional) | Free | Open-source |

---

## Success Criteria

- ✅ Accurate retrieval of factual mutual fund information.
- ✅ Strict adherence to facts-only responses.
- ✅ Consistent inclusion of valid source citations.
- ✅ Proper refusal of advisory queries.
- ✅ Clean, minimal, and user-friendly interface.

---

## Expected Deliverables

| Deliverable | Details |
|---|---|
| **README** | Setup instructions, selected AMC & schemes, architecture overview, known limitations |
| **Disclaimer snippet** | *"Facts-only. No investment advice."* |
| **Working RAG assistant** | Backend pipeline + React UI |

---

*Source: [problemStatement.txt](file:///c:/Users/panka/Documents/Pankaj_CodeSpace/AI_Projects/zero-advice-fund-rag/docs/problemStatement.txt)*
