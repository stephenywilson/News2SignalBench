# Dataset Card — News2Signal Demo Dataset

## Overview

The News2Signal demo dataset (`datasets/demo.jsonl`) is a synthetic labeled benchmark dataset for evaluating AI models on financial news-to-signal reasoning tasks.

---

## Dataset Purpose

This dataset is designed to support:

1. **Model evaluation** — Testing whether a language model can correctly classify the directional market impact, event type, relevant asset, and time horizon for a given piece of financial news
2. **Benchmark development** — Providing a reproducible labeled reference set for comparing model performance
3. **Research** — Studying the difficulty of financial reasoning tasks across different event types and asset classes

---

## Dataset Composition

| Attribute | Value |
|-----------|-------|
| Format | JSONL |
| Version | v0.1.1 |
| Total rows | 40 |
| License | Apache-2.0 |
| Language | English |

### Direction Distribution

| Direction | Count | Percentage |
|-----------|-------|-----------|
| Bullish | 10 | 25% |
| Bearish | 10 | 25% |
| Mixed | 10 | 25% |
| Neutral | 10 | 25% |

The dataset is perfectly balanced across all four direction labels. This ensures no direction class is systematically advantaged and the benchmark tests all signal types equally.

### Event Type Coverage

All 16 allowed event types are represented in the demo dataset:

| Event Type | Count |
|------------|-------|
| central_bank | 5 |
| consumer_demand | 3 |
| commodity | 4 |
| credit_risk | 3 |
| crypto_policy | 2 |
| earnings | 4 |
| fiscal_policy | 1 |
| geopolitical | 3 |
| guidance | 2 |
| housing | 1 |
| inflation | 3 |
| labor_market | 3 |
| merger_acquisition | 1 |
| product_launch | 1 |
| regulatory | 3 |
| supply_chain | 1 |

### Time Horizon Coverage

All four time horizons are represented:

| Time Horizon | Count | % |
|--------------|-------|---|
| intraday | 17 | 42.5% |
| short_term | 14 | 35.0% |
| medium_term | 5 | 12.5% |
| long_term | 4 | 10.0% |

Long-term examples cover all four direction labels (one each: bullish, bearish, neutral, mixed).

### Asset Type Coverage

7 of 8 asset types are represented: equity, equity_index, bond, fx, commodity, crypto, and sector_etf. The `macro_proxy` type is defined in the schema but has no examples in the demo dataset.

---

## Synthetic Nature

**All examples in this dataset are synthetic.** No real news articles were copied or reproduced. Headlines and summaries are representative of real-world market news patterns but are original compositions.

This means:

- No copyright infringement from news publishers
- No real trading signals or actionable market intelligence
- No correlation to any specific historical market event
- Descriptions may be inspired by categories of real news but are not derived from specific articles

---

## Limitations

- **Small size** — 40 rows is sufficient for demonstration and framework testing but is not sufficient for statistically robust model evaluation. Future versions will include larger labeled sets.
- **Single asset per row** — Each row labels one primary asset. Real news often affects multiple assets simultaneously.
- **No temporal structure** — Examples are not ordered or organized by date. The dataset does not support time-series analysis.
- **No market reaction ground truth** — Labels reflect a human labeler's expected directional impact, not observed market prices.
- **Synthetic content** — Real-world financial news contains subtleties, jargon, and domain knowledge that synthetic examples may not fully capture.
- **English only** — No multilingual coverage in v0.1.
- **Confidence labels are human-assigned** — The `confidence_label` field reflects subjective labeler confidence, not statistical certainty.

---

## Intended Use

This dataset is intended for:

- Evaluating language model financial reasoning capabilities
- Benchmarking model performance on structured signal prediction
- Research into financial NLP and market event classification
- Developing and testing evaluation frameworks and metrics

---

## Prohibited Use

This dataset must NOT be used for:

- Making real trading or investment decisions
- Providing financial advice to any person or entity
- Backtesting trading strategies
- Live market signal generation
- Any application where the output could be mistaken for actual financial analysis or advice

---

## Not Financial Advice

Every row in this dataset includes `"not_financial_advice": true`. This field exists as a machine-readable assertion that the dataset is for research only.

The News2Signal benchmark, this dataset, and any predictions generated using this dataset are not financial advice. They are research artifacts.

---

## Citation

If you use this dataset in research, please cite:

```
@software{news2signal_bench,
  title  = {News2Signal Bench},
  author = {Catalayer AI},
  year   = {2024},
  url    = {https://github.com/catalayer/News2SignalBench}
}
```
