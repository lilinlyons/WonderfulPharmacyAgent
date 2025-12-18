import React, { useState, useEffect } from "react";

export default function PharmacistDashboard({ data }) {
  const [prescriptions, setPrescriptions] = useState([]);
  const [supportRequests, setSupportRequests] = useState([]);
  const [activeTab, setActiveTab] = useState("dashboard");
  const [selectedMedication, setSelectedMedication] = useState("all"); // ✅ NEW

  /* ---------- hydrate state from backend ---------- */
  useEffect(() => {
    if (data?.prescriptions) {
      setPrescriptions(data.prescriptions);
    }
    if (data?.support_requests) {
      setSupportRequests(data.support_requests);
    }
  }, [data]);

  /* ---------- statistics helpers ---------- */
  const buildMonthlySales = (sales) => {
    const map = {};

    sales.forEach((s) => {
      const key = `${s.sold_year}-${String(s.sold_month).padStart(2, "0")}`;
      map[key] = (map[key] || 0) + s.quantity;
    });

    return Object.entries(map)
      .map(([month, total]) => ({ month, total }))
      .sort((a, b) => a.month.localeCompare(b.month));
  };

  /* ---------- FILTER SALES BY MEDICATION ---------- */
  const allSales = data?.medications_sold || [];

  const medicationOptions = [
    "all",
    ...Array.from(new Set(allSales.map((s) => s.medication_id))),
  ];

  const filteredSales =
    selectedMedication === "all"
      ? allSales
      : allSales.filter((s) => s.medication_id === selectedMedication);

  const salesData = buildMonthlySales(filteredSales);
  const maxValue = Math.max(...salesData.map((d) => d.total), 1);

  /* ---------- status updates ---------- */
  const updatePrescriptionStatus = async (id, newStatus) => {
    setPrescriptions((prev) =>
      prev.map((p) => (p.id === id ? { ...p, status: newStatus } : p))
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
      prev.map((s) => (s.id === id ? { ...s, status: newStatus } : s))
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
        background: "linear-gradient(135deg,#f0f9ff,#e0e7ff)",
      }}
    >
      <h2 style={{ fontSize: "1.6rem", fontWeight: 700 }}>
        Pharmacist Dashboard
      </h2>

      {/* ---------- TABS ---------- */}
      <div style={{ display: "flex", gap: "1rem", marginTop: "1rem" }}>
        {["dashboard", "stats"].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              padding: "0.5rem 1.25rem",
              borderRadius: "0.75rem",
              border: "1px solid #e5e7eb",
              background: activeTab === tab ? "#4f46e5" : "white",
              color: activeTab === tab ? "white" : "#111827",
              cursor: "pointer",
              fontWeight: 600,
            }}
          >
            {tab === "dashboard" ? "Dashboard" : "Statistics"}
          </button>
        ))}
      </div>

      {/* ---------- DASHBOARD TAB ---------- */}
      {activeTab === "dashboard" && (
        <>
          <h3 style={{ marginTop: "1.5rem" }}>All Prescriptions</h3>
          {prescriptions.length ? (
            prescriptions.map((p) => (
              <div
                key={p.id}
                style={{
                  background: "white",
                  padding: "1rem",
                  borderRadius: "0.75rem",
                  marginBottom: "0.75rem",
                }}
              >
                <strong>User:</strong> {p.user_id}
                <br />
                <strong>Medication:</strong> {p.medication_id}
                <br />
                <strong>Status:</strong>{" "}
                <select
                  value={p.status}
                  onChange={(e) => updatePrescriptionStatus(p.id, e.target.value)}
                >
                  <option value="Pending">Pending</option>
                  <option value="In Progress">In Progress</option>
                  <option value="Completed">Completed</option>
                </select>
              </div>
            ))
          ) : (
            <p>No prescriptions found.</p>
          )}

          <h3 style={{ marginTop: "2rem" }}>All Support Requests</h3>
          {supportRequests.length ? (
            supportRequests.map((s) => (
              <div
                key={s.id}
                style={{
                  background: "white",
                  padding: "1rem",
                  borderRadius: "0.75rem",
                  marginBottom: "0.75rem",
                }}
              >
                <strong>User:</strong> {s.user_id}
                <br />
                <strong>Topic:</strong> {s.subject}
                <br />
                <strong>Status:</strong>{" "}
                <select
                  value={s.status}
                  onChange={(e) => updateSupportStatus(s.id, e.target.value)}
                >
                  <option value="Pending">Pending</option>
                  <option value="In progress">In Progress</option>
                  <option value="Completed">Completed</option>
                </select>
              </div>
            ))
          ) : (
            <p>No support requests found.</p>
          )}
        </>
      )}

      {/* ---------- STATISTICS TAB ---------- */}
      {activeTab === "stats" && (
        <>
          <h3 style={{ marginTop: "1.5rem" }}>Medication Sales Over Time</h3>

          {/* ✅ MEDICATION FILTER */}
          <div style={{ marginBottom: "1rem" }}>
            <label style={{ fontWeight: 600, marginRight: "0.5rem" }}>
              Medication:
            </label>
            <select
              value={selectedMedication}
              onChange={(e) => setSelectedMedication(e.target.value)}
              style={{
                padding: "0.4rem 0.6rem",
                borderRadius: "0.5rem",
                border: "1px solid #e5e7eb",
                fontSize: "0.85rem",
              }}
            >
              {medicationOptions.map((m) => (
                <option key={m} value={m}>
                  {m === "all" ? "All Medications" : m}
                </option>
              ))}
            </select>
          </div>

          {salesData.length ? (
            <svg
              width="100%"
              height="300"
              viewBox="0 0 640 300"
              style={{
                background: "white",
                borderRadius: "0.75rem",
                padding: "1rem",
              }}
            >
              {/* chart layout */}
              {(() => {
                const left = 70;     // ✅ bigger left margin so y-axis text is visible
                const top = 20;
                const right = 20;
                const bottom = 60;

                const W = 640;
                const H = 300;

                const x0 = left;
                const x1 = W - right;
                const y0 = H - bottom;
                const y1 = top;

                const plotW = x1 - x0;
                const plotH = y0 - y1;

                const ticks = [0, 0.25, 0.5, 0.75, 1];

                const xForIndex = (i) =>
                  x0 + (i * plotW) / Math.max(salesData.length - 1, 1);

                const yForValue = (v) => y0 - (v / maxValue) * plotH;

                return (
                  <>
                    {/* Axes */}
                    <line x1={x0} y1={y1} x2={x0} y2={y0} stroke="#e5e7eb" />
                    <line x1={x0} y1={y0} x2={x1} y2={y0} stroke="#e5e7eb" />

                    {/* Y-axis grid + labels */}
                    {ticks.map((t, i) => {
                      const y = y0 - t * plotH;
                      const value = Math.round(t * maxValue);
                      return (
                        <g key={i}>
                          <line x1={x0} y1={y} x2={x1} y2={y} stroke="#f3f4f6" />
                          <line x1={x0 - 6} y1={y} x2={x0} y2={y} stroke="#9ca3af" />
                          <text
                            x={x0 - 10}
                            y={y + 4}
                            textAnchor="end"
                            fontSize="10"
                            fill="#6b7280"
                          >
                            {value}
                          </text>
                        </g>
                      );
                    })}

                    {/* Line */}
                    <polyline
                      fill="none"
                      stroke="#4f46e5"
                      strokeWidth="3"
                      points={salesData
                        .map((d, i) => `${xForIndex(i)},${yForValue(d.total)}`)
                        .join(" ")}
                    />

                    {/* Points + x labels */}
                    {salesData.map((d, i) => {
                      const x = xForIndex(i);
                      const y = yForValue(d.total);
                      return (
                        <g key={d.month}>
                          <circle cx={x} cy={y} r="4" fill="#4f46e5" />
                          <text
                            x={x}
                            y={y - 8}
                            textAnchor="middle"
                            fontSize="10"
                            fill="#111827"
                          >
                            {d.total}
                          </text>
                          <text
                            x={x}
                            y={y0 + 20}
                            textAnchor="middle"
                            fontSize="10"
                            fill="#6b7280"
                          >
                            {d.month}
                          </text>
                        </g>
                      );
                    })}
                  </>
                );
              })()}
            </svg>
          ) : (
            <p>No sales data available.</p>
          )}
        </>
      )}
    </div>
  );
}
