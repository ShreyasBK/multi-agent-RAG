"use client";
import { useRef, useState } from "react";

export function UploadZone() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  async function handleFiles(files: FileList | null) {
    if (!files?.length) return;
    setUploading(true);
    setStatus(null);

    const form = new FormData();
    form.append("file", files[0]);

    const res = await fetch("/api/documents/upload", { method: "POST", body: form });
    const data = await res.json();
    setStatus(res.ok ? `Queued: ${data.filename}` : `Error: ${data.detail}`);
    setUploading(false);
  }

  return (
    <div
      className="border-2 border-dashed rounded-lg p-8 text-center cursor-pointer hover:bg-muted/50"
      onClick={() => inputRef.current?.click()}
      onDrop={(e) => { e.preventDefault(); handleFiles(e.dataTransfer.files); }}
      onDragOver={(e) => e.preventDefault()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.docx,.pptx"
        className="hidden"
        onChange={(e) => handleFiles(e.target.files)}
      />
      {uploading ? (
        <p className="text-sm text-muted-foreground">Uploading…</p>
      ) : (
        <p className="text-sm text-muted-foreground">
          Drop a PDF, DOCX, or PPTX here, or click to browse
        </p>
      )}
      {status && <p className="mt-2 text-xs">{status}</p>}
    </div>
  );
}
