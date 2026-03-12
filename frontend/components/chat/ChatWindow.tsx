"use client";
import { useState } from "react";
import { MessageBubble } from "./MessageBubble";
import { SourceCard } from "./SourceCard";

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: { doc_id: string; content_preview: string; source_file: string }[];
}

export function ChatWindow({ sessionId }: { sessionId: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function send() {
    if (!input.trim()) return;
    const userMsg: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    const res = await fetch("/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: input, sessionId }),
    });
    const data = await res.json();
    setMessages((prev) => [
      ...prev,
      { role: "assistant", content: data.answer, sources: data.sources },
    ]);
    setLoading(false);
  }

  return (
    <div className="flex flex-col h-full p-4 gap-4">
      <div className="flex-1 overflow-y-auto flex flex-col gap-2">
        {messages.map((m, i) => (
          <div key={i}>
            <MessageBubble role={m.role} content={m.content} />
            {m.sources?.map((s) => <SourceCard key={s.doc_id} source={s} />)}
          </div>
        ))}
        {loading && <p className="text-muted-foreground text-sm">Thinking…</p>}
      </div>
      <div className="flex gap-2">
        <input
          className="flex-1 border rounded px-3 py-2 text-sm"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Ask a question…"
        />
        <button
          onClick={send}
          className="px-4 py-2 bg-primary text-primary-foreground rounded text-sm"
        >
          Send
        </button>
      </div>
    </div>
  );
}
