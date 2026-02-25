"""
Rule-based NLP engine for support ticket analysis.

This module implements LOCAL keyword-based heuristic logic to classify
tickets by category, urgency, priority, and confidence — without any
external AI APIs.

Custom Rule:
    If the message contains "refund" OR "money back", the ticket is always
    classified as **Billing** with a minimum priority of **P1**.
"""

import re
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Keyword dictionaries
# ---------------------------------------------------------------------------

CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "Billing":    ["payment", "refund", "invoice", "charge", "billing",
                   "money back", "subscription", "pricing", "receipt"],
    "Technical":  ["error", "bug", "crash", "not working", "broken",
                   "failed", "glitch", "outage", "slow", "timeout",
                   "exception"],
    "Account":    ["login", "password", "account locked", "account",
                   "sign in", "signup", "register", "locked out",
                   "two factor", "2fa", "authentication"],
    "Feature":    ["request", "feature", "add option", "enhancement",
                   "suggestion", "wishlist", "improve", "would like"],
}

URGENCY_KEYWORDS: list[str] = [
    "urgent", "asap", "immediately", "down", "critical",
    "emergency", "right now", "escalate", "blocked",
]

P0_KEYWORDS: list[str] = ["system down", "security breach", "data loss", "outage"]
P1_KEYWORDS: list[str] = ["urgent", "critical", "immediately", "asap"]

# Custom-rule trigger phrases
CUSTOM_BILLING_TRIGGERS: list[str] = ["refund", "money back"]


# ---------------------------------------------------------------------------
# Analysis result data class
# ---------------------------------------------------------------------------

@dataclass
class AnalysisResult:
    """Structured output of the NLP analysis pipeline."""
    category: str = "Other"
    priority: str = "P3"
    urgency: bool = False
    keywords: list[str] = field(default_factory=list)
    confidence: float = 0.0


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def _normalize(text: str) -> str:
    """Lowercase and collapse whitespace for matching."""
    return re.sub(r"\s+", " ", text.lower().strip())


def classify_category(text: str) -> tuple[str, list[str]]:
    """
    Determine ticket category by counting keyword matches.

    Returns:
        (category_name, matched_keywords)
    """
    normalized = _normalize(text)
    scores: dict[str, list[str]] = {}

    for category, kws in CATEGORY_KEYWORDS.items():
        matched = [kw for kw in kws if kw in normalized]
        if matched:
            scores[category] = matched

    if not scores:
        return "Other", []

    # Pick category with the most keyword matches
    best = max(scores, key=lambda c: len(scores[c]))
    return best, scores[best]


def detect_urgency(text: str) -> tuple[bool, list[str]]:
    """Return (is_urgent, matched_urgency_keywords)."""
    normalized = _normalize(text)
    matched = [kw for kw in URGENCY_KEYWORDS if kw in normalized]
    return bool(matched), matched


def determine_priority(
    text: str,
    category: str,
    is_urgent: bool,
) -> str:
    """
    Assign priority level (P0–P3).

    - P0: system down / security breach
    - P1: urgent + issue
    - P2: normal issue
    - P3: feature request / other
    """
    normalized = _normalize(text)

    # P0 — critical system events
    if any(kw in normalized for kw in P0_KEYWORDS):
        return "P0"

    # P1 — urgent issues
    if is_urgent or any(kw in normalized for kw in P1_KEYWORDS):
        return "P1"

    # P2 — non-urgent issues in actionable categories
    if category in ("Billing", "Technical", "Account"):
        return "P2"

    # P3 — feature requests and everything else
    return "P3"


def calculate_confidence(
    matched_keywords: list[str],
    urgency_keywords: list[str],
    category: str,
) -> float:
    """
    Heuristic confidence score between 0 and 1.

    Higher when more keywords match and category is not 'Other'.
    """
    total_matches = len(matched_keywords) + len(urgency_keywords)

    if total_matches == 0:
        return 0.3  # Minimum baseline for "Other"

    # Sigmoid-like scaling: more matches → higher confidence
    raw = min(total_matches / 5.0, 1.0)
    base = 0.5 + (raw * 0.45)  # Range: 0.50 – 0.95

    # Small boost for non-Other categories
    if category != "Other":
        base = min(base + 0.05, 1.0)

    return round(base, 2)


def _apply_custom_rules(
    text: str,
    result: AnalysisResult,
) -> AnalysisResult:
    """
    **Custom Rule (required by assignment):**
    If the message contains "refund" OR "money back":
      → category = Billing
      → priority = at least P1

    This rule runs AFTER standard classification to ensure it overrides
    any conflicting result.
    """
    normalized = _normalize(text)

    if any(trigger in normalized for trigger in CUSTOM_BILLING_TRIGGERS):
        result.category = "Billing"
        # Escalate priority to at least P1 (keep P0 if already set)
        if result.priority not in ("P0",):
            result.priority = "P1"
        # Ensure trigger keywords appear in the extracted list
        for trigger in CUSTOM_BILLING_TRIGGERS:
            if trigger in normalized and trigger not in result.keywords:
                result.keywords.append(trigger)

    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_ticket(message: str) -> AnalysisResult:
    """
    Full analysis pipeline for a support ticket message.

    Steps:
        1. Classify category via keyword matching
        2. Detect urgency
        3. Determine priority
        4. Calculate confidence
        5. Apply custom rules (refund / money back override)

    Returns:
        AnalysisResult dataclass with all fields populated.
    """
    category, cat_keywords = classify_category(message)
    is_urgent, urg_keywords = detect_urgency(message)
    priority = determine_priority(message, category, is_urgent)

    all_keywords = list(dict.fromkeys(cat_keywords + urg_keywords))  # Deduplicate, preserve order
    confidence = calculate_confidence(cat_keywords, urg_keywords, category)

    result = AnalysisResult(
        category=category,
        priority=priority,
        urgency=is_urgent,
        keywords=all_keywords,
        confidence=confidence,
    )

    # Apply custom business rules last so they can override
    result = _apply_custom_rules(message, result)

    return result
