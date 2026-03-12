const STATUS_STYLES: Record<string, string> = {
  queued: "text-yellow-600",
  processing: "text-blue-600",
  ready: "text-green-600",
  failed: "text-red-600",
};

export function ProcessingStatus({ status, chunks }: { status: string; chunks?: number }) {
  return (
    <span className={`text-xs font-medium ${STATUS_STYLES[status] ?? ""}`}>
      {status}{status === "ready" && chunks ? ` · ${chunks} chunks` : ""}
    </span>
  );
}
