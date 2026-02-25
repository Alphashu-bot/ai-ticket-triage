import { useState, useEffect, useCallback } from "react";
import { analyzeTicket, fetchTickets } from "../services/api";
import TicketForm from "../components/TicketForm";
import ResultCard from "../components/ResultCard";
import TicketHistory from "../components/TicketHistory";

/**
 * Dashboard — single-page layout with ticket form, result card, and history table.
 */
export default function Dashboard() {
    const [result, setResult] = useState(null);
    const [tickets, setTickets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fetch ticket history on mount
    const loadTickets = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await fetchTickets();
            setTickets(data);
        } catch (err) {
            setError("Failed to load ticket history. Is the backend running?");
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadTickets();
    }, [loadTickets]);

    // Handle new ticket submission
    const handleSubmit = async (message) => {
        setError(null);
        try {
            const analysis = await analyzeTicket(message);
            setResult(analysis);
            // Refresh history
            await loadTickets();
        } catch (err) {
            setError("Failed to analyze ticket. Please try again.");
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950">
            {/* Header */}
            <header className="border-b border-white/5 bg-white/[0.02] backdrop-blur-sm">
                <div className="mx-auto flex max-w-5xl items-center gap-3 px-6 py-5">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl
                          bg-gradient-to-br from-brand-500 to-brand-700 text-lg shadow-lg shadow-brand-600/30">
                        🧠
                    </div>
                    <div>
                        <h1 className="text-xl font-bold text-white tracking-tight">
                            AI Ticket Triage
                        </h1>
                        <p className="text-xs text-gray-400">
                            Local NLP-powered support ticket analysis
                        </p>
                    </div>
                </div>
            </header>

            {/* Main content */}
            <main className="mx-auto max-w-5xl space-y-8 px-6 py-10">
                {/* Section 1: Form */}
                <TicketForm onSubmit={handleSubmit} />

                {/* Section 2: Result card */}
                <ResultCard result={result} />

                {/* Section 3: Ticket history */}
                <TicketHistory tickets={tickets} loading={loading} error={error} />
            </main>

            {/* Footer */}
            <footer className="border-t border-white/5 py-6 text-center text-xs text-gray-600">
                AI Ticket Triage &copy; {new Date().getFullYear()} — Built with FastAPI + React
            </footer>
        </div>
    );
}
