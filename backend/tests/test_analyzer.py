"""
Unit tests for the NLP analyzer engine.

Covers:
    - Category classification
    - Urgency detection
    - Priority determination
    - Confidence calculation
    - Custom refund / money-back rule
    - Full pipeline integration
"""

import pytest

from app.analyzer.nlp_engine import (
    analyze_ticket,
    classify_category,
    detect_urgency,
    determine_priority,
    calculate_confidence,
)


# ===================================================================
# Category Classification Tests
# ===================================================================

class TestClassifyCategory:
    """Tests for keyword-based category classification."""

    def test_billing_keywords(self):
        category, keywords = classify_category("my payment failed")
        assert category == "Billing"
        assert "payment" in keywords

    def test_technical_keywords(self):
        category, keywords = classify_category("the app is crashing with error")
        assert category == "Technical"
        assert "crash" in keywords or "error" in keywords

    def test_account_keywords(self):
        category, keywords = classify_category("I can't login to my account")
        assert category == "Account"
        assert "login" in keywords or "account" in keywords

    def test_feature_keywords(self):
        category, keywords = classify_category("please add option for dark mode")
        assert category == "Feature"
        assert "add option" in keywords

    def test_other_category(self):
        category, keywords = classify_category("hello there, good morning")
        assert category == "Other"
        assert keywords == []

    def test_multiple_category_keywords_picks_best(self):
        # "payment" + "invoice" = 2 Billing matches vs 1 Technical
        category, _ = classify_category("payment invoice error")
        assert category == "Billing"

    def test_case_insensitive(self):
        category, _ = classify_category("MY PAYMENT FAILED")
        assert category == "Billing"


# ===================================================================
# Urgency Detection Tests
# ===================================================================

class TestDetectUrgency:
    """Tests for urgency keyword detection."""

    def test_urgent_detected(self):
        is_urgent, kws = detect_urgency("this is urgent, fix now")
        assert is_urgent is True
        assert "urgent" in kws

    def test_critical_detected(self):
        is_urgent, _ = detect_urgency("critical issue in production")
        assert is_urgent is True

    def test_no_urgency(self):
        is_urgent, kws = detect_urgency("just a question about pricing")
        assert is_urgent is False
        assert kws == []

    def test_multiple_urgency_keywords(self):
        is_urgent, kws = detect_urgency("urgent and critical, system is down")
        assert is_urgent is True
        assert len(kws) >= 2


# ===================================================================
# Priority Determination Tests
# ===================================================================

class TestDeterminePriority:
    """Tests for rule-based priority assignment."""

    def test_p0_system_down(self):
        priority = determine_priority("system down, nothing works", "Technical", True)
        assert priority == "P0"

    def test_p0_security_breach(self):
        priority = determine_priority("security breach detected", "Technical", False)
        assert priority == "P0"

    def test_p1_urgent(self):
        priority = determine_priority("please fix this", "Technical", True)
        assert priority == "P1"

    def test_p2_normal_billing(self):
        priority = determine_priority("invoice question", "Billing", False)
        assert priority == "P2"

    def test_p2_normal_technical(self):
        priority = determine_priority("small bug in settings", "Technical", False)
        assert priority == "P2"

    def test_p3_feature_request(self):
        priority = determine_priority("can you add dark mode", "Feature", False)
        assert priority == "P3"

    def test_p3_other(self):
        priority = determine_priority("hello world", "Other", False)
        assert priority == "P3"


# ===================================================================
# Confidence Calculation Tests
# ===================================================================

class TestCalculateConfidence:
    """Tests for heuristic confidence scoring."""

    def test_no_matches_returns_baseline(self):
        score = calculate_confidence([], [], "Other")
        assert score == 0.3

    def test_more_matches_higher_confidence(self):
        low = calculate_confidence(["payment"], [], "Billing")
        high = calculate_confidence(["payment", "invoice", "charge"], ["urgent"], "Billing")
        assert high > low

    def test_confidence_between_0_and_1(self):
        score = calculate_confidence(
            ["payment", "invoice", "refund"], ["urgent", "critical"], "Billing"
        )
        assert 0.0 <= score <= 1.0

    def test_non_other_category_boost(self):
        other = calculate_confidence(["payment"], [], "Other")
        billing = calculate_confidence(["payment"], [], "Billing")
        assert billing > other


# ===================================================================
# Custom Rule Tests
# ===================================================================

class TestCustomRefundRule:
    """Tests for the custom refund / money-back business rule."""

    def test_refund_forces_billing(self):
        result = analyze_ticket("I need a refund for my order")
        assert result.category == "Billing"

    def test_refund_forces_at_least_p1(self):
        result = analyze_ticket("I need a refund for my order")
        assert result.priority in ("P0", "P1")

    def test_money_back_forces_billing(self):
        result = analyze_ticket("I want my money back please")
        assert result.category == "Billing"

    def test_money_back_forces_at_least_p1(self):
        result = analyze_ticket("give me my money back")
        assert result.priority in ("P0", "P1")

    def test_refund_keyword_in_extracted_keywords(self):
        result = analyze_ticket("need a refund now")
        assert "refund" in result.keywords


# ===================================================================
# Full Pipeline Integration Tests
# ===================================================================

class TestAnalyzeTicketPipeline:
    """End-to-end tests for the analyze_ticket function."""

    def test_billing_urgent(self):
        result = analyze_ticket("my payment failed and this is urgent")
        assert result.category == "Billing"
        assert result.urgency is True
        assert result.priority == "P1"
        assert result.confidence > 0.5
        assert "payment" in result.keywords

    def test_technical_crash(self):
        result = analyze_ticket("the application crashes on startup")
        assert result.category == "Technical"
        assert "crash" in result.keywords

    def test_account_locked(self):
        result = analyze_ticket("my account is locked and I cannot login")
        assert result.category == "Account"

    def test_feature_request(self):
        result = analyze_ticket("would like a dark mode feature")
        assert result.category == "Feature"
        assert result.priority == "P3"

    def test_generic_message(self):
        result = analyze_ticket("hello, is anyone there?")
        assert result.category == "Other"
        assert result.priority == "P3"
        assert result.urgency is False
