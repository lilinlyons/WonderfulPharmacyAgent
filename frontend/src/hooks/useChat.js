import { useState, useRef, useCallback, useEffect } from "react";
import { api } from "../components/utils/api";

export function useChat(activeUser, translations) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // Create session ID once on component mount, never change it
  const sessionIdRef = useRef(null);

  // Initialize session ID only once
  useEffect(() => {
    if (!sessionIdRef.current) {
      sessionIdRef.current = crypto.randomUUID();
      console.log("Created new session ID:", sessionIdRef.current);
    }
  }, []);

  // Reset chat when user changes (but keep same session ID)
  const initializeChat = useCallback(() => {
    if (!activeUser || activeUser.role === "pharmacist") return;

    // Reset messages but DON'T create a new session ID
    setMessages([
      { role: "assistant", content: translations.greeting(activeUser.full_name) },
    ]);
  }, [activeUser, translations]);

  const sendMessage = async (text, onRefreshSidebar) => {
    if (!activeUser || !text.trim() || loading) return;

    setLoading(true);
    setMessages((m) => [...m, { role: "user", content: text }]);

    let assistantText = "";

    try {
      const res = await api.sendMessage({
        message: text,
        session_id: sessionIdRef.current,  // ← Same session ID throughout
        user_id: activeUser.id,
        preferred_lang: activeUser.lang,
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
    } catch (error) {
      console.error("Chat error:", error);
      setMessages((m) => [...m, { role: "assistant", content: translations.error }]);
    } finally {
      setLoading(false);
      if (onRefreshSidebar) onRefreshSidebar();
    }
  };

  return {
    messages,
    loading,
    initializeChat,
    sendMessage,
    sessionId: sessionIdRef.current,  // ← Export for debugging
  };
}