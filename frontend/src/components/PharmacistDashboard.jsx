import React, { useState, useEffect } from "react";

export default function PharmacistDashboard({ data }) {
  const [prescriptions, setPrescriptions] = useState([]);
  const [supportRequests, setSupportRequests] = useState([]);

  useEffect(() => {
    if (data?.prescriptions) {
      setPrescriptions(data.prescriptions);
    }
    if (data?.support_requests) {
      setSupportRequests(data.support_requests);
    }
  }, [data]);

  const updatePrescriptionStatus = async (id, newStatus) => {
    setPrescriptions((prev) =>
      prev.map((p) =>
        p.id === id ? { ...p, status: newStatus } : p
      )
    );

    try {
      await fetch(`http://localhost:8000/prescriptions/${id}/status`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus }),
      });
    } catch {
      alert("Failed to update prescription status");
    }
  };

  const updateSupportStatus = async (id, newStatus) => {
    setSupportRequests((prev) =>
      prev.map((s) =>
        s.id === id ? { ...s, status: newStatus } : s
      )
    );

    try {
      await fetch(`http://localhost:8000/support-requests/${id}/status`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus }),
      });
    } catch {
      alert("Failed to update support request status");
    }
  };

  if (!data) {
    return <div style={{ padding: "2rem" }}>Loading dashboard…</div>;
  }

  return (
    <div
      style={{
        flex: 1,
        padding: "2rem",
        overflowY: "auto",
        background: "#f9fafb",
      }}
    >
      <h2 style={{ fontSize: "1.5rem", fontWeight: 700 }}>
        Pharmacist Dashboard
      </h2>

      {/* PRESCRIPTIONS */}
      <h3 style={{ marginTop: "1.5rem" }}>All Prescriptions</h3>
      {prescriptions.length ? (
        prescriptions.map((p) => (
          <div
            key={p.id}
            style={{
              background: "white",
              padding: "1rem",
              borderRadius: "0.5rem",
              marginBottom: "0.75rem",
            }}
          >
            <strong>User:</strong> {p.user_id}
            <br />
            <strong>Medication:</strong> {p.medication_name}
            <br />
            <div style={{ marginTop: "0.5rem" }}>
              <strong>Status:</strong>{" "}
              <select
                value={p.status}
                onChange={(e) =>
                  updatePrescriptionStatus(p.id, e.target.value)
                }
                style={{
                  marginLeft: "0.5rem",
                  padding: "0.25rem 0.5rem",
                  borderRadius: "0.4rem",
                  border: "1px solid #e5e7eb",
                  fontSize: "0.85rem",
                }}
              >
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>

            {p.created_at && (
              <div style={{ color: "#6b7280", fontSize: "0.8rem" }}>
                {new Date(p.created_at).toLocaleString()}
              </div>
            )}
          </div>
        ))
      ) : (
        <p>No prescriptions found.</p>
      )}

      {/* SUPPORT */}
      <h3 style={{ marginTop: "2rem" }}>All Support Requests</h3>
      {supportRequests.length ? (
        supportRequests.map((s) => (
          <div
            key={s.id}
            style={{
              background: "white",
              padding: "1rem",
              borderRadius: "0.5rem",
              marginBottom: "0.75rem",
            }}
          >
            <strong>User:</strong> {s.user_id}
            <br />
            <strong>Topic:</strong> {s.subject}
            <br />
            <div style={{ marginTop: "0.5rem" }}>
              <strong>Status:</strong>{" "}
              <select
                value={s.status}
                onChange={(e) =>
                  updateSupportStatus(s.id, e.target.value)
                }
                style={{
                  marginLeft: "0.5rem",
                  padding: "0.25rem 0.5rem",
                  borderRadius: "0.4rem",
                  border: "1px solid #e5e7eb",
                  fontSize: "0.85rem",
                }}
              >
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>

            {s.created_at && (
              <div style={{ color: "#6b7280", fontSize: "0.8rem" }}>
                {new Date(s.created_at).toLocaleString()}
              </div>
            )}
          </div>
        ))
      ) : (
        <p>No support requests found.</p>
      )}
    </div>
  );
}
