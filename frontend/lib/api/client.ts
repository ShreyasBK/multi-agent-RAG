const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const backendClient = {
  async chat(sessionId: string, query: string, authHeader: string) {
    const res = await fetch(`${BASE_URL}/api/chat/${sessionId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: authHeader,
      },
      body: JSON.stringify({ query, session_id: sessionId }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async uploadDocument(file: File, authHeader: string) {
    const form = new FormData();
    form.append("file", file);
    const res = await fetch(`${BASE_URL}/api/documents/upload`, {
      method: "POST",
      headers: { Authorization: authHeader },
      body: form,
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async listDocuments(authHeader: string) {
    const res = await fetch(`${BASE_URL}/api/documents/`, {
      headers: { Authorization: authHeader },
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
};
