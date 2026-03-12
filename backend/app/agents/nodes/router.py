from backend.app.services.llm import get_llm
from backend.app.models.state import AgentState
from langchain_core.prompts import ChatPromptTemplate

_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "Classify the query into: factual, analytical, or conversational.\n"
        "Also decide if hybrid search (semantic + keyword) is needed: yes/no.\n"
        "Respond as JSON: {\"type\": \"...\", \"hybrid\": true/false}"
    )),
    ("human", "{query}"),
])


def router_node(state: AgentState) -> dict:
    import json
    llm = get_llm(temperature=0)
    chain = _prompt | llm
    result = chain.invoke({"query": state["query"]})
    try:
        parsed = json.loads(result.content)
        query_type = parsed.get("type", "factual")
        use_hybrid = bool(parsed.get("hybrid", False))
    except (json.JSONDecodeError, AttributeError):
        query_type = "factual"
        use_hybrid = False

    return {"query_type": query_type, "use_hybrid_search": use_hybrid}
