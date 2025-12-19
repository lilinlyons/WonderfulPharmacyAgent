import React from "react";
import RequestCard from "./RequestCard";

export default function RequestSection({
  title,
  requests,
  type,
  isOpen,
  onToggle,
  emptyText,
}) {
  return (
    <div style={{ marginBottom: "1.5rem" }}>
      <h3
        onClick={onToggle}
        style={{
          cursor: "pointer",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: "0.95rem",
          fontWeight: 600,
          color: "#111827",
          margin: "0 0 1rem 0",
        }}
      >
        <span>{title}</span>
        <span style={{ fontSize: "0.8rem" }}>{isOpen ? "▾" : "▸"}</span>
      </h3>

      {isOpen && requests.length > 0 ? (
        requests.map((request) => (
          <RequestCard key={request.id} request={request} type={type} />
        ))
      ) : isOpen ? (
        <div style={{ color: "#9ca3af", fontSize: "0.85rem" }}>{emptyText}</div>
      ) : null}
    </div>
  );
}