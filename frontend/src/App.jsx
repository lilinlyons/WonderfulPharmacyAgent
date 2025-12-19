import React, { useEffect } from "react";
import { useUsers } from "./hooks/useUsers";
import { useChat } from "./hooks/useChat";
import { useRequests } from "./hooks/useRequests.js";
import { getTranslations, isRTL } from "./components/utils/il8n.js";

import LoadingScreen from "./components/layout/LoadingScreen";
import Header from "./components/layout/Header";
import ChatContainer from "./components/chat/ChatContainer";
import Sidebar from "./components/sidebar/Sidebar";
import PharmacistDashboard from "./components/dashboard/PharmacistDashboard";

export default function App() {
  const { users, activeUser, setActiveUser, loading: usersLoading } = useUsers();
  const translations = getTranslations(activeUser?.lang || "en");
  const rtl = isRTL(activeUser?.lang || "en");

  const { messages, loading: chatLoading, initializeChat, sendMessage } = useChat(
    activeUser,
    translations
  );

  const {
    prescriptionRequests,
    supportRequests,
    refresh: refreshRequests,
    loading: requestsLoading,
    medicationsSold,
  } = useRequests(activeUser);

  // Initialize chat when user changes
  useEffect(() => {
    if (activeUser) {
      initializeChat();
      refreshRequests();
    }
  }, [activeUser?.id, initializeChat, refreshRequests]);

  const handleSendMessage = async (text) => {
    await sendMessage(text, refreshRequests);
  };

  const isPharmacist = activeUser?.role === "pharmacist";

  // Show loading screen while initializing
  if (usersLoading || !activeUser) {
    return <LoadingScreen text={translations.loading} />;
  }

  // Prepare dashboard data for pharmacist
  const dashboardData = isPharmacist ? {
    prescriptions: prescriptionRequests || [],
    support_requests: supportRequests || [],
    medications_sold: medicationsSold || [],
  } : null;

  return (
    <div
      style={{
        height: "100vh",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        direction: rtl ? "rtl" : "ltr",
        fontFamily: "system-ui",
      }}
    >
      <Header
        users={users}
        activeUser={activeUser}
        onUserChange={setActiveUser}
        isRTL={rtl}
        subtitle={translations.subtitle}
      />

      <div
        style={{
          flex: 1,
          display: "flex",
          minHeight: 0,
          gap: "1px",
          background: "#e5e7eb",
        }}
      >
        {isPharmacist ? (
          <PharmacistDashboard
            data={dashboardData}
          />
        ) : (
          <>
            <ChatContainer
              messages={messages}
              loading={chatLoading}
              onSend={handleSendMessage}
              placeholder={translations.placeholder}
              typingText={translations.assistantTyping}
            />
            <Sidebar
              prescriptionRequests={prescriptionRequests}
              supportRequests={supportRequests}
              translations={translations}
            />
          </>
        )}
      </div>
    </div>
  );
}