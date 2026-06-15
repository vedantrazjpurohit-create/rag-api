from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.engine import RagEngine

app = FastAPI(title="rag-api", version="0.1.0")
engine = RagEngine()


class QueryRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=5, ge=1, le=20)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)) -> dict:
    raw = await file.read()
    text = raw.decode("utf-8", errors="ignore")
    count = engine.ingest_text(text, source=file.filename or "upload")
    return {"chunks_indexed": count, "source": file.filename}


@app.post("/query")
def query(payload: QueryRequest):
    result = engine.query(payload.question, top_k=payload.top_k)
    body = {
        "answer": result.answer,
        "contexts": result.contexts,
        "timing_ms": {
            "retrieve": round(result.retrieve_ms, 2),
            "total": round(result.total_ms, 2),
        },
    }
    return JSONResponse(
        content=body,
        headers={
            "X-Retrieve-Ms": str(round(result.retrieve_ms, 2)),
            "X-Total-Ms": str(round(result.total_ms, 2)),
        },
    )