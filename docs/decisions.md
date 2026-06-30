# Decision Log — Zero-Advice Fund RAG

> A chronological record of key architectural, design, and implementation decisions made during development.

---

## Decision Format

Each entry follows this structure:

| Field | Description |
|-------|-------------|
| **ID** | Sequential identifier (DEC-001, DEC-002, ...) |
| **Date** | When the decision was made |
| **Context** | What problem or question prompted the decision |
| **Decision** | What was decided |
| **Rationale** | Why this option was chosen over alternatives |
| **Impact** | Files, components, or phases affected |

---

## DEC-001 — Use BGE-small over BGE-base for Embeddings

| Field | Detail |
|-------|--------|
| **Date** | 2026-06-29 |
| **Context** | Needed to select an embedding model for the vector store. `bge-small-en-v1.5` (384d) and `bge-base-en-v1.5` (768d) were both viable. |
| **Decision** | Use `BAAI/bge-small-en-v1.5`. |
| **Rationale** | Smaller model loads faster, uses less memory, and produces embeddings quickly on CPU. The accuracy trade-off is acceptable for a 10-fund corpus with well-structured chunks. |
| **Impact** | `backend/config.py`, `backend/query/retriever.py`, `backend/ingestion/embedder.py` |

---

## DEC-002 — Keyword-Based Query Classifier (No LLM Call)

| Field | Detail |
|-------|--------|
| **Date** | 2026-06-29 |
| **Context** | Query classification could use keyword rules, an LLM call, or a hybrid approach. |
| **Decision** | Use a pure keyword/regex-based classifier. |
| **Rationale** | Avoids consuming Groq rate limits (30 RPM) on classification. Keyword patterns reliably catch advisory intent ("should I", "recommend", "better") and PII patterns (PAN, Aadhaar, email, phone). Keeps latency near zero for refused queries. |
| **Impact** | `backend/query/classifier.py` |

---

## DEC-003 — Groq Rate Limit Guardrails

| Field | Detail |
|-------|--------|
| **Date** | 2026-06-30 |
| **Context** | Groq free tier has strict limits: 30 RPM, 1K RPD, 12K TPM, 100K TPD for `llama-3.3-70b-versatile`. |
| **Decision** | Add retry-with-backoff (3 retries, exponential delay), token budgeting (cap context to ~2000 tokens, response to ~500), and skip LLM calls entirely for advisory/PII queries. |
| **Rationale** | Maximizes the usable throughput within the free tier. Refusing advisory queries without hitting Groq saves RPM for actual factual queries. Token budgeting prevents a single query from consuming excessive TPM. |
| **Impact** | `backend/query/generator.py`, `backend/query/pipeline.py` |

---

## DEC-004 — Single-File Component Architecture for Frontend

| Field | Detail |
|-------|--------|
| **Date** | 2026-06-30 |
| **Context** | The implementation plan proposed separate component files (`ChatWindow.jsx`, `MessageBubble.jsx`, etc.). |
| **Decision** | Consolidate all components into a single `App.jsx` file. |
| **Rationale** | The app is small enough that splitting into many files adds navigation overhead without meaningful reusability gains. All components (Header, SearchBar, ResultFeed, etc.) are tightly coupled to the single-page chat flow. Easier to iterate during rapid development. |
| **Impact** | `frontend/src/App.jsx` |

---

## DEC-005 — Chatbot-Style Layout with Sticky Search Bar

| Field | Detail |
|-------|--------|
| **Date** | 2026-06-30 |
| **Context** | The initial UI placed the search bar in the middle of the page (Google-style search). User feedback indicated the search bar should behave like a chatbot input, always visible at the bottom. |
| **Decision** | Pin the search bar to the bottom of the viewport. Make the message feed scrollable with hidden scrollbars. Auto-scroll to the latest message. |
| **Rationale** | Users expect a chat-like experience when interacting conversationally. A sticky bottom input matches the mental model of messaging apps. Hidden scrollbars maintain a clean aesthetic while preserving scroll functionality. |
| **Impact** | `frontend/src/App.jsx`, `frontend/src/index.css` |

---

## DEC-006 — Conditional "New Chat" Button Visibility

| Field | Detail |
|-------|--------|
| **Date** | 2026-06-30 |
| **Context** | A "New Chat" button was always visible in the header, even on the initial home page where no conversation had started. |
| **Decision** | Only show the "New Chat" button when `messages.length > 0` (i.e., after the user has started a conversation). |
| **Rationale** | On the home page, there is no chat to reset — showing the button is misleading. Appearing it only during an active conversation gives it clear, intuitive purpose. |
| **Impact** | `frontend/src/App.jsx` |

---

## DEC-007 — Dynamic Supported Funds via Backend API

| Field | Detail |
|-------|--------|
| **Date** | 2026-06-30 |
| **Context** | The "Supported Funds" view was initially hardcoded in the React frontend with a static list of 5 funds. |
| **Decision** | Create a `GET /api/funds` backend endpoint that reads `parsed_data.json`, extracts unique scheme names and categories, caches them in memory, and returns them to the frontend. |
| **Rationale** | If new funds are scraped and added to `parsed_data.json`, the frontend automatically reflects them without any code change. This keeps the source of truth in one place (the ingested data) and avoids frontend-backend drift. |
| **Impact** | `backend/api/main.py` (new endpoint), `frontend/src/App.jsx` (dynamic fetch) |

