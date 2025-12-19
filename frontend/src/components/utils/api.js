const API_BASE = "http://localhost:8000";

// Helper function for API calls with error handling
async function apiCall(url, options = {}) {
  try {
    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response;
  } catch (error) {
    console.error(`API Error: ${error.message}`);
    throw error;
  }
}

export const api = {
  // ============================================================
  // USERS
  // ============================================================
  async fetchUsers() {
    try {
      const res = await apiCall(`${API_BASE}/users`);
      const data = await res.json();
      return data.data;
    } catch (error) {
      console.error("Failed to fetch users:", error);
      throw error;
    }
  },

  async fetchUser(userId) {
    try {
      const res = await apiCall(`${API_BASE}/users/${userId}`);
      const data = await res.json();
      return data.data;
    } catch (error) {
      console.error("Failed to fetch user:", error);
      throw error;
    }
  },

  // ============================================================
  // PRESCRIPTIONS
  // ============================================================
  async fetchPrescriptionRequests(userId, status = null, limit = 50, offset = 0) {
    try {
      let url = `${API_BASE}/users/${userId}/prescriptions?limit=${limit}&offset=${offset}`;
      if (status) {
        url += `&status_filter=${status}`;
      }

      const res = await apiCall(url);
      const data = await res.json();
      return data.data;
    } catch (error) {
      console.error("Failed to fetch prescriptions:", error);
      throw error;
    }
  },

  async fetchPrescription(userId, prescriptionId) {
    try {
      const res = await apiCall(
        `${API_BASE}/users/${userId}/prescriptions/${prescriptionId}`
      );
      const data = await res.json();
      return data.data;
    } catch (error) {
      console.error("Failed to fetch prescription:", error);
      throw error;
    }
  },

  async updatePrescriptionStatus(userId, prescriptionId, status) {
    try {
      const res = await apiCall(
        `${API_BASE}/users/${userId}/prescriptions/${prescriptionId}/status`,
        {
          method: "PATCH",
          body: JSON.stringify({ status }),
        }
      );
      const data = await res.json();
      return data.data;
    } catch (error) {
      console.error("Failed to update prescription status:", error);
      throw error;
    }
  },

  // ============================================================
  // SUPPORT REQUESTS
  // ============================================================
  async fetchSupportRequests(userId, status = null, limit = 50, offset = 0) {
    try {
      let url = `${API_BASE}/users/${userId}/support-tickets?limit=${limit}&offset=${offset}`;
      if (status) {
        url += `&status_filter=${status}`;
      }

      const res = await apiCall(url);
      const data = await res.json();
      return data.data;
    } catch (error) {
      console.error("Failed to fetch support requests:", error);
      throw error;
    }
  },

  async fetchSupportTicket(userId, ticketId) {
    try {
      const res = await apiCall(
        `${API_BASE}/users/${userId}/support-tickets/${ticketId}`
      );
      const data = await res.json();
      return data.data;
    } catch (error) {
      console.error("Failed to fetch support ticket:", error);
      throw error;
    }
  },

  async updateSupportStatus(userId, ticketId, status) {
    try {
      const res = await apiCall(
        `${API_BASE}/users/${userId}/support-tickets/${ticketId}/status`,
        {
          method: "PATCH",
          body: JSON.stringify({ status }),
        }
      );
      const data = await res.json();
      return data.data;
    } catch (error) {
      console.error("Failed to update support status:", error);
      throw error;
    }
  },

  // ============================================================
  // PHARMACIST
  // ============================================================
  async fetchPharmacistDashboard(userId) {
    try {
      const res = await apiCall(
        `${API_BASE}/pharmacist/dashboard?user_id=${userId}`
      );
      const data = await res.json();
      return data.data;
    } catch (error) {
      console.error("Failed to fetch pharmacist dashboard:", error);
      throw error;
    }
  },

  async fetchAllPrescriptions(userId, status = null, limit = 50, offset = 0) {
    try {
      let url = `${API_BASE}/pharmacist/prescriptions?user_id=${userId}&limit=${limit}&offset=${offset}`;
      if (status) {
        url += `&status_filter=${status}`;
      }

      const res = await apiCall(url);
      const data = await res.json();
      return data.data;
    } catch (error) {
      console.error("Failed to fetch all prescriptions:", error);
      throw error;
    }
  },

  // ============================================================
  // CHAT
  // ============================================================
  async sendMessage(payload) {
    try {
      const res = await apiCall(`${API_BASE}/chat`, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      return res;
    } catch (error) {
      console.error("Failed to send message:", error);
      throw error;
    }
  },

  // ============================================================
  // HEALTH
  // ============================================================
  async healthCheck() {
    try {
      const res = await apiCall(`${API_BASE}/health`);
      return res.ok;
    } catch (error) {
      console.error("Health check failed:", error);
      return false;
    }
  },
};