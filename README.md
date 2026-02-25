# 🧠 AI-Powered Support Ticket Triage

A full-stack web application that **analyzes support tickets using local AI-style NLP logic**, stores results in a database, and displays them in a modern dashboard UI.

> **No external AI APIs are used.** All intelligence is provided by a deterministic, keyword-based heuristic engine running entirely on the server.

---

## 📁 Project Structure

```
ai-ticket-triage/
│
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── routes/              # API route definitions
│   │   ├── controllers/         # Request handling & response formatting
│   │   ├── services/            # Business logic orchestration
│   │   ├── analyzer/            # NLP / AI logic (local only)
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── config/              # Application settings
│   │   └── db/                  # Database engine & session
│   │
│   ├── tests/                   # Pytest unit tests
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/          # TicketForm, ResultCard, TicketHistory
│   │   ├── pages/               # Dashboard
│   │   ├── services/api.js      # Axios API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

| Tool     | Version |
|----------|---------|
| Docker   | ≥ 20.x  |
| Docker Compose | ≥ 2.x |

### Run with Docker (Recommended)

```bash
# Clone the repository
git clone <repo-url> ai-ticket-triage
cd ai-ticket-triage

# Build and start all services
docker-compose up --build
```

The app will be available at:

| Service  | URL                       |
|----------|---------------------------|
| Frontend | http://localhost:5173      |
| Backend  | http://localhost:8000      |
| API Docs | http://localhost:8000/docs |

### Run without Docker

#### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Run Tests

```bash
cd backend
pip install -r requirements.txt
pytest
```

---

## ⚙️ API Endpoints

### `POST /tickets/analyze`

Analyze a support ticket message.

**Request:**
```json
{
  "message": "my payment failed and this is urgent"
}
```

**Response (201):**
```json
{
  "id": 1,
  "category": "Billing",
  "priority": "P1",
  "urgency": true,
  "keywords": ["payment", "urgent"],
  "confidence": 0.87,
  "message": "my payment failed and this is urgent"
}
```

### `GET /tickets`

Return all tickets (newest first).

### `GET /health`

Health check endpoint.

---

## 🧠 AI / NLP Logic — Architecture

All analysis runs **locally** using a deterministic, rule-based NLP engine (no OpenAI, Claude, Gemini, or any external API).

### Category Classification

The engine scans the lowercased message for keyword matches:

| Category   | Keywords                                                    |
|------------|-------------------------------------------------------------|
| Billing    | payment, refund, invoice, charge, billing, money back, …    |
| Technical  | error, bug, crash, not working, broken, fail, timeout, …    |
| Account    | login, password, account locked, sign in, 2fa, …            |
| Feature    | request, feature, add option, enhancement, suggestion, …    |
| Other      | (no matches)                                                |

When multiple categories match, the one with the **most keyword hits** wins.

### Urgency Detection

The message is scanned for urgency signals:
`urgent`, `asap`, `immediately`, `down`, `critical`, `emergency`, `right now`, `escalate`, `blocked`

### Priority Assignment

| Level | Condition                          |
|-------|------------------------------------|
| P0    | "system down" or "security breach" |
| P1    | Urgency detected                  |
| P2    | Normal issue (Billing / Technical / Account) |
| P3    | Feature request or uncategorized   |

### Confidence Score

A heuristic score between **0.0–1.0** based on:
- Number of keyword matches (sigmoid-like scaling)
- Category specificity bonus (non-"Other" categories get +0.05)
- Baseline of 0.30 for zero-match inputs

### Keyword Extraction

All matched keywords (category + urgency) are returned as a deduplicated list.

---

## ⭐ Custom Rule — Refund / Money Back Override

> **Assignment Requirement:** If the message contains `"refund"` **OR** `"money back"`, the ticket is **always** classified as **Billing** with a priority of **at least P1**.

This custom rule is implemented as a **post-processing step** in the analysis pipeline (`_apply_custom_rules`). It runs **after** standard classification so it can override any conflicting result:

1. If `"refund"` or `"money back"` appears in the message:
   - `category` → forced to `"Billing"`
   - `priority` → upgraded to `"P1"` (unless already `"P0"`)
   - The trigger keyword is added to the extracted keywords list

**Why post-processing?** This ensures the custom rule always wins regardless of what other keywords are present, providing a reliable business-logic override without complicating the core classification algorithm.

---

## 🏗️ Architecture Explanation

The application follows a **clean layered architecture** inspired by production-grade service design:

```
Request → Route → Controller → Service → Analyzer
                                  ↓
                               Database