---

## DEC-008 — Persistent Disclaimer Banner

| Field | Detail |
|-------|--------|
| **Date** | 2026-06-30 |
| **Context** | The "Facts-only. No investment advice." disclaimer was originally inside the WelcomeHero component, which disappears once a conversation starts. |
| **Decision** | Extract the disclaimer into its own `DisclaimerBanner` component rendered directly below the header, always visible regardless of which view is active. |
| **Rationale** | Regulatory and compliance best practice — the user must always see the disclaimer, especially during an active conversation when factual answers are being displayed. Prevents any ambiguity about the nature of the information provided. |
| **Impact** | `frontend/src/App.jsx`, `frontend/src/index.css` |

---

## DEC-009 — Vanilla CSS over Tailwind/CSS Frameworks

| Field | Detail |
|-------|--------|
| **Date** | 2026-06-30 |
| **Context** | Needed to choose a styling approach for the frontend. |
| **Decision** | Use Vanilla CSS with CSS Custom Properties (variables) for the design system. |
| **Rationale** | No build tool dependency, full control over every style, smaller bundle size, and the app's scope (single page, ~10 components) doesn't justify a framework. CSS variables provide theming capability if needed later. |
| **Impact** | `frontend/src/index.css` |

---

## DEC-010 — In-Memory Chat State (No Persistence)

| Field | Detail |
|-------|--------|
| **Date** | 2026-06-30 |
| **Context** | User requested that chat history be available during a session but start fresh on a new tab. |
| **Decision** | Keep all chat messages in React `useState` only — no `localStorage`, no `sessionStorage`. |
| **Rationale** | Simplest implementation that meets the requirement exactly. Opening a new tab/refreshing creates a blank state. No risk of stale or leaked data between sessions. |
| **Impact** | `frontend/src/App.jsx` |

---

## DEC-011 — Remove Duplicate Citation from LLM Answer Text

| Field | Detail |
|-------|--------|
| **Date** | 2026-06-30 |
| **Context** | The LLM system prompt instructed the model to embed a citation URL and "Last updated from sources: &lt;date&gt; &lt;url&gt;" directly inside the answer text. However, the frontend card footer already renders `last_updated` and `source_url` from the structured JSON response fields, causing ugly duplication. |
| **Decision** | Replace prompt rules 3 ("Include EXACTLY ONE citation link") and 4 ("End every response with: Last updated from sources…") with a single rule: "Do NOT include source URLs, dates, or citation footers in your answer — these are displayed separately by the UI." |
| **Rationale** | The structured JSON response already carries `source_url` and `last_updated` as first-class fields. The card footer renders them beautifully with icons. Embedding them again in the answer text was redundant, cluttered, and broke the clean card layout. |
| **Impact** | `backend/query/generator.py` (system prompt) |

---

## DEC-012 — Use Corpus-Specific Example Questions

| Field | Detail |
|-------|--------|
| **Date** | 2026-06-30 |
| **Context** | The 3 suggestion chips on the welcome screen showed generic questions ("What is an Expense Ratio?", "Explain Exit Load", "How do dividends work?") that were not specific to any fund in our corpus. These generic questions often returned "context not found" responses, giving a poor first impression. |
| **Decision** | Replace with fund-specific questions that directly map to data in `parsed_data.json`: (1) "What is the expense ratio of ICICI Prudential Large Cap Fund?" (2) "What is the exit load for HDFC Mid-Cap Opportunities Fund?" (3) "What are the top holdings of ICICI Prudential Flexicap Fund?" |
| **Rationale** | These questions target specific sections (`expense_ratio`, `exit_load`, `holdings`) of specific funds in our corpus, guaranteeing a high-quality factual response on the very first click. This showcases the system's capability immediately and builds user confidence. |
| **Impact** | `frontend/src/App.jsx` (SuggestionChips component) |

---

## DEC-013 — Cache Supported Funds in Browser (sessionStorage + 24h TTL)

| Field | Detail |
|-------|--------|
| **Date** | 2026-06-30 |
| **Context** | The Supported Funds view fetches from `GET /api/funds` every time the user toggles to it. The fund list rarely changes (only after a new ingestion run), so hitting the backend repeatedly is wasteful. |
| **Decision** | Cache the funds list in `sessionStorage` with a 24-hour TTL. On load, check cache first; only call the API if cache is missing or expired. |
| **Rationale** | `sessionStorage` is scoped to the browser tab — it naturally clears when the tab/browser closes (meeting the "until browser is open" requirement). The 24-hour TTL ensures that even a long-lived tab eventually picks up newly ingested funds. No risk of serving stale data across separate sessions since `sessionStorage` doesn't persist across tabs or restarts. |
| **Impact** | `frontend/src/App.jsx` (SupportedFunds component) |
