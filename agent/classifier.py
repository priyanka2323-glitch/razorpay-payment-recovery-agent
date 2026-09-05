CLASSIFICATION_MAP = {
    "insufficient_funds": {"severity": "medium", "retryable": True},
    "expired_card": {"severity": "high", "retryable": False},  # needs new card, not retry
    "bank_timeout": {"severity": "low", "retryable": True},
    "do_not_honor": {"severity": "high", "retryable": False},
}

def classify_failure(failure_code):
    return CLASSIFICATION_MAP.get(failure_code, {"severity": "medium", "retryable": True})