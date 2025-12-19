import React from "react";

export default function AssistantTyping({ text = "Assistant typing…" }) {
  return (
    <div style={{ display: "inline-flex", alignItems: "center", gap: "0.5rem" }}>
      <img
        src="/download.jpeg"
        alt="assistant"
        style={{
          width: 24,
          height: 24,
          borderRadius: "50%",
          animation: "pulse 1.2s ease-in-out infinite",
        }}
      />
      <span style={{ color: "#6b7280", fontSize: "13px", fontWeight: 500 }}>
        {text}
      </span>
      <style>
        {`
          @keyframes pulse {
            0% { transform: scale(0.9); opacity: 0.7; }
            50% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(0.9); opacity: 0.7; }
          }
        `}
      </style>
    </div>
  );
}