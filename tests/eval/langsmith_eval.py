"""LangSmith evaluation suite for the RAG pipeline."""
from langsmith import Client
from langsmith.evaluation import evaluate
from src.graph.workflow import rag_graph

client = Client()

DATASET_NAME = "multi-agent-rag-eval"


def predict(inputs: dict) -> dict:
    result = rag_graph.invoke({
        "query": inputs["query"],
        "session_id": "eval",
        "messages": [],
        "rewrite_count": 0,
    })
    return {"answer": result["answer"]}


def answer_relevance(run, example) -> dict:
    """Simple keyword-based relevance check. Replace with LLM judge."""
    answer = run.outputs.get("answer", "").lower()
    expected_keywords = example.outputs.get("keywords", [])
    hits = sum(1 for kw in expected_keywords if kw.lower() in answer)
    score = hits / len(expected_keywords) if expected_keywords else 0.0
    return {"key": "answer_relevance", "score": score}


if __name__ == "__main__":
    results = evaluate(
        predict,
        data=DATASET_NAME,
        evaluators=[answer_relevance],
        experiment_prefix="rag-eval",
    )
    print(results)
