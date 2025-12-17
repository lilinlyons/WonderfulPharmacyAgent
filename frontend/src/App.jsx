import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';

export default function PharmaChat() {
  const sessionIdRef = useRef(
    crypto.randomUUID()
  );

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello! I'm your Wonderful Pharmacy Assistant. How can I help you today? I can answer questions about our products, dosage, side effects, or help you find the right medication for your needs."
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const apiBase = "http://localhost:8000";

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const send = async () => {
  const trimmed = input.trim();
  if (!trimmed || loading) return;

  // Add user message
  const userMessage = { role: "user", content: trimmed };
  setMessages(prev => [...prev, userMessage]);
  setInput("");
  setLoading(true);

  let assistantText = "";

  const prevUserMessage = (() => {
  for (let i = messages.length - 1; i >= 0; i--) {
    if (messages[i].role === "user") {
      return messages[i].content;
    }
  }
  return null;
})();

  try {
    const res = await fetch(`${apiBase}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: trimmed,
        prev_user_message: prevUserMessage,
        session_id: sessionIdRef.current
      })
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      assistantText += chunk;

      setMessages(prev => {
        // Check if the last message is from assistant
        const lastMessage = prev[prev.length - 1];
        if (lastMessage?.role === 'assistant') {
          // Update existing assistant message
          const copy = [...prev];
          copy[copy.length - 1] = {
            role: "assistant",
            content: assistantText
          };
          return copy;
        } else {
          // Add new assistant message
          return [...prev, { role: "assistant", content: assistantText }];
        }
      });
    }
  } catch (error) {
    console.error("Error:", error);
    setMessages(prev => {
      const lastMessage = prev[prev.length - 1];
      if (lastMessage?.role === 'assistant') {
        const copy = [...prev];
        copy[copy.length - 1] = {
          role: "assistant",
          content: "Sorry, I encountered an error. Please try again."
        };
        return copy;
      } else {
        return [...prev, {
          role: "assistant",
          content: "Sorry, I encountered an error. Please try again."
        }];
      }
    });
  } finally {
    setLoading(false);
  }
};

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    background: 'linear-gradient(135deg, #f0f9ff 0%, #e0e7ff 100%)',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  };

  const headerStyle = {
    background: 'white',
    borderBottom: '1px solid #e5e7eb',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
    padding: '1.5rem 1rem',
    textAlign: 'center',
  };

  const titleStyle = {
    fontSize: '1.875rem',
    fontWeight: 'bold',
    color: '#111827',
    margin: 0,
  };

  const italicStyle = {
    fontStyle: 'italic',
    color: '#4f46e5',
  };

  const subtitleStyle = {
    fontSize: '0.875rem',
    color: '#6b7280',
    margin: '0.5rem 0 0 0',
  };

  const messagesContainerStyle = {
    flex: 1,
    overflowY: 'auto',
    padding: '1.5rem 1rem',
    maxWidth: '48rem',
    margin: '0 auto',
    width: '100%',
  };

  const messageBubbleStyle = (role) => ({
    display: 'flex',
    justifyContent: role === 'user' ? 'flex-end' : 'flex-start',
    marginBottom: '1rem',
  });

  const bubbleStyle = (role) => ({
    maxWidth: '70%',
    padding: '0.75rem 1rem',
    borderRadius: '0.5rem',
    wordWrap: 'break-word',
    whiteSpace: 'pre-wrap',
    fontSize: '0.95rem',
    lineHeight: '1.5',
    ...(role === 'user' ? {
      background: '#4f46e5',
      color: 'white',
      borderBottomRightRadius: '0.125rem',
      boxShadow: '0 1px 3px rgba(79, 70, 229, 0.3)',
    } : {
      background: 'white',
      color: '#111827',
      border: '1px solid #e5e7eb',
      borderBottomLeftRadius: '0.125rem',
      boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
    })
  });

  const inputContainerStyle = {
    background: 'white',
    borderTop: '1px solid #e5e7eb',
    padding: '1.5rem 1rem',
    boxShadow: '0 -2px 4px rgba(0, 0, 0, 0.05)',
  };

  const inputWrapperStyle = {
    maxWidth: '48rem',
    margin: '0 auto',
    display: 'flex',
    gap: '0.75rem',
  };

  const textareaStyle = {
    flex: 1,
    padding: '0.75rem 1rem',
    border: '1px solid #d1d5db',
    borderRadius: '0.5rem',
    fontSize: '0.95rem',
    fontFamily: 'inherit',
    resize: 'none',
    outline: 'none',
    boxSizing: 'border-box',
    transition: 'border-color 0.2s',
  };

  const buttonStyle = {
    background: loading || !input.trim() ? '#d1d5db' : '#4f46e5',
    color: 'white',
    border: 'none',
    borderRadius: '0.5rem',
    padding: '0.75rem 1rem',
    cursor: loading || !input.trim() ? 'not-allowed' : 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'background 0.2s',
    fontSize: '1rem',
  };

  const helpTextStyle = {
    maxWidth: '48rem',
    margin: '0.5rem auto 0',
    fontSize: '0.75rem',
    color: '#6b7280',
  };

  return (
    <div style={containerStyle}>
      <div style={headerStyle}>
        <h1 style={titleStyle}>
          Your <span style={italicStyle}>Wonderful</span> Pharmacy Assistant
        </h1>
        <p style={subtitleStyle}>
          Get answers about medications, dosages, side effects, and more
        </p>
      </div>

      <div style={messagesContainerStyle}>
        {messages.map((message, idx) => (
          <div key={idx} style={messageBubbleStyle(message.role)}>
            <div style={bubbleStyle(message.role)}>
              {message.content}
            </div>
          </div>
        ))}
        {loading && (
          <div style={messageBubbleStyle('assistant')}>
            <div style={bubbleStyle('assistant')}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <img
                  src="/download.jpeg"
                  alt="Loading..."
                  style={{
                    width: '20px',
                    height: '20px',
                    animation: 'pulse 1.5s ease-in-out infinite',
                  }}
                />
                <span>Assistant is typing...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div style={inputContainerStyle}>
        <div style={inputWrapperStyle}>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about medications, dosages, side effects, insurance coverage..."
            style={textareaStyle}
            rows="3"
            disabled={loading}
          />
          <button
            onClick={send}
            disabled={loading || !input.trim()}
            style={buttonStyle}
            title="Send message"
          >
            <Send size={20} />
          </button>
        </div>
        <div style={helpTextStyle}>
          Press Shift+Enter for new line, Enter to send
        </div>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% {
            transform: scale(1);
            opacity: 1;
          }
          50% {
            transform: scale(1.2);
            opacity: 0.7;
          }
        }
        
        textarea:focus {
          border-color: #4f46e5;
          box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }
        
        button:hover:not(:disabled) {
          background: #4338ca !important;
        }
      `}</style>
    </div>
  );
}