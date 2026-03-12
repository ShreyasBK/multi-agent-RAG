from backend.app.models.state import AgentState
from backend.app.agents.tools.vector_search import vector_search
from backend.app.agents.tools.keyword_search import keyword_search

TOP_K = 10


def retriever_node(state: AgentState) -> dict:
    query = state["query"]
    use_hybrid = state.get("use_hybrid_search", False)

    vector_docs = vector_search(query, top_k=TOP_K, user_id=state.get("user_id"))

    if use_hybrid:
        kw_docs = keyword_search(query, top_k=TOP_K // 2, user_id=state.get("user_id"))
        # Merge and deduplicate by id
        seen = {d["id"] for d in vector_docs}
        merged = vector_docs + [d for d in kw_docs if d["id"] not in seen]
    else:
        merged = vector_docs

    avg_score = sum(d.get("similarity", 0) for d in merged) / len(merged) if merged else 0.0

    return {
        "retrieved_docs": merged,
        "retrieval_score": avg_score,
        "retry_count": state.get("retry_count", 0),
    }
