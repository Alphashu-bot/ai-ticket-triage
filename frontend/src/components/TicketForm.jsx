import { useState } from "react";

/**
 * TicketForm — textarea + submit button with loading state.
 *
 * @param {{ onSubmit: (msg: string) => Promise<void> }} props
 */
export default function TicketForm({ onSubmit }) {
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!message.trim()) return;

        setLoading(true);
        try {
            await onSubmit(message.trim());
            setMessage("");
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="glass-card p-6 animate-fade-in">
            {/* Header */}
            <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <span className="inline-flex h-8 w-8 items-center justify-center rounded-lg bg-brand-600/20 text-brand-400">
                    ✉
                </span>
                Submit a Ticket
            </h2>

            {/* Textarea */}
            <textarea
                id="ticket-message"
                rows={4}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Describe your issue…"
                className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3
                   text-sm text-gray-200 placeholder-gray-500 outline-none
                   transition focus:border-brand-500 focus:ring-2 focus:ring-brand-500/30
                   resize-none"
            />

            {/* Submit */}
            <button
                type="submit"
                disabled={loading || !message.trim()}
                className="mt-4 w-full rounded-xl bg-gradient-to-r from-brand-600 to-brand-500
                   px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-brand-600/25
                   transition hover:shadow-brand-500/40 hover:brightness-110
                   disabled:cursor-not-allowed disabled:opacity-50"
            >
                {loading ? (
                    <span className="flex items-center justify-center gap-2">
                        <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
                        </svg>
                        Analyzing…
                    </span>
                ) : (
                    "Analyze Ticket"
                )}
            </button>
        </form>
    );
}
