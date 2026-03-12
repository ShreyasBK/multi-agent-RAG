from pathlib import Path
from langchain_core.documents import Document


def parse_pptx(path: Path) -> list[Document]:
    from unstructured.partition.pptx import partition_pptx
    elements = partition_pptx(filename=str(path))
    return [
        Document(
            page_content=str(el),
            metadata={"source": path.name, "element_type": type(el).__name__},
        )
        for el in elements
        if str(el).strip()
    ]
