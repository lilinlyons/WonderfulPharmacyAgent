import React, { useState } from "react";
import { Send } from "lucide-react";

export default function ChatInput({ onSend, disabled, placeholder }) {
  const [input, setInput] = useState("");
  const [hoverSend, setHoverSend] = useState(false);

  const handleSend = () => {
    if (!input.trim() || disabled) return;
    onSend(input.trim());
    setInput("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div style={{ padding: "1rem", background: "white", borderTop: "1px solid #e5e7eb" }}>
      <div style={{ display: "flex", gap: "0.75rem" }}>
        <textarea
          rows={3}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          style={{
            flex: 1,
            padding: "1rem",
            borderRadius: "0.75rem",
            resize: "none",
            fontFamily: "system-ui",
            fontSize: "15px",
            lineHeight: 1.5,
            border: "1px solid #d1d5db",
            outline: "none",
          }}
        />

        <button
          onClick={handleSend}
          onMouseEnter={() => setHoverSend(true)}
          onMouseLeave={() => setHoverSend(false)}
          disabled={!input.trim() || disabled}
          style={{
            background: hoverSend && !disabled ? "#4338ca" : "#4f46e5",
            color: "white",
            borderRadius: "0.75rem",
            padding: "1rem",
            border: "none",
            cursor: !input.trim() || disabled ? "not-allowed" : "pointer",
            transition: "all 0.2s ease",
            opacity: !input.trim() || disabled ? 0.6 : 1,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
}