# Evaluation Metrics

This document describes each metric produced by the News2Signal evaluator, its meaning, limitations, and how to interpret it.

---

## Coverage

**Formula:** `matched_rows / total_dataset_rows`

**Meaning:** The fraction of dataset examples that have a corresponding prediction.

**Interpretation:** A model that skips hard examples and only predicts on easy ones may appear to score higher on other metrics. Always report coverage alongside accuracy metrics to detect selective prediction.

**Limitations:** Does not distinguish between intentional abstentions and missing predictions.

---

## Direction Accuracy

**Formula:** `correct_direction_count / matched_rows`

**Meaning:** The fraction of matched rows where `predicted_direction` exactly matches `expected_direction`.

**Interpretation:** This is the primary signal quality metric. A random baseline over four classes achieves ~25%. A model that always predicts `bearish` would score approximately the bearish base rate in the dataset.

**Limitations:**
- Does not credit near-misses (e.g., predicting `neutral` when the answer is `mixed`)
- Does not weight by confidence label (a `high`-confidence label is weighted the same as `low`)
- Does not measure calibration

---

## Event Type Accuracy

**Formula:** `correct_event_type_count / matched_rows`

**Meaning:** The fraction of matched rows where `predicted_event_type` exactly matches `event_type`.

**Interpretation:** Measures whether the model correctly identifies the type of market event, independently of whether it gets the direction right. A model can have high direction accuracy but low event type accuracy by getting lucky on direction.

**Limitations:** Event types are not hierarchically scored. Predicting `guidance` when the label is `earnings` is penalized the same as predicting `geopolitical`.

---

## Asset Match Accuracy

**Formula:** `correct_asset_count / matched_rows`

**Meaning:** The fraction of matched rows where `predicted_asset` exactly matches `asset`.

**Interpretation:** Measures whether the model correctly identifies the primary affected asset. This is a string exact-match and is case-sensitive.

**Limitations:**
- Does not credit economically equivalent assets (e.g., `SPY` vs. `^GSPC`)
- Does not credit closely related assets (e.g., `XBI` vs. `IBB`)
- Ticker conventions may differ between models and the dataset

---

## Time Horizon Accuracy

**Formula:** `correct_time_horizon_count / matched_rows`

**Meaning:** The fraction of matched rows where `predicted_time_horizon` exactly matches `time_horizon`.

**Interpretation:** Measures whether the model correctly identifies the relevant time window for the signal. Time horizon is often the hardest label to get right because it requires reasoning about implementation lags, market pricing speed, and causal mechanism duration.

**Limitations:** Adjacent horizons (e.g., `short_term` vs. `medium_term`) are penalized the same as distant horizons (e.g., `intraday` vs. `long_term`). A partial-credit version of this metric would be more informative but is not currently implemented.

---

## Exact Row Match

**Formula:** `exact_match_count / matched_rows`

Where `exact_match` requires all four fields to be correct simultaneously:
- `expected_direction == predicted_direction`
- `event_type == predicted_event_type`
- `asset == predicted_asset`
- `time_horizon == predicted_time_horizon`

**Meaning:** The most demanding summary metric. Measures the fraction of rows where the model gets everything right at once.

**Interpretation:** This metric is intentionally strict. Even a good model will typically score below 60% on exact row match because a single field error nullifies the row. It is most useful for comparing two models against the same dataset rather than as an absolute quality measure.

**Why this matters:** In practice, a signal is only actionable if direction, asset, and horizon are all correct simultaneously. Getting direction right but horizon wrong could lead to a trade that is correct in theory but wrong in timing.

---

## Average Reasoning Score

**Formula:** `sum(reasoning_score) / count(rows with reasoning_score)`

**Range:** 1 to 5

**Meaning:** The average self-reported quality score for the model's reasoning on each prediction. This is provided by the model itself (or by a human reviewer annotating prediction quality).

**Interpretation:** A higher average score suggests the model is more confident and more articulate in its explanations. However, this metric is self-reported and should be treated with caution.

**Limitations:**
- Self-reported scores are not ground truth
- A model can score 5 on reasoning while getting the direction wrong
- Different models may interpret the 1–5 scale differently
- No verification that the reasoning actually supports the predicted label

---

## Missing Prediction IDs

**Meaning:** Dataset rows for which no prediction was provided.

**Use:** Identifies whether a model skipped certain examples and helps diagnose coverage gaps.

---

## Invalid Prediction IDs

**Meaning:** Prediction rows whose IDs do not appear in the dataset.

**Use:** Detects alignment errors between prediction and dataset files, such as ID format mismatches or predictions run on a different dataset version.

---

## Top Mismatches

**Meaning:** The first N direction and event type mismatches by dataset row order.

**Use:** Useful for qualitative error analysis — understanding which types of news the model systematically misclassifies.
