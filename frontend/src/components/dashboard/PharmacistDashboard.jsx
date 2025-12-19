import React, { useState, useEffect } from "react";

export default function PharmacistDashboard({ data }) {
  const [prescriptions, setPrescriptions] = useState([]);
  const [supportRequests, setSupportRequests] = useState([]);
  const [activeTab, setActiveTab] = useState("dashboard");
  const [selectedMedication, setSelectedMedication] = useState("all");
  const [selectedSalesMedication, setSelectedSalesMedication] = useState("all");

  useEffect(() => {
    if (data?.prescriptions) {
      setPrescriptions(data.prescriptions);
    }
    if (data?.support_requests) {
      setSupportRequests(data.support_requests);
    }
  }, [data]);

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

  const allSales = data?.medications_sold || [];
  const medicationOptions = [
    "all",
    ...Array.from(new Set(allSales.map((s) => s.medication_name || s.medication_id))),
  ];

  const filteredSales =
    selectedMedication === "all"
      ? allSales
      : allSales.filter((s) => (s.medication_name || s.medication_id) === selectedMedication);

  const salesData = buildMonthlySales(filteredSales);
  const maxValue = Math.max(...salesData.map((d) => d.total), 1);

  const updatePrescriptionStatus = async (userId, prescriptionId, newStatus) => {
    setPrescriptions((prev) =>
      prev.map((p) => (p.id === prescriptionId ? { ...p, status: newStatus } : p))
    );
    try {
      const res = await fetch(
        `http://localhost:8000/users/${userId}/prescriptions/${prescriptionId}/status`,
        {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ status: newStatus }),
        }
      );
      if (!res.ok) {
        alert("Failed to update prescription status");
      }
    } catch (error) {
      alert("Failed to update prescription status");
      console.error(error);
    }
  };

  const updateSupportStatus = async (userId, ticketId, newStatus) => {
    setSupportRequests((prev) =>
      prev.map((s) => (s.id === ticketId ? { ...s, status: newStatus } : s))
    );
    try {
      const res = await fetch(
        `http://localhost:8000/users/${userId}/support-tickets/${ticketId}/status`,
        {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ status: newStatus }),
        }
      );
      if (!res.ok) {
        alert("Failed to update support ticket status");
      }
    } catch (error) {
      alert("Failed to update support ticket status");
      console.error(error);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "Completed":
        return { bg: "#dbeafe", text: "#0c4a6e", border: "#0284c7" };
      case "In Progress":
      case "In progress":
        return { bg: "#fef08a", text: "#713f12", border: "#eab308" };
      case "Pending":
        return { bg: "#fee2e2", text: "#7c2d12", border: "#ef4444" };
      default:
        return { bg: "#f3f4f6", text: "#111827", border: "#d1d5db" };
    }
  };

  if (!data) {
    return (
      <div
        style={{
          padding: "2rem",
          background: "linear-gradient(135deg,#f0f9ff,#e0e7ff)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: "100%",
        }}
      >
        <div style={{ color: "#6b7280", fontWeight: 500 }}>
          Loading dashboard…
        </div>
      </div>
    );
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
      <div style={{ maxWidth: "1200px", margin: "0 auto" }}>
        {/* HEADER */}
        <div style={{ marginBottom: "2rem" }}>
          <h1
            style={{
              fontSize: "2rem",
              fontWeight: 700,
              color: "#111827",
              margin: "0 0 0.5rem 0",
            }}
          >
            Pharmacist Dashboard
          </h1>
          <p style={{ color: "#6b7280", margin: 0 }}>
            Manage prescriptions, support requests, and view sales analytics
          </p>
        </div>

        {/* STATS CARDS */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
            gap: "1rem",
            marginBottom: "2rem",
          }}
        >
          <StatCard
            label="Total Prescriptions"
            value={prescriptions.length}
            icon="📋"
          />
          <StatCard
            label="Support Requests"
            value={supportRequests.length}
            icon="🆘"
          />
          <div
            style={{
              background: "white",
              padding: "1.5rem",
              borderRadius: "0.75rem",
              border: "1px solid #e5e7eb",
              boxShadow: "0 1px 2px rgba(0,0,0,0.05)",
            }}
          >
            <div style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>📦</div>
            <div style={{ fontSize: "0.85rem", color: "#6b7280", fontWeight: 500 }}>
              Total Sales
            </div>
            <div
              style={{
                fontSize: "1.75rem",
                fontWeight: 700,
                color: "#111827",
                marginTop: "0.5rem",
              }}
            >
              {selectedSalesMedication === "all"
                ? allSales.reduce((sum, s) => sum + (s.quantity || 0), 0)
                : allSales
                    .filter((s) => (s.medication_name || s.medication_id) === selectedSalesMedication)
                    .reduce((sum, s) => sum + (s.quantity || 0), 0)}
            </div>
            <select
              value={selectedSalesMedication}
              onChange={(e) => setSelectedSalesMedication(e.target.value)}
              style={{
                width: "100%",
                marginTop: "0.75rem",
                padding: "0.5rem 0.75rem",
                borderRadius: "0.5rem",
                border: "1px solid #d1d5db",
                fontSize: "0.85rem",
                fontWeight: 500,
                background: "white",
                cursor: "pointer",
              }}
            >
              {medicationOptions.map((m) => (
                <option key={m} value={m}>
                  {m === "all" ? "All Medications" : m}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* TABS */}
        <div
          style={{
            display: "flex",
            gap: "0.5rem",
            marginBottom: "2rem",
            borderBottom: "2px solid #e5e7eb",
          }}
        >
          {["dashboard", "stats"].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                padding: "0.75rem 1.5rem",
                border: "none",
                background: "none",
                borderBottom: activeTab === tab ? "3px solid #4f46e5" : "none",
                color: activeTab === tab ? "#4f46e5" : "#6b7280",
                fontWeight: activeTab === tab ? 600 : 500,
                cursor: "pointer",
                fontSize: "0.95rem",
                transition: "all 0.2s ease",
              }}
            >
              {tab === "dashboard" ? "📊 Dashboard" : "📈 Statistics"}
            </button>
          ))}
        </div>

        {/* DASHBOARD TAB */}
        {activeTab === "dashboard" && (
          <div>
            {/* PRESCRIPTIONS */}
            <div style={{ marginBottom: "3rem" }}>
              <h2
                style={{
                  fontSize: "1.3rem",
                  fontWeight: 600,
                  color: "#111827",
                  marginBottom: "1rem",
                }}
              >
                Prescriptions ({prescriptions.length})
              </h2>
              {prescriptions && prescriptions.length > 0 ? (
                <div style={{ display: "grid", gap: "1rem" }}>
                  {prescriptions.map((p) => {
                    const statusColor = getStatusColor(p.status);
                    return (
                      <div
                        key={p.id}
                        style={{
                          background: "white",
                          padding: "1.25rem",
                          borderRadius: "0.75rem",
                          border: "1px solid #e5e7eb",
                          display: "grid",
                          gridTemplateColumns: "1fr 1fr 1fr 200px",
                          gap: "1rem",
                          alignItems: "center",
                          boxShadow: "0 1px 2px rgba(0,0,0,0.05)",
                        }}
                      >
                        <div>
                          <div
                            style={{
                              fontSize: "0.85rem",
                              color: "#6b7280",
                              fontWeight: 500,
                            }}
                          >
                            USER ID
                          </div>
                          <div
                            style={{
                              fontWeight: 600,
                              color: "#111827",
                              marginTop: "0.25rem",
                            }}
                          >
                            {p.user_id || "—"}
                          </div>
                        </div>

                        <div>
                          <div
                            style={{
                              fontSize: "0.85rem",
                              color: "#6b7280",
                              fontWeight: 500,
                            }}
                          >
                            MEDICATION
                          </div>
                          <div
                            style={{
                              fontWeight: 600,
                              color: "#111827",
                              marginTop: "0.25rem",
                            }}
                          >
                            {p.medication_name || p.medication_id || "—"}
                          </div>
                        </div>


                        <div>
                          <select
                            value={p.status}
                            onChange={(e) =>
                              updatePrescriptionStatus(
                                p.user_id,
                                p.id,
                                e.target.value
                              )
                            }
                            style={{
                              width: "100%",
                              padding: "0.5rem",
                              borderRadius: "0.5rem",
                              border: `1.5px solid ${statusColor.border}`,
                              background: statusColor.bg,
                              color: statusColor.text,
                              fontWeight: 600,
                              fontSize: "0.85rem",
                              cursor: "pointer",
                            }}
                          >
                            <option value="Pending">Pending</option>
                            <option value="In Progress">In Progress</option>
                            <option value="Completed">Completed</option>
                          </select>
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div
                  style={{
                    background: "white",
                    padding: "2rem",
                    borderRadius: "0.75rem",
                    textAlign: "center",
                    color: "#9ca3af",
                  }}
                >
                  No prescriptions found
                </div>
              )}
            </div>

            {/* SUPPORT REQUESTS */}
            <div>
              <h2
                style={{
                  fontSize: "1.3rem",
                  fontWeight: 600,
                  color: "#111827",
                  marginBottom: "1rem",
                }}
              >
                Support Requests ({supportRequests.length})
              </h2>
              {supportRequests && supportRequests.length > 0 ? (
                <div style={{ display: "grid", gap: "1rem" }}>
                  {supportRequests.map((s) => {
                    const statusColor = getStatusColor(s.status);
                    return (
                      <div
                        key={s.id}
                        style={{
                          background: "white",
                          padding: "1.25rem",
                          borderRadius: "0.75rem",
                          border: "1px solid #e5e7eb",
                          display: "grid",
                          gridTemplateColumns: "1fr 1fr 200px",
                          gap: "1rem",
                          alignItems: "center",
                          boxShadow: "0 1px 2px rgba(0,0,0,0.05)",
                        }}
                      >
                        <div>
                          <div
                            style={{
                              fontSize: "0.85rem",
                              color: "#6b7280",
                              fontWeight: 500,
                            }}
                          >
                            USER ID
                          </div>
                          <div
                            style={{
                              fontWeight: 600,
                              color: "#111827",
                              marginTop: "0.25rem",
                            }}
                          >
                            {s.user_id || "—"}
                          </div>
                        </div>

                        <div>
                          <div
                            style={{
                              fontSize: "0.85rem",
                              color: "#6b7280",
                              fontWeight: 500,
                            }}
                          >
                            SUBJECT
                          </div>
                          <div
                            style={{
                              fontWeight: 600,
                              color: "#111827",
                              marginTop: "0.25rem",
                            }}
                          >
                            {s.subject || "—"}
                          </div>
                        </div>

                        <div>
                          <select
                            value={s.status}
                            onChange={(e) =>
                              updateSupportStatus(
                                s.user_id,
                                s.id,
                                e.target.value
                              )
                            }
                            style={{
                              width: "100%",
                              padding: "0.5rem",
                              borderRadius: "0.5rem",
                              border: `1.5px solid ${statusColor.border}`,
                              background: statusColor.bg,
                              color: statusColor.text,
                              fontWeight: 600,
                              fontSize: "0.85rem",
                              cursor: "pointer",
                            }}
                          >
                            <option value="Pending">Pending</option>
                            <option value="In Progress">In Progress</option>
                            <option value="Completed">Completed</option>
                          </select>
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div
                  style={{
                    background: "white",
                    padding: "2rem",
                    borderRadius: "0.75rem",
                    textAlign: "center",
                    color: "#9ca3af",
                  }}
                >
                  No support requests found
                </div>
              )}
            </div>
          </div>
        )}

        {/* STATISTICS TAB */}
        {activeTab === "stats" && (
          <div>
            <div style={{ marginBottom: "1.5rem" }}>
              <label
                style={{
                  fontWeight: 600,
                  color: "#111827",
                  marginRight: "1rem",
                  fontSize: "0.95rem",
                }}
              >
                Filter by Medication:
              </label>
              <select
                value={selectedMedication}
                onChange={(e) => setSelectedMedication(e.target.value)}
                style={{
                  padding: "0.5rem 0.75rem",
                  borderRadius: "0.5rem",
                  border: "1px solid #d1d5db",
                  fontSize: "0.9rem",
                  fontWeight: 500,
                  background: "white",
                }}
              >
                {medicationOptions.map((m) => (
                  <option key={m} value={m}>
                    {m === "all" ? "All Medications" : m}
                  </option>
                ))}
              </select>
            </div>

            {salesData.length > 0 ? (
              <div
                style={{
                  background: "white",
                  borderRadius: "0.75rem",
                  padding: "1.5rem",
                  boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
                }}
              >
                <h3
                  style={{
                    fontSize: "1.1rem",
                    fontWeight: 600,
                    color: "#111827",
                    marginBottom: "1.5rem",
                    textAlign: "center",
                  }}
                >
                  Sales of {selectedMedication === "all" ? "All Medications" : selectedMedication}
                </h3>
                <svg
                  width="100%"
                  height="400"
                  viewBox="0 0 800 400"
                  style={{
                    overflow: "visible",
                  }}
                >
                  {(() => {
                    const left = 70;
                    const top = 20;
                    const right = 40;
                    const bottom = 80;

                    const W = 800;
                    const H = 400;

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
                        {/* Y-axis */}
                        <line
                          x1={x0}
                          y1={y1}
                          x2={x0}
                          y2={y0}
                          stroke="#d1d5db"
                          strokeWidth="2"
                        />
                        {/* X-axis */}
                        <line
                          x1={x0}
                          y1={y0}
                          x2={x1}
                          y2={y0}
                          stroke="#d1d5db"
                          strokeWidth="2"
                        />

                        {/* Y-axis grid + labels */}
                        {ticks.map((t, i) => {
                          const y = y0 - t * plotH;
                          const value = Math.round(t * maxValue);
                          return (
                            <g key={i}>
                              <line
                                x1={x0}
                                y1={y}
                                x2={x1}
                                y2={y}
                                stroke="#f3f4f6"
                                strokeDasharray="2,2"
                              />
                              <line
                                x1={x0 - 6}
                                y1={y}
                                x2={x0}
                                y2={y}
                                stroke="#d1d5db"
                              />
                              <text
                                x={x0 - 10}
                                y={y + 4}
                                textAnchor="end"
                                fontSize="11"
                                fill="#6b7280"
                                fontWeight="500"
                              >
                                {value}
                              </text>
                            </g>
                          );
                        })}

                        {/* Gradient fill under line */}
                        <defs>
                          <linearGradient
                            id="areaGradient"
                            x1="0%"
                            y1="0%"
                            x2="0%"
                            y2="100%"
                          >
                            <stop
                              offset="0%"
                              stopColor="#4f46e5"
                              stopOpacity="0.2"
                            />
                            <stop
                              offset="100%"
                              stopColor="#4f46e5"
                              stopOpacity="0"
                            />
                          </linearGradient>
                        </defs>

                        {/* Area */}
                        <polygon
                          fill="url(#areaGradient)"
                          points={[
                            `${x0},${y0}`,
                            ...salesData.map(
                              (d, i) => `${xForIndex(i)},${yForValue(d.total)}`
                            ),
                            `${x1},${y0}`,
                          ].join(" ")}
                        />

                        {/* Line */}
                        <polyline
                          fill="none"
                          stroke="#4f46e5"
                          strokeWidth="3"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          points={salesData
                            .map((d, i) => `${xForIndex(i)},${yForValue(d.total)}`)
                            .join(" ")}
                        />

                        {/* Points + labels */}
                        {salesData.map((d, i) => {
                          const x = xForIndex(i);
                          const y = yForValue(d.total);
                          return (
                            <g key={d.month}>
                              <circle
                                cx={x}
                                cy={y}
                                r="4"
                                fill="white"
                                stroke="#4f46e5"
                                strokeWidth="2"
                              />
                              <text
                                x={x}
                                y={y - 12}
                                textAnchor="middle"
                                fontSize="10"
                                fontWeight="600"
                                fill="#111827"
                              >
                                {d.total}
                              </text>
                              <g transform={`translate(${x}, ${y0 + 15})`}>
                                <text
                                  x={0}
                                  y={0}
                                  textAnchor="start"
                                  fontSize="10"
                                  fill="#6b7280"
                                  transform="rotate(45)"
                                >
                                  {d.month}
                                </text>
                              </g>
                            </g>
                          );
                        })}
                      </>
                    );
                  })()}
                </svg>
              </div>
            ) : (
              <div
                style={{
                  background: "white",
                  padding: "2rem",
                  borderRadius: "0.75rem",
                  textAlign: "center",
                  color: "#9ca3af",
                }}
              >
                No sales data available
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({ label, value, icon }) {
  return (
    <div
      style={{
        background: "white",
        padding: "1.5rem",
        borderRadius: "0.75rem",
        border: "1px solid #e5e7eb",
        boxShadow: "0 1px 2px rgba(0,0,0,0.05)",
      }}
    >
      <div style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>{icon}</div>
      <div style={{ fontSize: "0.85rem", color: "#6b7280", fontWeight: 500 }}>
        {label}
      </div>
      <div
        style={{
          fontSize: "1.75rem",
          fontWeight: 700,
          color: "#111827",
          marginTop: "0.5rem",
        }}
      >
        {value}
      </div>
    </div>
  );
}