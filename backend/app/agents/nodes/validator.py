from backend.app.models.state import AgentState
from backend.app.services.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate

_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "Check if the answer is grounded in the provided context (no hallucinations).\n"
        "Respond as JSON: {\"grounded\": true/false, \"score\": 0.0-1.0, \"reason\": \"...\"}"
    )),
    ("human", "Question: {query}\n\nAnswer: {answer}\n\nContext: {context}"),
])


def validator_node(state: AgentState) -> dict:
    import json
    docs = state.get("reranked_docs") or state.get("retrieved_docs", [])
    context = " | ".join(d.get("content", "")[:150] for d in docs[:3])

    llm = get_llm(temperature=0)
    chain = _prompt | llm
    result = chain.invoke({
        "query": state["query"],
        "answer": state.get("answer", ""),
        "context": context,
    })

    try:
        parsed = json.loads(result.content)
        is_grounded = bool(parsed.get("grounded", True))
        score = float(parsed.get("score", 1.0))
    except (json.JSONDecodeError, KeyError):
        is_grounded = True
        score = 1.0

    needs_retry = not is_grounded and state.get("retry_count", 0) < 2

    return {
        "hallucination_score": 1.0 - score,
        "is_grounded": is_grounded,
        "needs_retry": needs_retry,
        "retry_count": state.get("retry_count", 0) + (1 if needs_retry else 0),
    }
