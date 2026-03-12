from fastapi import APIRouter, Depends, HTTPException
from backend.app.models.schemas import ChatRequest, ChatResponse, SourceReference
from backend.app.agents.graph import rag_graph
from backend.app.api.middleware.auth import verify_supabase_jwt
from backend.app.api.middleware.rate_limit import rate_limit

router = APIRouter()


@router.post("/{session_id}", response_model=ChatResponse)
async def chat(
    session_id: str,
    body: ChatRequest,
    token: dict = Depends(verify_supabase_jwt),
) -> ChatResponse:
    user_id = token.get("sub", "")
    await rate_limit(request=None, user_id=user_id)

    try:
        result = await rag_graph.ainvoke({
            "query": body.query,
            "session_id": session_id,
            "user_id": user_id,
            "messages": [],
            "retry_count": 0,
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    sources = [
        SourceReference(
            doc_id=str(s),
            content_preview="",
            similarity=result.get("confidence", 0.0),
            source_file="",
        )
        for s in result.get("sources", [])
    ]

    return ChatResponse(
        answer=result["answer"],
        sources=sources,
        confidence=result.get("confidence", 0.0),
        session_id=session_id,
        query_type=result.get("query_type", "factual"),
    )
