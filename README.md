# hello-langchain

A RAG (Retrieval-Augmented Generation) API built with FastAPI, LangChain, pgvector, and Ollama. Upload PDF documents and ask questions about their content.

## How it works

```
Upload PDF → parse → chunk → embed (HuggingFace) → store in pgvector
Ask question → embed query → cosine similarity search → top-3 chunks → Ollama LLM → answer
```

1. **PDF upload** — the file is parsed with PyMuPDF, split into overlapping text chunks, and each chunk is embedded with a HuggingFace sentence-transformer model running locally (CUDA or CPU).
2. **Embeddings storage** — chunks and their 1024-dim vectors are persisted in PostgreSQL with the `pgvector` extension. An HNSW index (`vector_cosine_ops`) is used for fast approximate nearest-neighbour search.
3. **Question answering** — the query is embedded the same way, the 3 most similar chunks are retrieved, and the assembled context is sent to an Ollama LLM via a strict prompt that prevents hallucination outside the provided context.

## Stack

| Component | Technology |
|-----------|-----------|
| API | FastAPI |
| LLM | Ollama (configurable model) |
| Embeddings | HuggingFace `sentence-transformers` |
| Vector DB | PostgreSQL + pgvector (HNSW index) |
| ORM | SQLAlchemy 2.0 async |
| Migrations | Alembic |
| Runtime | Python 3.13, uv |

## Prerequisites

- Docker + Docker Compose with the Compose plugin
- NVIDIA GPU + drivers (for CUDA embeddings) — or set `MY_APP__AI__EMBEDDING__HF__DEVICE=cpu`
- Ollama running on the host at port `12434` (or adjust `MY_APP__AI__LLM__OLLAMA__BASE_URL`)
- A HuggingFace token if the embedding model is gated

## Quick start

**1. Clone and configure**

```bash
git clone <repo-url>
cd hello-langchain
cp .env.example .env
# edit .env — set at minimum HF_TOKEN and verify model names
```

**2. Start**

```bash
docker compose up
```

This starts three services in order:
- `db` — PostgreSQL with pgvector, waits until healthy
- `migrate` — runs `alembic upgrade head`, then exits
- `app` — FastAPI on port `8000`, waits for migrations to complete

**Development mode** (live reload on `./src` changes):

```bash
docker compose up --watch
```

## Configuration

Copy `.env.example` to `.env` and adjust:

```env
MY_APP__DB__HOST=db
MY_APP__DB__NAME=db
MY_APP__DB__USER=user
MY_APP__DB__PASSWORD=password

# Ollama — host.docker.internal resolves to the Docker host on both Linux and macOS
MY_APP__AI__LLM__OLLAMA__MODEL=ai/gemma4
MY_APP__AI__LLM__OLLAMA__BASE_URL=http://host.docker.internal:12434

# HuggingFace embedding model
MY_APP__AI__EMBEDDING__HF__MODEL=ai-forever/ru-en-RoSBERTa
MY_APP__AI__EMBEDDING__HF__DEVICE=cuda   # or cpu

HF_TOKEN=hf_...
```

All variables are prefixed with `MY_APP__` and use `__` as the nested delimiter.

## API

Interactive docs available at [http://localhost:8000/docs](http://localhost:8000/docs).

### Upload a PDF

```bash
curl -X POST http://localhost:8000/rag/upload-pdf \
  -F "file=@document.pdf"
```

### Ask a question

```bash
curl "http://localhost:8000/rag/ask-pdf?q=What+is+the+document+about"
```

Returns a plain-text answer grounded in the uploaded documents.
