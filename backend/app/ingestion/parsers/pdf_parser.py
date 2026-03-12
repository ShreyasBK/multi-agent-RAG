from pathlib import Path
from langchain_core.documents import Document


def parse_pdf(path: Path) -> list[Document]:
    from unstructured.partition.pdf import partition_pdf
    elements = partition_pdf(filename=str(path), strategy="hi_res")
    return [
        Document(
            page_content=str(el),
            metadata={"source": path.name, "element_type": type(el).__name__},
        )
        for el in elements
        if str(el).strip()
    ]
