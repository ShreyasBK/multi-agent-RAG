from backend.app.models.state import AgentState
from backend.app.services.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate

_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a helpful assistant. Answer the question using ONLY the provided context.\n"
        "If the context is insufficient, clearly state that.\n"
        "Cite sources inline as [doc_id].\n\n"
        "Context:\n{context}"
    )),
    ("human", "{query}"),
])


def generator_node(state: AgentState) -> dict:
    docs = state.get("reranked_docs") or state.get("retrieved_docs", [])
    context = "\n\n".join(
        f"[{d.get('id', i)}] {d.get('content', '')}"
        for i, d in enumerate(docs)
    )
    sources = [str(d.get("id", i)) for i, d in enumerate(docs)]

    llm = get_llm(temperature=0.2)
    chain = _prompt | llm
    result = chain.invoke({"context": context, "query": state["query"]})

    return {
        "answer": result.content,
        "sources": sources,
        "confidence": state.get("retrieval_score", 0.0),
    }
