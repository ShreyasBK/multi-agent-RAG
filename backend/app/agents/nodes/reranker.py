from backend.app.models.state import AgentState
from backend.app.services.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate

_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "Given the query and a list of document snippets, return the indices of the "
        "top 5 most relevant documents in order, as a JSON array of integers. "
        "Example: [2, 0, 4, 1, 3]"
    )),
    ("human", "Query: {query}\n\nDocuments:\n{docs}"),
])


def reranker_node(state: AgentState) -> dict:
    import json
    docs = state.get("retrieved_docs", [])
    if len(docs) <= 5:
        return {"reranked_docs": docs}

    llm = get_llm(temperature=0)
    chain = _prompt | llm

    docs_text = "\n".join(
        f"[{i}] {d.get('content', '')[:200]}" for i, d in enumerate(docs)
    )
    result = chain.invoke({"query": state["query"], "docs": docs_text})

    try:
        indices = json.loads(result.content)
        reranked = [docs[i] for i in indices if i < len(docs)]
    except (json.JSONDecodeError, IndexError):
        reranked = docs[:5]

    return {"reranked_docs": reranked}
