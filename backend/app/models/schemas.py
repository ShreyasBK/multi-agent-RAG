from pydantic import BaseModel, Field
from typing import Optional
import uuid


# ── Chat ──────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class SourceReference(BaseModel):
    doc_id: str
    content_preview: str
    similarity: float
    source_file: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceReference]
    confidence: float
    session_id: str
    query_type: str


# ── Documents ─────────────────────────────────────────────────────────────────

class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    status: str  # "queued" | "processing" | "ready" | "failed"
    message: str


class DocumentStatus(BaseModel):
    document_id: str
    filename: str
    status: str
    chunks_stored: Optional[int] = None
    error: Optional[str] = None
    created_at: str


class DocumentListResponse(BaseModel):
    documents: list[DocumentStatus]
    total: int
