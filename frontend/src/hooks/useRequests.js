import { useState, useCallback } from "react";
import { api } from "../components/utils/api.js";

export function useRequests(activeUser) {
  const [prescriptionRequests, setPrescriptionRequests] = useState([]);
  const [supportRequests, setSupportRequests] = useState([]);
  const [medicationsSold, setMedicationsSold] = useState([]);
  const [loading, setLoading] = useState(false);

  const refresh = useCallback(async () => {
    // Don't proceed if no active user
    if (!activeUser || !activeUser.id) {
      console.warn("No active user or user ID");
      return;
    }

    setLoading(true);
    try {
      if (activeUser.role === "pharmacist") {
        // Fetch pharmacist dashboard
        console.log("Fetching pharmacist dashboard for user:", activeUser.id);
        const dashboard = await api.fetchPharmacistDashboard(activeUser.id);

        setPrescriptionRequests(dashboard.prescriptions || []);
        setSupportRequests(dashboard.support_requests || []);
        setMedicationsSold(dashboard.medications_sold || []);

        console.log("Dashboard loaded:", dashboard);
      } else {
        // Fetch user-specific requests
        console.log("Fetching user requests for:", activeUser.id);
        const [pres, sup] = await Promise.all([
          api.fetchPrescriptionRequests(activeUser.id),
          api.fetchSupportRequests(activeUser.id),
        ]);

        setPrescriptionRequests(pres || []);
        setSupportRequests(sup || []);
        setMedicationsSold([]);

        console.log("User requests loaded - Prescriptions:", pres, "Support:", sup);
      }
    } catch (error) {
      console.error("Failed to fetch requests:", error);
      setPrescriptionRequests([]);
      setSupportRequests([]);
      setMedicationsSold([]);
    } finally {
      setLoading(false);
    }
  }, [activeUser]);

  return {
    prescriptionRequests,
    supportRequests,
    medicationsSold,
    loading,
    refresh,
  };
}