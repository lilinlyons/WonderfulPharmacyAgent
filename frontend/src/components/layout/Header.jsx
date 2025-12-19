import React from "react";

export default function Header({ users, activeUser, onUserChange, isRTL, subtitle }) {
  return (
    <div
      style={{
        background: "white",
        padding: "1.5rem",
        textAlign: "center",
        position: "relative",
        borderBottom: "1px solid #e5e7eb",
      }}
    >
      <select
        value={activeUser?.id}
        onChange={(e) => {
          const user = users.find((u) => u.id === e.target.value);
          if (user) onUserChange(user);
        }}
        style={{
          position: "absolute",
          top: "1rem",
          left: isRTL ? "auto" : "1rem",
          right: isRTL ? "1rem" : "auto",
          padding: "0.5rem 0.75rem",
          borderRadius: "0.5rem",
          border: "1px solid #d1d5db",
          background: "white",
          fontSize: "0.9rem",
          fontWeight: 500,
        }}
      >
        {users.map((u) => (
          <option key={u.id} value={u.id}>
            {u.full_name} {u.role ? `(${u.role})` : ""}
          </option>
        ))}
      </select>

      <h1 style={{ fontSize: "2rem", fontWeight: 700, margin: "0 0 0.5rem 0" }}>
        Your <span style={{ color: "#6d28d9", fontStyle: "italic" }}>Wonderful</span>{" "}
        Pharmacy Assistant
      </h1>

      <p style={{ color: "#6b7280", margin: 0, fontSize: "0.95rem" }}>
        {subtitle}
      </p>
    </div>
  );
}