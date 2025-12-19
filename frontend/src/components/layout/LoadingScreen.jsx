import React from "react";

export default function LoadingScreen({ text = "Loading…" }) {
  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(135deg,#f0f9ff,#e0e7ff)",
        fontFamily: "system-ui",
      }}
    >
      <div style={{ textAlign: "center" }}>
        <div style={{ position: "relative", width: 220, height: 220, margin: "0 auto" }}>
          <div
            style={{
              position: "absolute",
              inset: 0,
              borderRadius: "999px",
              border: "3px solid rgba(79,70,229,0.25)",
              animation: "radar 1.6s ease-out infinite",
            }}
          />
          <div
            style={{
              position: "absolute",
              inset: 0,
              borderRadius: "999px",
              border: "3px solid rgba(79,70,229,0.18)",
              animation: "radar 1.6s ease-out infinite",
              animationDelay: "0.8s",
            }}
          />
          <img
            src="/download.jpeg"
            alt="loading"
            style={{
              width: 180,
              height: 180,
              borderRadius: "999px",
              objectFit: "cover",
              position: "absolute",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              boxShadow: "0 10px 30px rgba(0,0,0,0.12)",
            }}
          />
        </div>
        <div style={{ marginTop: "1rem", color: "#111827", fontWeight: 600 }}>
          {text}
        </div>
        <style>
          {`
            @keyframes radar {
              0% { transform: scale(0.75); opacity: 0.0; }
              15% { opacity: 1.0; }
              100% { transform: scale(1.25); opacity: 0.0; }
            }
          `}
        </style>
      </div>
    </div>
  );
}