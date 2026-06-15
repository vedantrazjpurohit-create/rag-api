# rag-api

Minimal FastAPI service around local retrieval — built to expose the same metrics I care about in `rag-eval-bench`, but over HTTP.

No LangChain magic. Upload a doc, ask a question, get an answer + timing breakdown in response headers.

## Why

Notebooks don't prove deployability. I wanted a single endpoint I could hit from a frontend, curl, or a robot's edge node without rewriting the pipeline.

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Endpoints

- `POST /ingest` — upload `.md` / `.txt`, chunks + indexes automatically
- `POST /query` — `{ "question": "...", "top_k": 5 }` → answer + retrieved snippets
- `GET /health` — liveness

## Example

```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What chunk size worked better?\"}"
```

Example response body:

```json
{
  "answer": "Top match suggests: ...",
  "contexts": [{"text": "...", "source": "upload", "score": 0.91}],
  "timing_ms": {"retrieve": 14.2, "total": 15.1}
}
```

Response headers include `X-Retrieve-Ms` and `X-Total-Ms` for quick profiling.

## Stack

FastAPI · ChromaDB · sentence-transformers · Python 3.11+