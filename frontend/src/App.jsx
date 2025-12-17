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
    <div style={{ display: "inline-flex", alignItems: "center", gap: "0.75rem" }}>
      <img
        src="/download.jpeg"
        alt="assistant"
        style={{
          width: 36,
          height: 36,
          animation: "pulse 1.2s ease-in-out infinite",
        }}
      />
      <span style={{ color: "#6b7280", fontSize: "14px" }}>
        Assistant is typing…
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
  const [hoverSend, setHoverSend] = useState(false);

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

  /* ---------------- RESET CHAT ON USER CHANGE ---------------- */
  useEffect(() => {
    if (!activeUser) return;

    sessionIdRef.current = crypto.randomUUID();
    setMessages([{ role: "assistant", content: t.greeting(activeUser.full_name) }]);
    refreshSidebar();
  }, [activeUser, lang]);

  /* ---------------- SAFE AUTO SCROLL ---------------- */
  useEffect(() => {
    const el = messagesEndRef.current?.parentElement;
    if (!el) return;

    if (el.scrollHeight - el.scrollTop - el.clientHeight < 150) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, loading]);

  /* ---------------- SIDEBAR DATA ---------------- */
  const refreshSidebar = async () => {
    if (!activeUser) return;
    try {
      const [pres, sup] = await Promise.all([
        fetch(`${apiBase}/prescription-requests/${activeUser.id}`),
        fetch(`${apiBase}/support-requests/${activeUser.id}`),
      ]);
      setPrescriptionRequests(await pres.json());
      setSupportRequests(await sup.json());
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

  if (!activeUser) return <div>Loading…</div>;

  /* ---------------- RENDER ---------------- */
  return (
    <div
      style={{
        height: "100vh",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        direction: isRTL ? "rtl" : "ltr",
        fontFamily: "system-ui",
      }}
    >
      {/* HEADER */}
      <div style={{ background: "white", padding: "1.5rem", textAlign: "center", position: "relative" }}>
        <select
          value={activeUser.id}
          onChange={(e) =>
            setActiveUser(users.find((u) => u.id === e.target.value))
          }
          style={{
            position: "absolute",
            top: "1rem",
            left: isRTL ? "auto" : "1rem",
            right: isRTL ? "1rem" : "auto",
            padding: "0.4rem 0.6rem",
            borderRadius: "0.5rem",
            border: "1px solid #e5e7eb",
            background: "white",
            fontSize: "0.85rem",
          }}
        >
          {users.map((u) => (
            <option key={u.id} value={u.id}>
              {u.full_name} {u.role ? `(${u.role})` : ""}
            </option>
          ))}
        </select>

        <h1 style={{ fontSize: "2rem", fontWeight: 700 }}>
          Your <span style={{ color: "#6d28d9", fontStyle: "italic" }}>Wonderful</span>{" "}
          Pharmacy Assistant
        </h1>
        <p style={{ color: "#6b7280" }}>{t.subtitle}</p>
      </div>

      {/* BODY */}
      <div style={{ flex: 1, display: "flex", minHeight: 0 }}>
        {/* CHAT */}
        <div
          style={{
            flex: 1,
            padding: "1.5rem",
            overflowY: "auto",
            background: "linear-gradient(135deg,#f0f9ff,#e0e7ff)",
          }}
        >
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

          {loading && (
            <div style={{ marginBottom: "1rem", textAlign: "left" }}>
              <div
                style={{
                  display: "inline-block",
                  padding: "0.75rem 1rem",
                  borderRadius: "0.75rem",
                  background: "white",
                }}
              >
                <AssistantTyping />
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* SIDEBAR */}
        <div style={{ width: 280, padding: "1rem", overflowY: "auto", background: "#f9fafb" }}>
          {/* Prescription */}
          <h3
            onClick={() => setShowRequests(!showRequests)}
            style={{ cursor: "pointer", display: "flex", justifyContent: "space-between" }}
          >
            <span>{t.requestsTitle}</span>
            <span>{showRequests ? "▾" : "▸"}</span>
          </h3>

          {showRequests &&
            prescriptionRequests.map((r) => (
              <div
                key={r.id}
                style={{
                  background: "white",
                  padding: "0.75rem",
                  borderRadius: "0.5rem",
                  marginBottom: "0.5rem",
                  fontSize: "0.8rem",
                }}
              >
                <strong>Request #{r.id.slice(0, 8)}</strong>
                <div>Status: {r.status}</div>
                {r.medication_name && <div>Medication: {r.medication_name}</div>}
                {r.created_at && (
                  <div style={{ color: "#6b7280" }}>
                    {new Date(r.created_at).toLocaleString()}
                  </div>
                )}
              </div>
            ))}

          {/* Support */}
          <h3
            onClick={() => setShowSupport(!showSupport)}
            style={{
              cursor: "pointer",
              display: "flex",
              justifyContent: "space-between",
              marginTop: "1rem",
            }}
          >
            <span>{t.supportTitle}</span>
            <span>{showSupport ? "▾" : "▸"}</span>
          </h3>

          {showSupport &&
            supportRequests.map((s) => (
              <div
                key={s.id}
                style={{
                  background: "white",
                  padding: "0.75rem",
                  borderRadius: "0.5rem",
                  marginBottom: "0.5rem",
                  fontSize: "0.8rem",
                }}
              >
                <strong>Support #{s.id.slice(0, 8)}</strong>
                <div>Status: {s.status}</div>
                {s.subject && <div>Topic: {s.subject}</div>}
                {s.created_at && (
                  <div style={{ color: "#6b7280" }}>
                    {new Date(s.created_at).toLocaleString()}
                  </div>
                )}
              </div>
            ))}
        </div>
      </div>

      {/* INPUT */}
      <div style={{ padding: "1rem", background: "white" }}>
        <div style={{ display: "flex", gap: "1rem" }}>
          <textarea
            rows={3}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                send();
              }
            }}
            placeholder={t.placeholder}
            style={{
              flex: 1,
              padding: "1rem",
              borderRadius: "0.75rem",
              resize: "none",
              fontFamily:
                "-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif",
              fontSize: "15px",
              lineHeight: 1.5,
              border: "1px solid #e5e7eb",
            }}
          />

          <button
            onClick={send}
            onMouseEnter={() => setHoverSend(true)}
            onMouseLeave={() => setHoverSend(false)}
            disabled={!input.trim() || loading}
            style={{
              background: hoverSend ? "#4338ca" : "#4f46e5",
              color: "white",
              borderRadius: "0.75rem",
              padding: "0.75rem 1rem",
              border: "none",
              cursor: "pointer",
              transition: "all 0.2s ease",
            }}
          >
            <Send />
          </button>
        </div>
      </div>
    </div>
  );
}
