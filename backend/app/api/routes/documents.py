import uuid
import tempfile
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from backend.app.models.schemas import DocumentListResponse, DocumentStatus, DocumentUploadResponse
from backend.app.api.middleware.auth import verify_supabase_jwt
from backend.app.services.supabase import get_supabase
from backend.app.ingestion.pipeline import ingest_document

ALLOWED_TYPES = {".pdf", ".docx", ".pptx"}

router = APIRouter()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    token: dict = Depends(verify_supabase_jwt),
) -> DocumentUploadResponse:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {suffix}")

    document_id = str(uuid.uuid4())
    user_id = token.get("sub", "")
    content = await file.read()

    # Save to Supabase Storage, then queue Celery task
    client = get_supabase()
    storage_path = f"{user_id}/{document_id}{suffix}"
    client.storage.from_("documents").upload(storage_path, content)

    # Record in DB
    client.table("document_jobs").insert({
        "id": document_id,
        "user_id": user_id,
        "filename": file.filename,
        "storage_path": storage_path,
        "status": "queued",
    }).execute()

    # Dispatch Celery task
    ingest_document.delay(document_id, storage_path, suffix, user_id)

    return DocumentUploadResponse(
        document_id=document_id,
        filename=file.filename or "",
        status="queued",
        message="Document queued for processing",
    )


@router.get("/", response_model=DocumentListResponse)
def list_documents(token: dict = Depends(verify_supabase_jwt)) -> DocumentListResponse:
    user_id = token.get("sub", "")
    client = get_supabase()
    response = (
        client.table("document_jobs")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    docs = [DocumentStatus(**d) for d in (response.data or [])]
    return DocumentListResponse(documents=docs, total=len(docs))


@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    token: dict = Depends(verify_supabase_jwt),
) -> dict:
    user_id = token.get("sub", "")
    client = get_supabase()

    # Verify ownership
    row = (
        client.table("document_jobs")
        .select("storage_path")
        .eq("id", document_id)
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    if not row.data:
        raise HTTPException(status_code=404, detail="Document not found")

    client.storage.from_("documents").remove([row.data["storage_path"]])
    client.table("chunks").delete().eq("document_id", document_id).execute()
    client.table("document_jobs").delete().eq("id", document_id).execute()

    return {"deleted": document_id}
