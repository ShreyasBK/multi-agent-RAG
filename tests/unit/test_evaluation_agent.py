from unittest.mock import MagicMock, patch
from src.agents.evaluation.agent import evaluation_agent


@patch("src.agents.evaluation.agent._chain")
def test_evaluation_high_score(mock_chain):
    mock_chain.invoke.return_value = MagicMock(
        content='{"score": 0.9, "needs_rewrite": false, "reason": "good answer"}'
    )
    state = {
        "query": "What is RAG?",
        "answer": "RAG is retrieval-augmented generation.",
        "retrieved_docs": [],
        "rewrite_count": 0,
    }
    result = evaluation_agent(state)
    assert result["eval_score"] == 0.9
    assert result["needs_rewrite"] is False


@patch("src.agents.evaluation.agent._chain")
def test_evaluation_triggers_rewrite(mock_chain):
    mock_chain.invoke.return_value = MagicMock(
        content='{"score": 0.3, "needs_rewrite": true, "reason": "insufficient context"}'
    )
    state = {
        "query": "What is RAG?",
        "answer": "I don't know.",
        "retrieved_docs": [],
        "rewrite_count": 0,
    }
    result = evaluation_agent(state)
    assert result["needs_rewrite"] is True
    assert result["rewrite_count"] == 1
