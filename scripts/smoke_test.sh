#!/usr/bin/env bash
# End-to-end smoke test for News2Signal Bench.
# Run from the repository root: bash scripts/smoke_test.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

DATASET="datasets/demo.jsonl"
ORACLE="examples/predictions/oracle_baseline.jsonl"
SIMPLE="examples/predictions/simple_baseline.jsonl"
WEAK="examples/predictions/weak_baseline.jsonl"
REPORT="reports/smoke-report.json"

echo "========================================"
echo "  News2Signal Bench — Smoke Test"
echo "========================================"
echo ""

echo ">>> Validating dataset (with stats): $DATASET"
python -m news2signal.validate --dataset "$DATASET" --stats
echo ""

echo ">>> Validating oracle_baseline predictions: $ORACLE"
python -m news2signal.validate --predictions "$ORACLE"
echo ""

echo ">>> Validating simple_baseline predictions: $SIMPLE"
python -m news2signal.validate --predictions "$SIMPLE"
echo ""

echo ">>> Validating weak_baseline predictions: $WEAK"
python -m news2signal.validate --predictions "$WEAK"
echo ""

echo ">>> Evaluating oracle_baseline (sanity check — should score 100%)"
python -m news2signal.evaluate --dataset "$DATASET" --predictions "$ORACLE"
echo ""

echo ">>> Evaluating simple_baseline (main demo baseline)"
python -m news2signal.evaluate --dataset "$DATASET" --predictions "$SIMPLE"
echo ""

echo ">>> Evaluating weak_baseline (failure-mode example)"
python -m news2signal.evaluate --dataset "$DATASET" --predictions "$WEAK"
echo ""

echo ">>> Writing smoke report to: $REPORT"
python -m news2signal.evaluate \
  --dataset "$DATASET" \
  --predictions "$SIMPLE" \
  --output "$REPORT"

if [[ ! -f "$REPORT" ]]; then
  echo "ERROR: Report file was not created at $REPORT" >&2
  exit 1
fi

echo ""
echo ">>> Confirming report file exists: $REPORT"
ls -lh "$REPORT"

echo ""
echo "========================================"
echo "  All smoke tests passed."
echo "========================================"
