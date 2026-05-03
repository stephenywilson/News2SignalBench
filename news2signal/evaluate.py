"""Main evaluator entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .io import load_jsonl, write_json
from .metrics import compute_metrics
from .report import render_terminal


def _run(args: argparse.Namespace) -> int:
    dataset_path = Path(args.dataset)
    predictions_path = Path(args.predictions)

    for p in (dataset_path, predictions_path):
        if not p.exists():
            print(f"Error: file not found: {p}", file=sys.stderr)
            return 1

    print(f"Loading dataset      : {dataset_path}")
    print(f"Loading predictions  : {predictions_path}")

    try:
        dataset = load_jsonl(dataset_path)
        predictions = load_jsonl(predictions_path)
    except ValueError as exc:
        print(f"Parse error: {exc}", file=sys.stderr)
        return 1

    result = compute_metrics(dataset, predictions)

    report_text = render_terminal(result, predictions_path=str(predictions_path))
    print(report_text)

    if args.output:
        output_path = Path(args.output)
        payload = result.to_dict()
        payload["dataset_path"] = str(dataset_path)
        payload["predictions_path"] = str(predictions_path)
        write_json(payload, output_path)
        print(f"Report written to: {output_path}")

    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate News2Signal predictions against a labeled dataset."
    )
    parser.add_argument("--dataset", required=True, metavar="PATH",
                        help="Path to labeled dataset JSONL")
    parser.add_argument("--predictions", required=True, metavar="PATH",
                        help="Path to model predictions JSONL")
    parser.add_argument("--output", metavar="PATH",
                        help="Optional: write JSON report to this path")
    args = parser.parse_args()
    sys.exit(_run(args))


if __name__ == "__main__":
    main()
