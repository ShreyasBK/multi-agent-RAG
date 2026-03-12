from langchain_core.documents import Document
from backend.app.services.llm import get_embeddings
from backend.app.services.supabase import get_supabase

BATCH_SIZE = 100


def embed_and_store(
    chunks: list[Document],
    document_id: str,
    user_id: str,
) -> int:
    embeddings_model = get_embeddings()
    client = get_supabase()

    stored = 0
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        texts = [c.page_content for c in batch]
        vectors = embeddings_model.embed_documents(texts)

        rows = [
            {
                "document_id": document_id,
                "user_id": user_id,
                "content": text,
                "embedding": vector,
                "metadata": chunk.metadata,
            }
            for text, vector, chunk in zip(texts, vectors, batch)
        ]
        client.table("chunks").insert(rows).execute()
        stored += len(rows)

    return stored
