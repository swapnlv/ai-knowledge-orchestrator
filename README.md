# AI Knowledge Orchestrator

The **AI Knowledge Orchestrator** is a backend service that ingests documents from multiple sources (PDFs, URLs, text, etc.), builds an intelligent knowledge base using embeddings and vector search, and exposes APIs for conversational querying using LLMs, LangChain, and LangGraph.

The primary goal of this project is **learning** modern AI + backend concepts end-to-end:
- FastAPI-based backend development
- RAG (Retrieval-Augmented Generation)
- LangChain (loaders, chains, agents, memory, vector stores)
- LangGraph (graph-based LLM workflows)
- Persistence (SQL database + vector store)
- Deployment-ready architecture (Docker, environment-based config)

---

## 🧠 High-Level Overview

### What This Service Does

- Accepts **documents** from different sources:
  - PDF uploads
  - Raw text / markdown
  - URLs or web articles
- Processes and **embeds** them into a **vector store** (e.g., Chroma/FAISS)
- Exposes APIs to:
  - Ask natural language questions over the ingested knowledge
  - Get source-aware answers (with references to original docs)
  - Maintain **conversational context** using memory
- Uses **LangChain** for:
  - Document loading, splitting, embedding, retrieval
  - RAG pipelines and basic agents
- Uses **LangGraph** for:
  - Defining more complex, graph-based workflows
  - Routing between tools (retriever, web search, etc.) based on query type

---

## 🎯 Learning Objectives

This project is structured as a learning playground for:

- **Backend Engineering**
  - FastAPI, RESTful design, request/response models
  - Modular, layered architecture (`api/`, `services/`, `llm/`, `models/`)
- **Databases**
  - SQLAlchemy ORM, migrations (Alembic)
  - Designing tables for users, documents, sessions
- **AI & LLMs**
  - LLM calls via OpenAI (or other providers)
  - Embeddings and vector similarity search
  - Retrieval-Augmented Generation (RAG)
- **LangChain**
  - Loaders, splitters, vector stores, retrievers, chains, agents, memory
- **LangGraph**
  - Node-based orchestration, branching logic, tool routing
- **DevOps Basics**
  - Dockerization, `.env` config, local orchestration via `docker-compose`

---

## 🧰 Tech Stack

- **Language**: Python 3.10+
- **Web Framework**: FastAPI
- **LLM Orchestration**: LangChain, LangGraph
- **LLM Provider**: OpenAI (default)
- **Vector Store**: Chroma and/or FAISS
- **Relational DB**: PostgreSQL (or SQLite for local dev)
- **ORM**: SQLAlchemy + Alembic
- **Cache / Optional**: Redis
- **Containerization**: Docker, docker-compose
- **Testing**: pytest

---

## 🗂️ Project Milestones

The project is divided into milestones so you can build and learn incrementally.

---

### ✅ Milestone 1 – Project Skeleton & Basic API

**Goal:** Set up the foundational backend structure and a minimal working FastAPI app.

**Key Outcomes:**
- Basic FastAPI application running
- Clear folder structure
- Healthcheck API endpoint

**What You Implement:**

- Project layout under `app/`:
  - `app/main.py` – creates FastAPI instance, mounts routers
  - `app/api/v1/endpoints/health.py` – `/health` or `/ping` route
  - `app/core/config.py` – loads environment variables (e.g., DB URL, API keys)
  - `app/models/db.py` – base SQLAlchemy setup
- `requirements.txt` with all core dependencies
- `.env.example` file with configuration variables

**Concepts Covered:**
- Modern Python project layout
- FastAPI basics (routes, startup, dependencies)
- Config management with environment variables

---

### ✅ Milestone 2 – Database & Document Metadata Layer

**Goal:** Add persistence for users, documents, and sessions using SQLAlchemy.

**Key Outcomes:**
- Relational database connected (PostgreSQL or SQLite)
- Basic models and migrations set up

**What You Implement:**

- Database engine & session:
  - `app/db/session.py` – `SessionLocal`, `get_db` dependency
- ORM models:
  - `app/models/document.py` – document metadata (title, source_type, path, created_at)
  - `app/models/session.py` – conversation/session info
  - (Optional) `app/models/user.py` – for multi-user support
- Pydantic schemas:
  - `app/schemas/document.py` – for document-related requests/responses
- Initial migrations using Alembic (optional early, but useful)

**Concepts Covered:**
- SQLAlchemy models & relationships
- ORM vs schemas (Pydantic)
- DB sessions and dependency injection in FastAPI

---

### ✅ Milestone 3 – Document Ingestion Pipeline (LangChain)

**Goal:** Ingest documents and prepare them for retrieval using LangChain.

**Key Outcomes:**
- API to upload/ingest documents
- Documents stored in DB and vector store

**What You Implement:**

- Document loaders:
  - `app/llm/loaders.py` – functions using LangChain loaders (e.g., `PyPDFLoader`, URL loader)
- Text splitting:
  - Configure `RecursiveCharacterTextSplitter`
- Embeddings + vector store:
  - `app/llm/embeddings.py` – construct embedding model (e.g., `OpenAIEmbeddings`)
  - `app/llm/vectorstore.py` – reuse or create a Chroma/FAISS instance
