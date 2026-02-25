/**
 * ResultCard — displays the analysis result after a ticket is submitted.
 *
 * @param {{ result: Object | null }} props
 */
export default function ResultCard({ result }) {
    if (!result) return null;

    const priorityColor = {
        P0: "bg-red-500/20 text-red-400 border-red-500/30",
        P1: "bg-orange-500/20 text-orange-400 border-orange-500/30",
        P2: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
        P3: "bg-green-500/20 text-green-400 border-green-500/30",
    };

    const categoryIcon = {
        Billing: "💳",
        Technical: "🔧",
        Account: "👤",
        Feature: "✨",
        Other: "📋",
    };

    return (
        <div className="glass-card p-6 animate-slide-up">
            <h2 className="text-lg font-semibold text-white mb-5 flex items-center gap-2">
                <span className="inline-flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-600/20 text-emerald-400">
                    📊
                </span>
                Analysis Result
            </h2>

            {/* Stat grid */}
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
                {/* Category */}
                <div className="rounded-xl border border-white/10 bg-white/5 p-4 text-center">
                    <p className="text-xs font-medium uppercase tracking-wider text-gray-400">
                        Category
                    </p>
                    <p className="mt-1 text-2xl">
                        {categoryIcon[result.category] || "📋"}
                    </p>
                    <p className="mt-1 text-sm font-semibold text-white">
                        {result.category}
                    </p>
                </div>

                {/* Priority */}
                <div className="rounded-xl border border-white/10 bg-white/5 p-4 text-center">
                    <p className="text-xs font-medium uppercase tracking-wider text-gray-400">
                        Priority
                    </p>
                    <span
                        className={`mt-2 inline-block rounded-full border px-3 py-1 text-xs font-bold ${priorityColor[result.priority] || "bg-gray-500/20 text-gray-400"
                            }`}
                    >
                        {result.priority}
                    </span>
                </div>

                {/* Urgency */}
                <div className="rounded-xl border border-white/10 bg-white/5 p-4 text-center">
                    <p className="text-xs font-medium uppercase tracking-wider text-gray-400">
                        Urgency
                    </p>
                    <p className="mt-2 text-xl">
                        {result.urgency ? (
                            <span className="text-red-400 font-bold">🚨 Yes</span>
                        ) : (
                            <span className="text-gray-400">— No</span>
                        )}
                    </p>
                </div>

                {/* Confidence */}
                <div className="rounded-xl border border-white/10 bg-white/5 p-4 text-center">
                    <p className="text-xs font-medium uppercase tracking-wider text-gray-400">
                        Confidence
                    </p>
                    <p className="mt-2 text-xl font-bold text-brand-400">
                        {(result.confidence * 100).toFixed(0)}%
                    </p>
                </div>
            </div>

            {/* Keywords */}
            {result.keywords?.length > 0 && (
                <div className="mt-5">
                    <p className="text-xs font-medium uppercase tracking-wider text-gray-400 mb-2">
                        Matched Keywords
                    </p>
                    <div className="flex flex-wrap gap-2">
                        {result.keywords.map((kw, i) => (
                            <span
                                key={i}
                                className="rounded-full border border-brand-500/30 bg-brand-600/15 px-3 py-1
                           text-xs font-medium text-brand-300"
                            >
                                {kw}
                            </span>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
