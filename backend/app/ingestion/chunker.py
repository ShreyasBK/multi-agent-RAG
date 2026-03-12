from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Semantic + hierarchical chunking strategy
_parent_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2048,
    chunk_overlap=128,
    separators=["\n\n\n", "\n\n", "\n", ". ", " ", ""],
)

_child_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""],
)


def chunk_documents(docs: list[Document]) -> list[Document]:
    """
    Two-level chunking: large parent chunks for context,
    small child chunks for precision retrieval.
    Child chunks carry parent_id in metadata.
    """
    chunks: list[Document] = []
    for parent_idx, parent in enumerate(_parent_splitter.split_documents(docs)):
        parent.metadata["parent_id"] = f"p{parent_idx}"
        children = _child_splitter.split_documents([parent])
        for child in children:
            child.metadata["parent_id"] = f"p{parent_idx}"
        chunks.extend(children)
    return chunks
