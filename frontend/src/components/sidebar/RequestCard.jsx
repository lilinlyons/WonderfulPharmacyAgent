import React from "react";

export default function RequestCard({ request, type = "prescription" }) {
  return (
    <div
      style={{
        background: "#f9fafb",
        padding: "1rem",
        borderRadius: "0.5rem",
        marginBottom: "0.75rem",
        fontSize: "0.85rem",
        border: "1px solid #e5e7eb",
      }}
    >
      <div style={{ fontWeight: 600, color: "#6d28d9", marginBottom: "0.5rem" }}>
        #{request.id.slice(0, 8)}
      </div>

      <div style={{ color: "#6b7280", marginBottom: "0.25rem" }}>
        <strong>Status:</strong> {request.status}
      </div>

      {type === "prescription" && request.medication_name && (
        <div style={{ color: "#6b7280", marginBottom: "0.25rem" }}>
          <strong>Med:</strong> {request.medication_name}
        </div>
      )}
        

      {request.created_at && (
        <div style={{ color: "#9ca3af", fontSize: "0.8rem" }}>
          {new Date(request.created_at).toLocaleDateString()}
        </div>
      )}
    </div>
  );
}