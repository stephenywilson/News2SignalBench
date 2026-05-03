# Contributing to News2Signal Bench

Thank you for your interest in contributing. This document explains how to set up the project, run checks, and contribute examples or improvements.

## Setup

```bash
git clone https://github.com/catalayer/News2SignalBench
cd News2SignalBench
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Validate the demo dataset

```bash
python -m news2signal.validate --dataset datasets/demo.jsonl
```

## Validate predictions

```bash
python -m news2signal.validate --predictions examples/predictions/baseline.jsonl
python -m news2signal.validate --predictions examples/predictions/weak_baseline.jsonl
```

## Run the evaluator

```bash
python -m news2signal.evaluate \
  --dataset datasets/demo.jsonl \
  --predictions examples/predictions/baseline.jsonl
```

## Run the smoke test

```bash
bash scripts/smoke_test.sh
```

All checks must pass before submitting a pull request.

## Contributing examples

If you want to contribute additional labeled examples:

1. Follow the schema defined in `schema/news_signal.schema.json`
2. Read the labeling guide in `docs/labeling-guide.md`
3. Use only synthetic or clearly paraphrased content — no real article bodies
4. Set `not_financial_advice` to `true` on every row
5. Include a diverse mix of directions, event types, and asset types
6. Run validation before submitting: `python -m news2signal.validate --dataset your-file.jsonl`

## Contributing model predictions

If you want to add predictions from a new model:

1. Place the predictions file in `examples/predictions/`
2. Follow the prediction schema: `id`, `predicted_direction`, `predicted_event_type`, `predicted_asset`, `predicted_time_horizon`, and optionally `reasoning_score` and `reasoning`
3. Run the evaluator and include the report in your pull request description

## Code style

- Python 3.10+
- Type hints on all public functions
- Minimal dependencies — standard library first
- No notebooks, no heavy frameworks

## What to avoid

- Do not include real news article bodies (copyright)
- Do not include real API keys or secrets
- Do not include private datasets
- Do not add dependencies that require a network call or external service
- Do not add trading execution logic
