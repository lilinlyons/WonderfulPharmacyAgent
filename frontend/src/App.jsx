import React, { useEffect, useRef, useState } from "react";
import { Send } from "lucide-react";

/* ---------------- I18N ---------------- */
const I18N = {
  en: {
    greeting: (name) => `Hello ${name}! How can I help you today?`,
    subtitle: "Get answers about medications, dosages, side effects, and more",
    placeholder: "Ask about medications, dosages, side effects...",
    error: "Sorry, something went wrong.",
    requestsTitle: "Prescription Requests",
    supportTitle: "Support Requests",
    noRequests: "No requests found",
  },
  he: {
    greeting: (name) => `שלום ${name}! איך אפשר לעזור לך היום?`,
    subtitle: "מידע על תרופות, מינונים, תופעות לוואי ועוד",
    placeholder: "שאל על תרופות, מינונים, תופעות לוואי...",
    error: "אירעה שגיאה, נסה שוב.",
    requestsTitle: "בקשות מרשם",
    supportTitle: "פניות תמיכה",
    noRequests: "לא נמצאו בקשות",
  },
};

/* ---------------- Assistant Typing ---------------- */
function AssistantTyping() {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
      <img
        src="/download.jpeg"
        alt="assistant"
        style={{
          width: 42,
          height: 42,
          animation: "pulse 1.2s ease-in-out infinite",
        }}
      />
      <span style={{ color: "#6b7280" }}>Assistant is typing…</span>

      <style>
        {`
          @keyframes pulse {
            0%   { transform: scale(0.85); opacity: 0.7; }
            50%  { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(0.85); opacity: 0.7; }
          }
        `}
      </style>
    </div>
  );
}

