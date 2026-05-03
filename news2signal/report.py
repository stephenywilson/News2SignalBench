"""Terminal report renderer for evaluation results."""

from __future__ import annotations

from .metrics import EvalResult


_BAR_WIDTH = 40


def _bar(ratio: float) -> str:
    filled = round(ratio * _BAR_WIDTH)
    return "[" + "=" * filled + " " * (_BAR_WIDTH - filled) + "]"


def _pct(ratio: float) -> str:
    return f"{ratio * 100:.1f}%"


def render_terminal(result: EvalResult, predictions_path: str = "") -> str:
    lines: list[str] = []

    lines.append("")
    lines.append("=" * 60)
    lines.append("  News2Signal Bench — Evaluation Report")
    lines.append("=" * 60)

    if predictions_path:
        lines.append(f"  Predictions : {predictions_path}")

    lines.append("")
    lines.append(f"  Dataset rows      : {result.total_dataset}")
    lines.append(f"  Prediction rows   : {result.total_predictions}")
    lines.append(f"  Matched rows      : {result.matched}")
    lines.append("")

    cov = result.coverage()
    lines.append(f"  Coverage          : {_pct(cov)}  {_bar(cov)}")

    da = result.direction_accuracy()
    lines.append(f"  Direction Acc.    : {_pct(da)}  {_bar(da)}")

    ea = result.event_type_accuracy()
    lines.append(f"  Event Type Acc.   : {_pct(ea)}  {_bar(ea)}")

    aa = result.asset_accuracy()
    lines.append(f"  Asset Match Acc.  : {_pct(aa)}  {_bar(aa)}")

    ha = result.time_horizon_accuracy()
    lines.append(f"  Time Horizon Acc. : {_pct(ha)}  {_bar(ha)}")

    xm = result.exact_match_rate()
    lines.append(f"  Exact Row Match   : {_pct(xm)}  {_bar(xm)}")

    avg_rs = result.avg_reasoning_score()
    if avg_rs is not None:
        lines.append(f"  Avg Reasoning     : {avg_rs:.2f} / 5.00")
    else:
        lines.append("  Avg Reasoning     : N/A (no scores provided)")

    lines.append("")

    if result.missing_ids:
        lines.append(f"  Missing predictions ({len(result.missing_ids)}):")
        for mid in result.missing_ids[:10]:
            lines.append(f"    - {mid}")
        if len(result.missing_ids) > 10:
            lines.append(f"    ... and {len(result.missing_ids) - 10} more")
        lines.append("")

    if result.invalid_ids:
        lines.append(f"  Invalid prediction IDs ({len(result.invalid_ids)}) — not in dataset:")
        for iid in result.invalid_ids[:5]:
            lines.append(f"    - {iid}")
        lines.append("")

    if result.direction_mismatches:
        lines.append(f"  Direction mismatches (top {min(5, len(result.direction_mismatches))}):")
        for mm in result.direction_mismatches[:5]:
            lines.append(
                f"    {mm['id']}: expected={mm['expected']}  predicted={mm['predicted']}"
            )
        lines.append("")

    if result.event_type_mismatches:
        lines.append(f"  Event type mismatches (top {min(5, len(result.event_type_mismatches))}):")
        for mm in result.event_type_mismatches[:5]:
            lines.append(
                f"    {mm['id']}: expected={mm['expected']}  predicted={mm['predicted']}"
            )
        lines.append("")

    lines.append("=" * 60)
    lines.append("  NOTE: This is a research benchmark. Not financial advice.")
    lines.append("=" * 60)
    lines.append("")

    return "\n".join(lines)
