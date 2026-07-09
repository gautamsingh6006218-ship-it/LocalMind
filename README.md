# LocalMind

Fully offline personal assistant: RAG over your own files (PDFs, notes, emails export) answered by a locally-running Llama model. No API calls to OpenAI/Anthropic.

## Architecture

- `backend/` — FastAPI service: ingestion, embeddings (Qwen3), retrieval (Qdrant), generation (Ollama), observability (Langfuse + RAGAS)
- `frontend/` — React + TypeScript chat UI
- `infra/` — Docker Compose: Ollama, Qdrant, Postgres, ClickHouse, Redis, MinIO, Langfuse

## Prerequisites

- Docker Desktop
- Python 3
- Node.js + npm

## First-time setup

1. Start the infra stack (Ollama, Qdrant, Langfuse, etc.):
   ```
   cd infra
   docker compose up -d
   ```

2. Pull the required Ollama models (only needed once, downloads several GB):
   ```
   docker exec infra-ollama-1 ollama pull llama3.2:3b
   docker exec infra-ollama-1 ollama pull qwen2.5:7b
   ```

3. Set up the backend:
   ```
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. Create `backend/.env` with your Langfuse API keys (log in at http://localhost:3000 first, generate keys under Settings > API Keys):
   ```
   LANGFUSE_PUBLIC_KEY=pk-lf-your-key
   LANGFUSE_SECRET_KEY=sk-lf-your-key
   LANGFUSE_HOST=http://localhost:3000
   ```

5. Set up the frontend:
   ```
   cd frontend
   npm install
   ```

6. Ingest your documents into Qdrant (run once, or again whenever you add new files):
   ```
   cd backend
   python -m app.ingestion.ingest
   ```

## Running it day-to-day

1. Make sure the infra stack is up (only needs restarting if it was stopped):
   ```
   docker compose -f infra/docker-compose.yml up -d
   ```
2. Start the backend and frontend together with one command:
   ```
   ./dev.sh
   ```
   Ctrl+C stops both.

## URLs

- Frontend (chat UI): http://localhost:5173
- Backend API: http://localhost:8000
- Langfuse dashboard (traces + eval scores): http://localhost:3000

## Running tests

```
cd backend
pytest -v
```

## Configuration

All tunable settings (model names, judge model, sample rate for RAGAS scoring, etc.) live in `backend/app/config.py`, and can be overridden via `backend/.env` without touching code. See that file for the full list.

## Ports used by this project

| Port | Service |
|---|---|
| 5173 | Frontend (React dev server) |
| 8000 | Backend (FastAPI) |
| 3000 | Langfuse web dashboard |
| 3030 | Langfuse worker |
| 6333 | Qdrant |
| 11434 | Ollama |
| 5432 | Postgres |
| 6379 | Redis |
| 8123, 9000 | ClickHouse |
| 9090, 9091 | MinIO |

**Stop the whole infra stack** (all 8 containers/ports above at once, data is preserved):
```
docker compose -f infra/docker-compose.yml stop
```
**Start it back up:**
```
docker compose -f infra/docker-compose.yml up -d
```

## Troubleshooting

**Check what's running on a port** (swap the number for any port above):
```
lsof -i :3000
```

**Stop whatever's using it:**
```
kill -9 $(lsof -t -i:3000)
```

**Check which Ollama model is currently loaded in memory:**
```
docker exec infra-ollama-1 ollama ps
```

**Check Docker's resource usage** (useful if requests are running slower than expected):
```
docker stats infra-ollama-1 --no-stream
```