- Ingestion service:
  - `app/services/ingestion_service.py` – orchestrates:
    1. Load document
    2. Split into chunks
    3. Embed
    4. Store in vector store
    5. Save metadata to DB
- API endpoint:
  - `app/api/v1/endpoints/ingest.py` – e.g. `POST /v1/ingest/pdf`, `POST /v1/ingest/url`

**Concepts Covered:**
- LangChain document loaders and text splitters
- Embeddings and vector stores
- Designing a service layer to separate business logic from API layer

---

### ✅ Milestone 4 – Basic RAG Query API

**Goal:** Build an endpoint that lets users query the knowledge base using RAG.

**Key Outcomes:**
- User can ask questions and receive answers grounded in the ingested documents
- Responses include source metadata (citations)

**What You Implement:**

- A RAG chain:
  - `app/llm/chains/rag_chain.py` – defines a Retrieval-Augmented Generation pipeline using LangChain:
    - Use `VectorStoreRetriever`
    - Build a prompt template
    - Combine question + retrieved chunks
- Query service:
  - `app/services/query_service.py` – handles:
    1. Accept query and (optional) session id
    2. Retrieve relevant chunks
    3. Run LLM call
    4. Return answer + sources
- API endpoint:
  - `app/api/v1/endpoints/query.py` – e.g. `POST /v1/query`

**Concepts Covered:**
- Retrieval-Augmented Generation pattern
- LangChain retrievers and chains
- Prompt engineering basics (templates, context injection)
- Returning structured responses (answer + sources)

---

### ✅ Milestone 5 – Conversational Memory & Sessions

**Goal:** Introduce conversational context and support multi-turn chats.

**Key Outcomes:**
- Queries can be associated with sessions
- Conversation history influences responses

**What You Implement:**

- Memory integration:
  - Use LangChain’s `ConversationBufferMemory` or `ConversationSummaryMemory`
- Update models:
  - Store user queries and responses in `Session` / `Message` tables
- Extend RAG pipeline to:
  - Include relevant past exchanges for a given session
- API updates:
  - `POST /v1/query` accepts `session_id` and returns updated `session_id`

**Concepts Covered:**
- Conversation memory patterns
- Combining DB-stored history with LLM memory
- Session management in backend APIs

---

### ✅ Milestone 6 – Agent Tools & LangGraph Orchestration

**Goal:** Add more intelligence by letting the system decide *how* to answer a query (which tools or sources to use).

**Key Outcomes:**
- A simple LangChain agent with tools
- A LangGraph-based flow for complex workflows

**What You Implement:**

- Tools:
  - Web search tool (optional)
  - “Knowledge base query” tool (RAG)
  - (Optional) Python REPL tool
- Agent:
  - `app/llm/agents/orchestrator_agent.py` – uses tools to answer questions requiring reasoning/decisions
- LangGraph workflow:
  - `app/llm/graphs/knowledge_graph.py` – define nodes and edges:
    - classify query → decide:
      - use RAG
      - use web search
      - combine both
- API:
  - `POST /v1/agent/query` – interactive endpoint that uses the graph or agent

**Concepts Covered:**
- LangChain agents & tools
- LangGraph nodes, edges, and state
- Tool routing and decision-making based on query type

---

### ✅ Milestone 7 – Hardening, Testing & Deployment

**Goal:** Make the project production-friendly and testable.

**Key Outcomes:**
- Containerized app
- Basic tests
- Environment-based configuration

**What You Implement:**

- Testing:
  - `tests/test_health.py`, `tests/test_ingest.py`, `tests/test_query.py`
  - Mock LLM calls in tests
- Dockerization:
  - `Dockerfile` for FastAPI app
  - `docker-compose.yml` for app + DB + (optional) Redis
- Logging & error handling:
  - Structured logs (e.g., with `loguru` or standard `logging`)
  - Central error handler for API exceptions
- Readme & documentation:
  - Setup steps
  - Running locally
  - Example API calls

**Concepts Covered:**
- pytest & mocking
- Docker basics
- Logging, error handling, and observability
- How to explain and document a real-world AI backend project

---

## 🧪 Example Flow (End-to-End)

1. **Ingest phase**
   - Call `/v1/ingest/pdf` with a PDF file.
   - Backend:
     - Loads and splits the document
     - Generates embeddings
     - Stores chunks in vector store
     - Saves metadata in relational DB

2. **Query phase**
   - Call `/v1/query` with a natural language question.
   - Backend:
     - Retrieves relevant chunks from vector DB
     - Builds a prompt with context
     - Calls LLM via LangChain
     - Returns answer + sources

3. **Advanced agent/graph mode**
   - Call `/v1/agent/query` with a more complex query.
   - Backend:
     - Classifies query via LangGraph
     - Routes to appropriate tools (RAG, web search, etc.)
     - Combines results into a final answer

---

## 🧩 Future Enhancements

- User authentication & role-based access
- Rich UI (React / Next.js / Streamlit frontend)
- Advanced evaluation metrics for RAG
- Multi-agent collaboration using LangGraph
- Support for more LLM providers and local models
