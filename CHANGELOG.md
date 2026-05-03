# Changelog

All notable changes to News2Signal Bench are documented here.

## [0.1.1] — 2026-05-03

Benchmark hardening and dataset coverage polish pass before public release.

### Changed

- `datasets/demo.jsonl` — Rebalanced direction labels to exactly 10/10/10/10. Four additional rows replaced to add `long_term` time horizon (one per direction), `supply_chain` event type, and `product_launch` event type. All 16 allowed event types are now represented; all 4 time horizons are now represented.
- `examples/predictions/baseline.jsonl` — Renamed to `oracle_baseline.jsonl` to clarify its purpose as a sanity-check file that should always score 100%, not a real model baseline.
- `scripts/smoke_test.sh` — Updated to test all three prediction files (oracle, simple, weak) and validate with `--stats`.
- `README.md` — Updated Quick Start, Metrics section, and "What's included" to reflect v0.1.1 changes.
- `docs/dataset-card.md` — Updated all distribution tables; added event type, time horizon, and asset type tables.

### Added

- `examples/predictions/simple_baseline.jsonl` — Main demo baseline (~62% direction accuracy, 82.5% event type, 52.5% time horizon, 32.5% exact match). Represents a plausible but imperfect model.
- `news2signal/validate.py` — Added `--stats` flag to print direction, event type, asset type, and time horizon distributions after validation.

### Coverage after v0.1.1

- Direction: 10 bullish / 10 bearish / 10 neutral / 10 mixed
- Event types: all 16 represented
- Time horizons: all 4 represented (intraday 17 / short_term 14 / medium_term 5 / long_term 4)
- Asset types: 7 of 8 represented (macro_proxy has 0 demo examples)

### Notes

- `oracle_baseline.jsonl` is a label-copy sanity check, not a real baseline. It should always score 100%.
- `simple_baseline.jsonl` is the main demo baseline intended for Quick Start examples.
- `weak_baseline.jsonl` is a failure-mode example demonstrating systematic direction misclassification.
- Demo dataset is synthetic. No real news articles or copyrighted content is included.
- Not financial advice. No trading or execution functionality.

---

## [0.1.0] — 2026-05-03

Initial public release.

### Added

- `datasets/demo.jsonl` — 40 synthetic, balanced labeled examples covering 10 bullish, 10 bearish, 10 neutral, and 10 mixed direction labels
- `news2signal/schema.py` — canonical allowed label values for all fields
- `news2signal/io.py` — JSONL read/write utilities
- `news2signal/validate.py` — dataset and prediction validation with clear error messages
- `news2signal/metrics.py` — scoring computation for direction accuracy, event type accuracy, asset match, time horizon accuracy, exact row match, and reasoning quality
- `news2signal/report.py` — terminal report renderer with ASCII progress bars
- `news2signal/evaluate.py` — CLI evaluator entry point with optional JSON output
- `examples/predictions/baseline.jsonl` — label-copy oracle predictions (100% accuracy, sanity check)
- `examples/predictions/weak_baseline.jsonl` — weak baseline predictions demonstrating systematic failure modes
- `examples/prompts/baseline_prompt.md` — prompt template used to generate baseline predictions
- `schema/news_signal.schema.json` — JSON Schema document for dataset row structure
- `docs/labeling-guide.md` — labeling instructions for direction, event type, time horizon, and difficult cases
- `docs/evaluation-metrics.md` — explanation of each metric, limitations, and interpretation guidance
- `docs/dataset-card.md` — dataset card covering composition, intended use, and prohibited use
- `docs/github-release.md` — suggested GitHub release metadata
- `scripts/smoke_test.sh` — end-to-end smoke test script
- `pyproject.toml` — package definition with console scripts
- `LICENSE` — Apache 2.0
- `CONTRIBUTING.md` — contribution guide
- `SECURITY.md` — security policy

### Notes

- Demo dataset is synthetic. No real news articles or copyrighted content is included.
- Not financial advice. No trading or execution functionality.
- No external dependencies beyond Python 3.10+ standard library.
