# Labeling Guide

This guide explains how to assign labels to news examples in the News2Signal benchmark dataset.

---

## 1. Assigning `expected_direction`

Direction describes the expected price impact of the news on the primary asset.

| Value | When to use |
|-------|-------------|
| `bullish` | News is clearly positive for the asset price and a reasonable analyst would expect buying pressure |
| `bearish` | News is clearly negative for the asset price and a reasonable analyst would expect selling pressure |
| `neutral` | News contains no directional information, is fully priced in, or conflicting forces exactly cancel out |
| `mixed` | News contains genuine bullish and bearish signals with no clear net direction |

**Key principle:** Direction is relative to the primary asset only, not the broader market, unless the asset is a market index.

**Examples:**
- "Fed signals rate cuts" → `bullish` for SPY (equity index)
- "CPI re-accelerates above forecast" → `bearish` for TLT (long-duration bonds)
- "Earnings match consensus exactly" → `neutral` for the stock
- "Strong earnings but guidance cut" → `mixed` (genuine conflict)

---

## 2. Choosing `event_type`

Use the most specific event type that captures the primary market-moving mechanism.

| Type | Typical trigger |
|------|----------------|
| `central_bank` | FOMC decisions, ECB meetings, Fed chair speeches, rate changes |
| `inflation` | CPI, PCE, PPI data releases |
| `earnings` | Quarterly earnings reports, EPS, revenue |
| `guidance` | Forward guidance changes without a full earnings report |
| `regulatory` | FDA approvals, SEC rulings, government enforcement actions |
| `geopolitical` | Wars, trade negotiations, sanctions, conflict escalation |
| `supply_chain` | Lead times, inventory corrections, port disruptions |
| `labor_market` | NFP reports, unemployment rate, wage data, JOLTS |
| `merger_acquisition` | M&A announcements, buyouts, divestitures |
| `product_launch` | New product announcements, major unveilings |
| `credit_risk` | Rating agency actions, default events, reserve builds |
| `commodity` | OPEC decisions, inventory data, weather events affecting commodities |
| `crypto_policy` | ETF approvals, exchange regulations, government digital asset policy |
| `housing` | Housing starts, building permits, home sales data |
| `consumer_demand` | Retail sales, consumer confidence, credit card spending |
| `fiscal_policy` | Government spending packages, tax changes, budget announcements |

**When in doubt:** Choose the event type that best explains *why* the news is directional, not just what category the news organization would file it under.

---

## 3. Choosing `time_horizon`

The time horizon describes the window over which the directional signal is most applicable.

| Value | Approximate range | Typical triggers |
|-------|-------------------|------------------|
| `intraday` | Same trading session | Earnings prints, rate decisions, hard news |
| `short_term` | 1–5 trading days | Data releases, policy signals, credit events |
| `medium_term` | 1–4 weeks | Trade deals (implementation lag), structural supply/demand shifts |
| `long_term` | Multiple months | Structural regulatory changes, multi-year policies |

**Key principle:** Choose the horizon where the *primary* impact materializes, not the duration of the effect. A rate cut might affect equities for months, but the primary repricing happens in the first few days.

---

## 4. Handling neutral cases

**Neutral** is the hardest label to assign correctly. Use it when:

- The outcome was fully priced in by markets before the announcement
- The news contains no directional information whatsoever
- Bullish and bearish components exactly cancel out
- The event is a routine confirmation of existing expectations

**Do not use neutral** as a hedge when you are uncertain. Uncertainty is not neutrality. If the news is directional but you are unsure of the magnitude, use `low` confidence and pick the most likely direction.

---

## 5. Handling mixed cases

**Mixed** means the news contains genuine, material signals in both directions with no clear net outcome.

A strong earnings beat combined with guidance cut is the canonical mixed case. The market must weigh two competing signals, and the net direction is legitimately ambiguous.

**Mixed is not the same as:**
- Low confidence in a direction
- Unclear news
- A direction you personally disagree with

---

## 6. Labeling asset relevance

The `asset` field should name the most directly affected single asset. Guidelines:

- For sector-wide news, use a sector ETF (e.g., `XBI` for biotech, `KRE` for regional banks)
- For macro-wide news, use an index ETF or proxy (e.g., `SPY`, `TLT`, `DXY`)
- For company-specific news, use the company's ticker
- For FX news, use the currency pair (e.g., `EURUSD`)
- For commodity news, use the commodity ticker or ETF (e.g., `USO`, `GLD`)

---

## 7. Difficult cases

### Case: "Strong jobs but wage inflation rises"

Direction: `mixed`. The strong employment is bullish for economic activity. The wage acceleration is inflationary and bearish for rate cut expectations. The net signal for equities depends on which channel dominates, which is genuinely unclear at the time of release.

### Case: "Rate cut but forward guidance removed"

Direction: `mixed`. The cut itself is a stimulus (bullish). The removal of forward guidance signals a shallower easing cycle (bearish relative to priced expectations). The net depends on how many future cuts were priced.

### Case: "Earnings beat but below-the-line guidance cut"

Direction: `mixed`. The current quarter beat is bullish. The forward guidance cut implies the beat was one-time. The stock may move in either direction depending on which frame investors adopt.

### Case: "Company announces index inclusion (previously telegraphed)"

Direction: `neutral`. A telegraphed index addition is priced in by the time of announcement. Passive funds front-run the rebalance. No sustained directional move should be expected.

### Case: "Trade deal announced, excludes most sensitive sectors"

Direction: `mixed` for the affected index. Certain sectors benefit; the excluded sectors do not. The aggregate direction depends on index weighting and which sectors are included vs. excluded.