```

| Layer        | Responsibility |
|--------------|----------------|
| **Routes**   | Define HTTP endpoints and wire FastAPI dependencies |
| **Controllers** | Handle HTTP concerns: parse requests, format responses, error codes |
| **Services** | Orchestrate business logic: call analyzer, persist to DB |
| **Analyzer** | Pure NLP logic: classify, detect urgency, assign priority, compute confidence |
| **Models**   | SQLAlchemy ORM table definitions |
| **Schemas**  | Pydantic validation for API input/output |

This separation means each layer can be **tested, replaced, or extended independently**.

---

## 🎨 Frontend Architecture

| Component        | Purpose |
|------------------|---------|
| `Dashboard`      | Page-level container managing state & data fetching |
| `TicketForm`     | Textarea + submit button with loading spinner |
| `ResultCard`     | Color-coded analysis result display (category, priority, urgency, confidence, keywords) |
| `TicketHistory`  | Table of all previous tickets with loading, error, and empty states |
| `api.js`         | Axios client with `analyzeTicket()` and `fetchTickets()` |

Styling uses **Tailwind CSS** with a custom design system featuring:
- Dark glassmorphism (`glass-card` utility)
- Brand indigo palette
- Micro-animations (fade-in, slide-up)
- Google Fonts (Inter)

---

## 🐳 Docker Architecture

| Service    | Image        | Port  | Notes |
|------------|--------------|-------|-------|
| `backend`  | Python 3.12  | 8000  | SQLite DB stored in a Docker named volume |
| `frontend` | Node 20      | 5173  | Vite dev server with API proxy |

SQLite is persisted via the `db-data` named volume so data survives container restarts.

---

## 🧪 Testing

The test suite (`backend/tests/test_analyzer.py`) covers:

- **Category classification** — all five categories, case insensitivity, multi-keyword disambiguation
- **Urgency detection** — single keyword, multiple keywords, no urgency
- **Priority determination** — P0 through P3 scenarios
- **Confidence scoring** — baseline, scaling, category boost, bounds check
- **Custom rule** — refund forces Billing + P1, money-back forces Billing + P1
- **Full pipeline** — end-to-end `analyze_ticket()` integration tests

Run:
```bash
cd backend && pytest -v
```

---

## 🔍 Reflection

### Design Decisions

1. **Layered architecture** — Separating routes, controllers, services, and the analyzer keeps each concern isolated. The analyzer is a pure function module with zero HTTP or DB knowledge, making it trivially testable.

2. **Dataclass for AnalysisResult** — Using a Python `dataclass` instead of a Pydantic model internally keeps the analyzer free of framework coupling while still being easy to convert.

3. **Post-processing custom rules** — Running custom business rules as a final pipeline step (rather than embedding them in the classifier) makes them explicitly visible, easy to add/remove, and impossible to accidentally bypass.

4. **SQLite** — Chosen for zero-ops simplicity. The entire database is a single file, perfect for a self-contained demo. The Docker volume ensures persistence.

5. **Tailwind + Glassmorphism dark theme** — Modern, polished look with minimal CSS. The `glass-card` utility class avoids repetition across components.

### Tradeoffs

| Decision | Benefit | Cost |
|----------|---------|------|
| Rule-based NLP vs. ML model | Deterministic, explainable, zero dependencies | Cannot generalize to unseen phrasings |
| SQLite vs. PostgreSQL | Zero config, file-based | No concurrent writes, not for heavy production |
| Vite dev server in Docker | Hot reload during development | Not optimized for production (use `nginx` for prod) |
| Single-page app (no router) | Simplicity | Cannot scale to multi-page without adding a router |

### Limitations

- **Keyword coverage** — The engine only recognizes predefined keywords. Synonyms, typos, or novel phrasing will fall through to "Other."
- **No ML generalization** — Unlike a trained model, the engine cannot learn from new data.
- **Single-user SQLite** — Under high concurrency, SQLite may become a bottleneck.
- **No authentication** — The API is open; any client can submit or read tickets.

### Future Improvements

- **Add TF-IDF or a small local ML model** (e.g., scikit-learn Naive Bayes) for better generalization while staying fully local.
- **Swap SQLite for PostgreSQL** with connection pooling for production workloads.
- **Add authentication & RBAC** (e.g., OAuth2 + JWT) to protect endpoints.
- **Build production Docker images** with multi-stage builds and an `nginx` reverse proxy for the frontend.
- **Add WebSocket support** for real-time ticket updates on the dashboard.
- **Pagination & search** for the ticket history endpoint.
- **CI/CD pipeline** with GitHub Actions running lint, tests, and image builds automatically.

---

## 📄 License

This project is provided as an educational / assignment submission and is not licensed for commercial use.
