"""Validation for dataset and prediction JSONL files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import NamedTuple

from .io import iter_jsonl
from .schema import (
    REQUIRED_DATASET_FIELDS,
    REQUIRED_PREDICTION_FIELDS,
    VALID_DIRECTIONS,
    VALID_TIME_HORIZONS,
    VALID_CONFIDENCE_LABELS,
    VALID_EVENT_TYPES,
    VALID_ASSET_TYPES,
    REASONING_SCORE_MIN,
    REASONING_SCORE_MAX,
)


class ValidationError(NamedTuple):
    row: int
    record_id: str | None
    field: str
    message: str

    def __str__(self) -> str:
        loc = f"row {self.row}" + (f" id={self.record_id!r}" if self.record_id else "")
        return f"  [{loc}] {self.field}: {self.message}"


def validate_dataset(path: str | Path) -> list[ValidationError]:
    errors: list[ValidationError] = []
    seen_ids: dict[str, int] = {}

    for lineno, row in enumerate(iter_jsonl(path), start=1):
        rid = row.get("id")

        missing = REQUIRED_DATASET_FIELDS - set(row.keys())
        for f in sorted(missing):
            errors.append(ValidationError(lineno, rid, f, "required field missing"))

        if missing:
            continue  # skip value checks if fields are missing

        if rid in seen_ids:
            errors.append(ValidationError(
                lineno, rid, "id",
                f"duplicate id (first seen at row {seen_ids[rid]})"
            ))
        else:
            seen_ids[rid] = lineno

        dir_val = row.get("expected_direction")
        if dir_val not in VALID_DIRECTIONS:
            errors.append(ValidationError(
                lineno, rid, "expected_direction",
                f"invalid value {dir_val!r}; allowed: {sorted(VALID_DIRECTIONS)}"
            ))

        hor_val = row.get("time_horizon")
        if hor_val not in VALID_TIME_HORIZONS:
            errors.append(ValidationError(
                lineno, rid, "time_horizon",
                f"invalid value {hor_val!r}; allowed: {sorted(VALID_TIME_HORIZONS)}"
            ))

        conf_val = row.get("confidence_label")
        if conf_val not in VALID_CONFIDENCE_LABELS:
            errors.append(ValidationError(
                lineno, rid, "confidence_label",
                f"invalid value {conf_val!r}; allowed: {sorted(VALID_CONFIDENCE_LABELS)}"
            ))

        evt_val = row.get("event_type")
        if evt_val not in VALID_EVENT_TYPES:
            errors.append(ValidationError(
                lineno, rid, "event_type",
                f"invalid value {evt_val!r}; allowed: {sorted(VALID_EVENT_TYPES)}"
            ))

        ast_type = row.get("asset_type")
        if ast_type not in VALID_ASSET_TYPES:
            errors.append(ValidationError(
                lineno, rid, "asset_type",
                f"invalid value {ast_type!r}; allowed: {sorted(VALID_ASSET_TYPES)}"
            ))

        nfa = row.get("not_financial_advice")
        if nfa is not True:
            errors.append(ValidationError(
                lineno, rid, "not_financial_advice",
                f"must be boolean true, got {nfa!r}"
            ))

    return errors


def validate_predictions(path: str | Path) -> list[ValidationError]:
    errors: list[ValidationError] = []
    seen_ids: dict[str, int] = {}

    for lineno, row in enumerate(iter_jsonl(path), start=1):
        rid = row.get("id")

        missing = REQUIRED_PREDICTION_FIELDS - set(row.keys())
        for f in sorted(missing):
            errors.append(ValidationError(lineno, rid, f, "required field missing"))

        if missing:
            continue

        if rid in seen_ids:
            errors.append(ValidationError(
                lineno, rid, "id",
                f"duplicate id (first seen at row {seen_ids[rid]})"
            ))
        else:
            seen_ids[rid] = lineno

        dir_val = row.get("predicted_direction")
        if dir_val not in VALID_DIRECTIONS:
            errors.append(ValidationError(
                lineno, rid, "predicted_direction",
                f"invalid value {dir_val!r}; allowed: {sorted(VALID_DIRECTIONS)}"
            ))

        hor_val = row.get("predicted_time_horizon")
        if hor_val not in VALID_TIME_HORIZONS:
            errors.append(ValidationError(
                lineno, rid, "predicted_time_horizon",
                f"invalid value {hor_val!r}; allowed: {sorted(VALID_TIME_HORIZONS)}"
            ))

        evt_val = row.get("predicted_event_type")
        if evt_val not in VALID_EVENT_TYPES:
            errors.append(ValidationError(
                lineno, rid, "predicted_event_type",
                f"invalid value {evt_val!r}; allowed: {sorted(VALID_EVENT_TYPES)}"
            ))

        score = row.get("reasoning_score")
        if score is not None:
            try:
                s = float(score)
                if not (REASONING_SCORE_MIN <= s <= REASONING_SCORE_MAX):
                    errors.append(ValidationError(
                        lineno, rid, "reasoning_score",
                        f"value {s} out of range [{REASONING_SCORE_MIN}, {REASONING_SCORE_MAX}]"
                    ))
            except (TypeError, ValueError):
                errors.append(ValidationError(
                    lineno, rid, "reasoning_score",
                    f"must be a number, got {score!r}"
                ))

    return errors


def _print_stats(rows: list[dict]) -> None:
    from collections import Counter

    def _table(title: str, counter: Counter) -> None:
        print(f"\n  {title}")
        total = sum(counter.values())
        for k, v in sorted(counter.items()):
            bar = "=" * round(v / total * 30)
            print(f"    {k:<22s} {v:3d}  [{bar:<30s}]  {v/total*100:.1f}%")

    print(f"\n  Total rows: {len(rows)}")
    _table("Direction", Counter(r.get("expected_direction", "?") for r in rows))
    _table("Event type", Counter(r.get("event_type", "?") for r in rows))
    _table("Asset type", Counter(r.get("asset_type", "?") for r in rows))
    _table("Time horizon", Counter(r.get("time_horizon", "?") for r in rows))
    print()


def _run(args: argparse.Namespace) -> int:
    path = Path(args.dataset or args.predictions)
    is_dataset = args.dataset is not None

    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 1

    print(f"Validating {'dataset' if is_dataset else 'predictions'}: {path}")

    try:
        rows = list(iter_jsonl(path))
        errors = validate_dataset(path) if is_dataset else validate_predictions(path)
    except ValueError as exc:
        print(f"Parse error: {exc}", file=sys.stderr)
        return 1

    if errors:
        print(f"\n{len(errors)} validation error(s) found:\n")
        for err in errors:
            print(err)
        return 1

    print(f"OK — {len(rows)} rows, no errors.")

    if is_dataset and getattr(args, "stats", False):
        _print_stats(rows)

    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a News2Signal dataset or prediction file."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dataset", metavar="PATH", help="Path to dataset JSONL")
    group.add_argument("--predictions", metavar="PATH", help="Path to predictions JSONL")
    parser.add_argument(
        "--stats", action="store_true",
        help="Print label distribution stats after validation (dataset only)"
    )
    args = parser.parse_args()
    sys.exit(_run(args))


if __name__ == "__main__":
    main()
