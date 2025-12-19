import React from "react";

function formatContent(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/\n\n/g, "</p><p>")
    .replace(/^/g, "<p>")
    .replace(/$/g, "</p>");
}

export default function MessageBubble({ role, content }) {
  const isUser = role === "user";

  return (
    <div
      style={{
        marginBottom: "1rem",
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
      }}
    >
      <div
        style={{
          maxWidth: "70%",
          padding: isUser ? "0.75rem 1rem" : "0.85rem 1.1rem",
          borderRadius: isUser
            ? "1rem 1rem 0.25rem 1rem"
            : "1rem 1rem 1rem 0.25rem",
          background: isUser ? "#4f46e5" : "white",
          color: isUser ? "white" : "#111827",
          fontSize: "15px",
          lineHeight: 1.5,
          wordWrap: "break-word",
          boxShadow: isUser
            ? "0 2px 8px rgba(79, 70, 229, 0.15)"
            : "0 1px 3px rgba(0, 0, 0, 0.08)",
          fontWeight: isUser ? 500 : 400,
        }}
      >
        {!isUser && content.includes("\n") ? (
          <div
            dangerouslySetInnerHTML={{ __html: formatContent(content) }}
            style={{ whiteSpace: "pre-wrap", overflowWrap: "break-word" }}
          />
        ) : (
          <span>{content}</span>
        )}
      </div>
    </div>
  );
}