interface Source {
  doc_id: string;
  content_preview: string;
  source_file: string;
}

export function SourceCard({ source }: { source: Source }) {
  return (
    <div className="border rounded p-2 text-xs text-muted-foreground mt-1">
      <span className="font-medium">{source.source_file}</span>
      {source.content_preview && (
        <p className="mt-1 truncate">{source.content_preview}</p>
      )}
    </div>
  );
}
