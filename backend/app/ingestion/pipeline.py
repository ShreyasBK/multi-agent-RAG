from backend.worker.celery_app import celery
from backend.app.ingestion.parsers.pdf_parser import parse_pdf
from backend.app.ingestion.parsers.docx_parser import parse_docx
from backend.app.ingestion.parsers.pptx_parser import parse_pptx
from backend.app.ingestion.chunker import chunk_documents
from backend.app.ingestion.embedder import embed_and_store
from backend.app.services.supabase import get_supabase
import tempfile
from pathlib import Path


PARSERS = {".pdf": parse_pdf, ".docx": parse_docx, ".pptx": parse_pptx}


@celery.task(bind=True, max_retries=3)
def ingest_document(self, document_id: str, storage_path: str, suffix: str, user_id: str):
    client = get_supabase()

    def update_status(status: str, error: str | None = None):
        client.table("document_jobs").update(
            {"status": status, "error": error}
        ).eq("id", document_id).execute()

    try:
        update_status("processing")

        # Download from Supabase Storage
        file_bytes = client.storage.from_("documents").download(storage_path)

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = Path(tmp.name)

        # Parse
        parser = PARSERS.get(suffix)
        if not parser:
            raise ValueError(f"No parser for {suffix}")
        docs = parser(tmp_path)
        tmp_path.unlink(missing_ok=True)

        # Chunk + embed + store
        chunks = chunk_documents(docs)
        stored = embed_and_store(chunks, document_id=document_id, user_id=user_id)

        client.table("document_jobs").update(
            {"status": "ready", "chunks_stored": stored}
        ).eq("id", document_id).execute()

    except Exception as exc:
        update_status("failed", str(exc))
        raise self.retry(exc=exc, countdown=30)
