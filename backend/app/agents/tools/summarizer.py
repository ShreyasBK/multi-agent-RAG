from backend.app.services.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate

_prompt = ChatPromptTemplate.from_messages([
    ("system", "Summarize the following document content concisely in 2-3 sentences."),
    ("human", "{content}"),
])


def summarize_document(content: str) -> str:
    llm = get_llm(temperature=0)
    chain = _prompt | llm
    result = chain.invoke({"content": content[:4000]})  # truncate for token safety
    return result.content
