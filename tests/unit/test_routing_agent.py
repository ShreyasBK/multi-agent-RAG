from unittest.mock import MagicMock, patch
from src.agents.routing.agent import routing_agent


@patch("src.agents.routing.agent._chain")
def test_routing_factual(mock_chain):
    mock_chain.invoke.return_value = MagicMock(content="factual")
    result = routing_agent({"query": "What is RAG?", "messages": []})
    assert result["query_type"] == "factual"
    assert result["routed_to"] == "retriever"


@patch("src.agents.routing.agent._chain")
def test_routing_fallback_on_invalid(mock_chain):
    mock_chain.invoke.return_value = MagicMock(content="unknown_type")
    result = routing_agent({"query": "some query", "messages": []})
    assert result["query_type"] == "factual"
