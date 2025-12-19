import React from "react";
import MessageList from "./MessageList";
import ChatInput from "./ChatInput";

export default function ChatContainer({
  messages,
  loading,
  onSend,
  placeholder,
  typingText,
}) {
  return (
    <div style={{ flex: 1, display: "flex", flexDirection: "column", minHeight: 0 }}>
      <MessageList messages={messages} loading={loading} typingText={typingText} />
      <ChatInput onSend={onSend} disabled={loading} placeholder={placeholder} />
    </div>
  );
}