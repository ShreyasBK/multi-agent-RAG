from langgraph.graph import StateGraph, END
from backend.app.models.state import AgentState
from backend.app.agents.nodes.router import router_node
from backend.app.agents.nodes.retriever import retriever_node
from backend.app.agents.nodes.reranker import reranker_node
from backend.app.agents.nodes.generator import generator_node
from backend.app.agents.nodes.validator import validator_node


def should_retry(state: AgentState) -> str:
    if state.get("needs_retry") and state.get("retry_count", 0) < 2:
        return "retry"
    return "done"


def build_rag_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("reranker", reranker_node)
    graph.add_node("generator", generator_node)
    graph.add_node("validator", validator_node)

    graph.set_entry_point("router")
    graph.add_edge("router", "retriever")
    graph.add_edge("retriever", "reranker")
    graph.add_edge("reranker", "generator")
    graph.add_edge("generator", "validator")
    graph.add_conditional_edges(
        "validator",
        should_retry,
        {"retry": "retriever", "done": END},
    )

    return graph.compile()


rag_graph = build_rag_graph()
