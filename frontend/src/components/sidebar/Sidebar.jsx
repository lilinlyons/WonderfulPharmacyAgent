import React, { useState } from "react";
import RequestSection from "./RequestSection";

export default function Sidebar({
  prescriptionRequests,
  supportRequests,
  translations,
}) {
  const [showRequests, setShowRequests] = useState(true);
  const [showSupport, setShowSupport] = useState(true);

  return (
    <div
      style={{
        width: 300,
        padding: "1.5rem",
        overflowY: "auto",
        background: "white",
        borderLeft: "1px solid #e5e7eb",
      }}
    >
      <RequestSection
        title={translations.requestsTitle}
        requests={prescriptionRequests}
        type="prescription"
        isOpen={showRequests}
        onToggle={() => setShowRequests(!showRequests)}
        emptyText={translations.noRequests}
      />

      <RequestSection
        title={translations.supportTitle}
        requests={supportRequests}
        type="support"
        isOpen={showSupport}
        onToggle={() => setShowSupport(!showSupport)}
        emptyText={translations.noRequests}
      />
    </div>
  );
}