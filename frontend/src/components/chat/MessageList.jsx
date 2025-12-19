import React, { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";
import AssistantTyping from "./AssistantTyping";

export default function MessageList({ messages, loading, typingText }) {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const el = messagesEndRef.current?.parentElement;
    if (!el) return;

    if (el.scrollHeight - el.scrollTop - el.clientHeight < 150) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, loading]);

  return (
    <div
      style={{
        flex: 1,
        padding: "1.5rem",
        overflowY: "auto",
        background: "linear-gradient(135deg,#f0f9ff,#e0e7ff)",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {messages.map((m, i) => (
        <MessageBubble key={i} role={m.role} content={m.content} />
      ))}

      {loading && (
        <div style={{ marginBottom: "1rem" }}>
          <div
            style={{
              display: "inline-block",
              padding: "0.85rem 1.1rem",
              borderRadius: "1rem 1rem 1rem 0.25rem",
              background: "#f3f4f6",
              boxShadow: "0 1px 3px rgba(0, 0, 0, 0.08)",
            }}
          >
            <AssistantTyping text={typingText} />
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}