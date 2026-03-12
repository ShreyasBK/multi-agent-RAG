"use client";
import { useEffect, useState } from "react";
import { ProcessingStatus } from "./ProcessingStatus";

interface Doc {
  document_id: string;
  filename: string;
  status: string;
  chunks_stored?: number;
}

export function DocList() {
  const [docs, setDocs] = useState<Doc[]>([]);

  useEffect(() => {
    fetch("/api/documents")
      .then((r) => r.json())
      .then((d) => setDocs(d.documents ?? []));
  }, []);

  if (!docs.length) return <p className="text-sm text-muted-foreground">No documents yet.</p>;

  return (
    <ul className="flex flex-col gap-2">
      {docs.map((doc) => (
        <li key={doc.document_id} className="border rounded p-3 flex items-center justify-between text-sm">
          <span>{doc.filename}</span>
          <ProcessingStatus status={doc.status} chunks={doc.chunks_stored} />
        </li>
      ))}
    </ul>
  );
}
