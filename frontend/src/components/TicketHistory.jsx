/**
 * TicketHistory — table showing all previously analyzed tickets.
 *
 * Handles loading, empty state, and error state.
 *
 * @param {{ tickets: Array, loading: boolean, error: string|null }} props
 */
export default function TicketHistory({ tickets, loading, error }) {
    const priorityColor = {
        P0: "text-red-400",
        P1: "text-orange-400",
        P2: "text-yellow-400",
        P3: "text-green-400",
    };

    return (
        <div className="glass-card p-6 animate-fade-in">
            <h2 className="text-lg font-semibold text-white mb-5 flex items-center gap-2">
                <span className="inline-flex h-8 w-8 items-center justify-center rounded-lg bg-purple-600/20 text-purple-400">
                    📜
                </span>
                Ticket History
            </h2>

            {/* Loading */}
            {loading && (
                <div className="flex items-center justify-center py-12">
                    <svg className="h-6 w-6 animate-spin text-brand-400" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
                    </svg>
                    <span className="ml-3 text-sm text-gray-400">Loading tickets…</span>
                </div>
            )}

            {/* Error */}
            {error && !loading && (
                <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-400">
                    ⚠️ {error}
                </div>
            )}

            {/* Empty */}
            {!loading && !error && tickets.length === 0 && (
                <div className="py-12 text-center text-gray-500 text-sm">
                    No tickets analyzed yet. Submit one above to get started!
                </div>
            )}

            {/* Table */}
            {!loading && !error && tickets.length > 0 && (
                <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left">
                        <thead>
                            <tr className="border-b border-white/10 text-xs uppercase tracking-wider text-gray-400">
                                <th className="py-3 px-4">Message</th>
                                <th className="py-3 px-4">Category</th>
                                <th className="py-3 px-4">Priority</th>
                                <th className="py-3 px-4">Urgency</th>
                                <th className="py-3 px-4">Confidence</th>
                                <th className="py-3 px-4">Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tickets.map((t) => (
                                <tr
                                    key={t.id}
                                    className="border-b border-white/5 transition hover:bg-white/5"
                                >
                                    <td className="py-3 px-4 max-w-[260px] truncate text-gray-300">
                                        {t.message}
                                    </td>
                                    <td className="py-3 px-4 text-gray-200 font-medium">{t.category}</td>
                                    <td className="py-3 px-4">
                                        <span className={`font-bold ${priorityColor[t.priority] || "text-gray-400"}`}>
                                            {t.priority}
                                        </span>
                                    </td>
                                    <td className="py-3 px-4">
                                        {t.urgency ? (
                                            <span className="text-red-400 font-semibold">Yes</span>
                                        ) : (
                                            <span className="text-gray-500">No</span>
                                        )}
                                    </td>
                                    <td className="py-3 px-4 text-brand-400 font-medium">
                                        {(t.confidence * 100).toFixed(0)}%
                                    </td>
                                    <td className="py-3 px-4 text-gray-500 whitespace-nowrap">
                                        {new Date(t.created_at).toLocaleDateString("en-US", {
                                            month: "short",
                                            day: "numeric",
                                            year: "numeric",
                                            hour: "2-digit",
                                            minute: "2-digit",
                                        })}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
