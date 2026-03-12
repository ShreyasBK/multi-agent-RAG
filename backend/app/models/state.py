from typing import Annotated, Any
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """Shared state across all LangGraph nodes."""
    # Input
    query: str
    session_id: str
    user_id: str

    # Routing
    query_type: str          # "factual" | "analytical" | "conversational"
    use_hybrid_search: bool

    # Retrieval
    retrieved_docs: list[dict[str, Any]]
    reranked_docs: list[dict[str, Any]]
    retrieval_score: float

    # Generation
    answer: str
    sources: list[str]
    confidence: float

    # Validation
    hallucination_score: float
    is_grounded: bool
    needs_retry: bool
    retry_count: int

    # Conversation history
    messages: Annotated[list, add_messages]
