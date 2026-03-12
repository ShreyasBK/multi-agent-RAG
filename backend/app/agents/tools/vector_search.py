from backend.app.services.supabase import get_supabase
from backend.app.services.llm import get_embeddings


def vector_search(
    query: str,
    top_k: int = 10,
    user_id: str | None = None,
    similarity_threshold: float = 0.5,
) -> list[dict]:
    embedding = get_embeddings().embed_query(query)
    client = get_supabase()

    params: dict = {
        "query_embedding": embedding,
        "match_count": top_k,
        "similarity_threshold": similarity_threshold,
    }
    if user_id:
        params["filter_user_id"] = user_id

    response = client.rpc("match_documents", params).execute()
    return response.data or []
