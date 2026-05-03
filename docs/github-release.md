# GitHub Release Notes

This document contains suggested metadata for the initial GitHub release of News2Signal Bench.

---

## Suggested GitHub Repository Description

```
Open benchmark for evaluating financial news-to-signal reasoning in AI models.
```

---

## Suggested Topics

```
financial-news
ai-benchmark
market-signals
llm-evaluation
news-understanding
finance-ai
python
jsonl
evaluation
benchmark
catalayer
```

---

## Initial Release Title

```
News2Signal Bench v0.1.1 — Financial News-to-Signal Evaluation
```

---

## Initial Release Notes

**News2Signal Bench v0.1.1**

Initial public release of News2Signal Bench by Catalayer AI.

Most AI models can summarize market news. Fewer can turn it into structured signals.

News2Signal Bench evaluates whether a model can classify:
- **Direction** — bullish, bearish, neutral, or mixed
- **Event type** — central bank, earnings, inflation, geopolitical, and more
- **Asset relevance** — which asset is most directly affected
- **Time horizon** — intraday, short-term, medium-term, or long-term

### What's included in v0.1.1

- Synthetic demo dataset (40 balanced labeled examples)
- News-to-signal schema with JSON Schema definition
- Local evaluator with terminal report and JSON output
- Prediction validation CLI
- `simple_baseline.jsonl` — main demo baseline (~65% direction accuracy)
- `oracle_baseline.jsonl` — sanity-check oracle (always scores 100%, not a real model)
- `weak_baseline.jsonl` — failure-mode example
- Scoring metrics: direction accuracy, event type accuracy, asset match, time horizon accuracy, exact row match, reasoning quality
- `--stats` flag for dataset distribution inspection
- Labeling guide
- Evaluation metrics documentation
- Dataset card

### Notes

- Research benchmark only — not financial advice
- No trading execution
- Demo dataset is synthetic
- No private Catalayer data included
- No external dependencies (Python 3.10+ standard library only)

### Quick Start

```bash
git clone https://github.com/catalayer/News2SignalBench
cd News2SignalBench
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m news2signal.validate --dataset datasets/demo.jsonl
python -m news2signal.evaluate \
  --dataset datasets/demo.jsonl \
  --predictions examples/predictions/baseline.jsonl
```

---

## Roadmap Notes (for future releases)

- v0.2: Larger labeled dataset, additional event types
- v0.3: Reasoning quality scoring rubric
- v0.4: Multi-asset labeling support
- v1.0: Public leaderboard integration
