"""Allowed label values and field definitions for the News2Signal schema."""

from __future__ import annotations

VALID_DIRECTIONS: frozenset[str] = frozenset({
    "bullish", "bearish", "neutral", "mixed"
})

VALID_TIME_HORIZONS: frozenset[str] = frozenset({
    "intraday", "short_term", "medium_term", "long_term"
})

VALID_CONFIDENCE_LABELS: frozenset[str] = frozenset({
    "low", "medium", "high"
})

VALID_EVENT_TYPES: frozenset[str] = frozenset({
    "central_bank", "inflation", "earnings", "guidance", "regulatory",
    "geopolitical", "supply_chain", "labor_market", "merger_acquisition",
    "product_launch", "credit_risk", "commodity", "crypto_policy",
    "housing", "consumer_demand", "fiscal_policy",
})

VALID_ASSET_TYPES: frozenset[str] = frozenset({
    "equity", "equity_index", "bond", "fx", "commodity",
    "crypto", "sector_etf", "macro_proxy",
})

REQUIRED_DATASET_FIELDS: frozenset[str] = frozenset({
    "id", "headline", "summary", "asset", "asset_type", "sector",
    "event_type", "expected_direction", "time_horizon", "confidence_label",
    "reasoning", "not_financial_advice",
})

REQUIRED_PREDICTION_FIELDS: frozenset[str] = frozenset({
    "id", "predicted_direction", "predicted_event_type",
    "predicted_asset", "predicted_time_horizon",
})

REASONING_SCORE_MIN = 1
REASONING_SCORE_MAX = 5