/* ---------------- MAIN COMPONENT ---------------- */
export default function PharmaChat() {
  const apiBase = "http://localhost:8000";
  const sessionIdRef = useRef(crypto.randomUUID());
  const messagesEndRef = useRef(null);

  const [users, setUsers] = useState([]);
  const [activeUser, setActiveUser] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const [prescriptionRequests, setPrescriptionRequests] = useState([]);
  const [supportRequests, setSupportRequests] = useState([]);

  const [showRequests, setShowRequests] = useState(true);
  const [showSupport, setShowSupport] = useState(true);

  /* ---------------- LOAD USERS ---------------- */
  useEffect(() => {
    fetch(`${apiBase}/users`)
      .then((r) => r.json())
      .then((data) => {
        if (Array.isArray(data) && data.length) {
          setUsers(data);
          setActiveUser(data[0]);
        }
      });
  }, []);

  /* ---------------- LANGUAGE ---------------- */
  const lang = activeUser?.lang === "he" ? "he" : "en";
  const t = I18N[lang];
  const isRTL = lang === "he";

  /* ---------------- RESET CHAT ---------------- */
  useEffect(() => {
    if (!activeUser) return;

    sessionIdRef.current = crypto.randomUUID();
    setMessages([{ role: "assistant", content: t.greeting(activeUser.full_name) }]);
    refreshSidebar();
  }, [activeUser, lang]);

  /* ---------------- AUTO SCROLL ---------------- */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  /* ---------------- REFRESH SIDEBAR ---------------- */
  const refreshSidebar = async () => {
    if (!activeUser) return;

    try {
      const [presRes, supportRes] = await Promise.all([
        fetch(`${apiBase}/prescription-requests/${activeUser.id}`),
        fetch(`${apiBase}/support-requests/${activeUser.id}`),
      ]);

      const presData = await presRes.json();
      const supportData = await supportRes.json();

      setPrescriptionRequests(Array.isArray(presData) ? presData : []);
      setSupportRequests(Array.isArray(supportData) ? supportData : []);
    } catch {
      setPrescriptionRequests([]);
      setSupportRequests([]);
    }
  };

  /* ---------------- SEND MESSAGE ---------------- */
  const send = async () => {
    if (!activeUser || !input.trim() || loading) return;

    const text = input.trim();
    setInput("");
    setLoading(true);
    setMessages((m) => [...m, { role: "user", content: text }]);

    let assistantText = "";

    try {
      const res = await fetch(`${apiBase}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          session_id: sessionIdRef.current,
          user_id: activeUser.id,
          user_role: activeUser.role,
          preferred_lang: activeUser.lang,
        }),
      });

      const reader = res.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        assistantText += decoder.decode(value, { stream: true });

        setMessages((prev) => {
          const last = prev.at(-1);
          if (last?.role === "assistant") {
            return [...prev.slice(0, -1), { role: "assistant", content: assistantText }];
          }
          return [...prev, { role: "assistant", content: assistantText }];
        });
      }
    } catch {
      setMessages((m) => [...m, { role: "assistant", content: t.error }]);
    } finally {
      setLoading(false);
      refreshSidebar();
    }
  };

  if (!activeUser) return <div style={{ padding: 20 }}>Loading…</div>;

  /* ---------------- RENDER ---------------- */
  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        direction: isRTL ? "rtl" : "ltr",
        background: "linear-gradient(135deg,#f0f9ff,#e0e7ff)",
        fontFamily: "system-ui",
      }}
    >
      {/* HEADER */}
      <div style={{ background: "white", padding: "1.5rem", textAlign: "center" }}>
        <select
          value={activeUser.id}
          onChange={(e) => setActiveUser(users.find((u) => u.id === e.target.value))}
          style={{ position: "absolute", left: "1rem", top: "1rem" }}
        >
          {users.map((u) => (
            <option key={u.id} value={u.id}>
              {u.full_name} ({u.role})
            </option>
          ))}
        </select>

        <h1 style={{ fontSize: "2rem", fontWeight: 700 }}>
          <span style={{ color: "#111827" }}>My </span>
          <span style={{ color: "#6d28d9", fontStyle: "italic", fontWeight: 800 }}>
            Wonderful
          </span>
          <span style={{ color: "#111827" }}> Pharmacy Assistant</span>
        </h1>

        <p style={{ color: "#6b7280" }}>{t.subtitle}</p>
      </div>

      {/* BODY */}
      <div style={{ flex: 1, display: "flex" }}>
        {/* CHAT */}
        <div style={{ flex: 1, padding: "1.5rem", overflowY: "auto" }}>
          {messages.map((m, i) => (
            <div key={i} style={{ marginBottom: "1rem", textAlign: m.role === "user" ? "right" : "left" }}>
              <div
                style={{
                  display: "inline-block",
                  maxWidth: "75%",
                  padding: "0.75rem 1rem",
                  borderRadius: "0.75rem",
                  background: m.role === "user" ? "#4f46e5" : "white",
                  color: m.role === "user" ? "white" : "#111827",
                }}
              >
                {m.content}
              </div>
            </div>
          ))}
          {loading && <AssistantTyping />}
          <div ref={messagesEndRef} />
        </div>

        {/* SIDEBAR */}
        <div style={{ width: 280, background: "#f9fafb", padding: "1rem" }}>
          {/* Prescription */}
          <h3 onClick={() => setShowRequests(!showRequests)} style={{ cursor: "pointer" }}>
            {t.requestsTitle} {showRequests ? "▾" : "▸"}
          </h3>
          {showRequests &&
            (prescriptionRequests.length === 0
              ? <div style={{ color: "#6b7280" }}>{t.noRequests}</div>
              : prescriptionRequests.map((r) => (
                  <div key={r.id} style={{ background: "white", borderRadius: "0.75rem", padding: "0.75rem", marginBottom: "0.75rem", fontSize: "0.8rem" }}>
                    <strong>Request #{r.id.slice(0, 8)}</strong>
                    <div>Status: {r.status}</div>
                    <div>{new Date(r.created_at).toLocaleString()}</div>
                  </div>
                ))
            )}

          {/* Support */}
          <h3 onClick={() => setShowSupport(!showSupport)} style={{ cursor: "pointer", marginTop: "1rem" }}>
            {t.supportTitle} {showSupport ? "▾" : "▸"}
          </h3>
          {showSupport &&
            (supportRequests.length === 0
              ? <div style={{ color: "#6b7280" }}>{t.noRequests}</div>
              : supportRequests.map((s) => (
                  <div key={s.id} style={{ background: "white", borderRadius: "0.75rem", padding: "0.75rem", marginBottom: "0.75rem", fontSize: "0.8rem" }}>
                    <strong>Support #{s.id.slice(0, 8)}</strong>
                    <div>Status: {s.status}</div>
                    <div>{new Date(s.created_at).toLocaleString()}</div>
                  </div>
                ))
            )}
        </div>
      </div>

      {/* INPUT */}
      <div style={{ background: "white", padding: "1rem" }}>
        <div style={{ maxWidth: "64rem", margin: "0 auto", display: "flex", gap: "1rem" }}>
          <textarea
            rows={5}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t.placeholder}
            style={{ flex: 1, padding: "1rem", borderRadius: "0.75rem" }}
          />
          <button
            onClick={send}
            disabled={loading || !input.trim()}
            style={{ background: "#4f46e5", color: "white", borderRadius: "0.75rem", padding: "0.75rem 1rem" }}
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}