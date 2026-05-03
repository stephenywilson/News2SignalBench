"""Scoring metrics for News2Signal evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EvalResult:
    total_dataset: int = 0
    total_predictions: int = 0
    matched: int = 0  # rows where dataset id has a prediction

    direction_correct: int = 0
    event_type_correct: int = 0
    asset_correct: int = 0
    time_horizon_correct: int = 0
    exact_match: int = 0

    reasoning_scores: list[float] = field(default_factory=list)

    missing_ids: list[str] = field(default_factory=list)
    invalid_ids: list[str] = field(default_factory=list)

    direction_mismatches: list[dict] = field(default_factory=list)
    event_type_mismatches: list[dict] = field(default_factory=list)

    def coverage(self) -> float:
        if self.total_dataset == 0:
            return 0.0
        return self.matched / self.total_dataset

    def direction_accuracy(self) -> float:
        if self.matched == 0:
            return 0.0
        return self.direction_correct / self.matched

    def event_type_accuracy(self) -> float:
        if self.matched == 0:
            return 0.0
        return self.event_type_correct / self.matched

    def asset_accuracy(self) -> float:
        if self.matched == 0:
            return 0.0
        return self.asset_correct / self.matched

    def time_horizon_accuracy(self) -> float:
        if self.matched == 0:
            return 0.0
        return self.time_horizon_correct / self.matched

    def exact_match_rate(self) -> float:
        if self.matched == 0:
            return 0.0
        return self.exact_match / self.matched

    def avg_reasoning_score(self) -> float | None:
        if not self.reasoning_scores:
            return None
        return sum(self.reasoning_scores) / len(self.reasoning_scores)

    def to_dict(self) -> dict:
        return {
            "total_dataset_rows": self.total_dataset,
            "total_prediction_rows": self.total_predictions,
            "matched_rows": self.matched,
            "coverage": round(self.coverage(), 4),
            "direction_accuracy": round(self.direction_accuracy(), 4),
            "event_type_accuracy": round(self.event_type_accuracy(), 4),
            "asset_match_accuracy": round(self.asset_accuracy(), 4),
            "time_horizon_accuracy": round(self.time_horizon_accuracy(), 4),
            "exact_row_match_rate": round(self.exact_match_rate(), 4),
            "avg_reasoning_score": (
                round(self.avg_reasoning_score(), 4)
                if self.avg_reasoning_score() is not None
                else None
            ),
            "missing_prediction_ids": self.missing_ids,
            "invalid_prediction_ids": self.invalid_ids,
            "top_direction_mismatches": self.direction_mismatches[:10],
            "top_event_type_mismatches": self.event_type_mismatches[:10],
        }


def compute_metrics(
    dataset: list[dict],
    predictions: list[dict],
) -> EvalResult:
    result = EvalResult(
        total_dataset=len(dataset),
        total_predictions=len(predictions),
    )

    pred_index: dict[str, dict] = {p["id"]: p for p in predictions}
    dataset_ids: set[str] = {row["id"] for row in dataset}

    # Track prediction ids that don't appear in dataset
    for pid in pred_index:
        if pid not in dataset_ids:
            result.invalid_ids.append(pid)

    for row in dataset:
        row_id = row["id"]
        pred = pred_index.get(row_id)

        if pred is None:
            result.missing_ids.append(row_id)
            continue

        result.matched += 1

        dir_ok = row["expected_direction"] == pred.get("predicted_direction")
        evt_ok = row["event_type"] == pred.get("predicted_event_type")
        ast_ok = row["asset"] == pred.get("predicted_asset")
        hor_ok = row["time_horizon"] == pred.get("predicted_time_horizon")

        if dir_ok:
            result.direction_correct += 1
        else:
            result.direction_mismatches.append({
                "id": row_id,
                "expected": row["expected_direction"],
                "predicted": pred.get("predicted_direction"),
            })

        if evt_ok:
            result.event_type_correct += 1
        else:
            result.event_type_mismatches.append({
                "id": row_id,
                "expected": row["event_type"],
                "predicted": pred.get("predicted_event_type"),
            })

        if ast_ok:
            result.asset_correct += 1

        if hor_ok:
            result.time_horizon_correct += 1

        if dir_ok and evt_ok and ast_ok and hor_ok:
            result.exact_match += 1

        score = pred.get("reasoning_score")
        if score is not None:
            try:
                result.reasoning_scores.append(float(score))
            except (TypeError, ValueError):
                pass

    return result
