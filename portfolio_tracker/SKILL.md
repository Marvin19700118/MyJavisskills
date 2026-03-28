---
name: portfolio_tracker
description: "Auto-sync portfolio, calculate daily PnL, and generate alerts for stop-loss (-10%) and take-profit (+20%)."
metadata: { "openclaw": { "emoji": "💼", "requires": { "bins": ["python", "uv"] } } }
---

# Portfolio Tracker

This skill provides an automated script to read `My_Portfolio.json`, fetch the latest closing prices, and calculate exact PnL and ROI for each holding.

## Features

1. **Auto-Sync**: Fetches the latest prices via `yfinance`. Automatically appends `.TW` for Taiwan stocks.
2. **PnL Calculation**: 
   - TW: `(Current Price - Cost) * Total Shares`
   - US: `(Current Price - Cost) * Total Shares`
3. **Alert System**: Triggers explicit visual alerts if a stock's ROI drops below -10% or exceeds +20%.

## Usage

Run the script to output the current portfolio status and alerts.

```bash
uv run --with yfinance python skills/portfolio_tracker/tracker.py
```
