from functools import lru_cache
from langchain_anthropic import ChatAnthropic
from langchain_openai import OpenAIEmbeddings
from backend.app.core.config import settings


def get_llm(temperature: float = 0) -> ChatAnthropic:
    return ChatAnthropic(
        model=settings.llm_model,
        anthropic_api_key=settings.anthropic_api_key,
        temperature=temperature,
    )


@lru_cache(maxsize=1)
def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
        dimensions=settings.embedding_dimensions,
    )
