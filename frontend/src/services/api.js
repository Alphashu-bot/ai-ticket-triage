/**
 * Axios-based API client for the AI Ticket Triage backend.
 *
 * In Docker the Vite dev server proxies /tickets → backend:8000.
 * For plain local dev, adjust VITE_API_URL in a .env file.
 */

import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "",
    headers: { "Content-Type": "application/json" },
    timeout: 15_000,
});

/**
 * POST /tickets/analyze
 * @param {string} message - Raw support ticket text.
 * @returns {Promise<Object>} Analysis result.
 */
export const analyzeTicket = async (message) => {
    const { data } = await api.post("/tickets/analyze", { message });
    return data;
};

/**
 * GET /tickets
 * @returns {Promise<Array>} List of all analyzed tickets (newest first).
 */
export const fetchTickets = async () => {
    const { data } = await api.get("/tickets");
    return data;
};

export default api;
