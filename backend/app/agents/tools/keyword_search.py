from backend.app.services.supabase import get_supabase


def keyword_search(
    query: str,
    top_k: int = 5,
    user_id: str | None = None,
) -> list[dict]:
    """Full-text search using Postgres tsvector (BM25-like ranking)."""
    client = get_supabase()

    params: dict = {"query_text": query, "match_count": top_k}
    if user_id:
        params["filter_user_id"] = user_id

    response = client.rpc("keyword_search_documents", params).execute()
    return response.data or []
