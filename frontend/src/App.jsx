import React, { useMemo, useState } from "react";

export default function App() {
  const [lang, setLang] = useState("he");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { role: "assistant", content: lang === "he" ? "היי! איך אפשר לעזור?" : "Hi! How can I help?" }
  ]);

  const apiBase = useMemo(() => (import.meta.env.VITE_API_BASE || "http://localhost:8000"), []);

  async function send() {
    const trimmed = input.trim();
    if (!trimmed) return;

    const nextMessages = [...messages, { role: "user", content: trimmed }];
    setMessages(nextMessages);
    setInput("");

    // Create a placeholder assistant message we’ll stream into
    let assistantText = "";
    setMessages([...nextMessages, { role: "assistant", content: "" }]);

    const res = await fetch(`${apiBase}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: nextMessages })
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });

      // SSE parsing (very simple)
      const lines = chunk.split("\n");
      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        const payload = JSON.parse(line.slice(6));
        if (payload.type === "delta") {
          assistantText += payload.text;
          setMessages(prev => {
            const copy = [...prev];
            copy[copy.length - 1] = { role: "assistant", content: assistantText };
            return copy;
          });
        }
      }
    }
  }

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", fontFamily: "system-ui" }}>
      <h2>Pharmacy Agent (Streaming, Stateless)</h2>

      <div style={{ marginBottom: 10 }}>
        <label>Language: </label>
        <select value={lang} onChange={e => setLang(e.target.value)}>
          <option value="he">Hebrew</option>
          <option value="en">English</option>
        </select>
      </div>

      <div style={{ border: "1px solid #ddd", padding: 16, height: 420, overflow: "auto" }}>
        {messages.map((m, idx) => (
          <div key={idx} style={{ margin: "10px 0" }}>
            <b>{m.role}:</b> <span dir={lang === "he" ? "rtl" : "ltr"}>{m.content}</span>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
        <input
          style={{ flex: 1, padding: 10 }}
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder={lang === "he" ? "כתוב הודעה..." : "Type a message..."}
          onKeyDown={e => e.key === "Enter" && send()}
        />
        <button onClick={send} style={{ padding: "10px 16px" }}>Send</button>
      </div>
    </div>
  );
}
