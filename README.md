# MyJavisskills

A collection of AI-powered skills and tools built for personal productivity, finance, and health management.

## 📦 Skills / 技能清單

| Skill | Description |
|-------|-------------|
| [📈 Stock Analyst Tool](./stock_analyst_tool/) | Fetch real-time stock prices, K-line data, and news. Includes a mandatory dual-direction investment analysis framework. |
| [💼 Portfolio Tracker](./portfolio_tracker/) | Auto-sync portfolio holdings, calculate daily PnL/ROI, and trigger stop-loss / take-profit alerts. |
| [🥗 Health & Diet Tracker](./health-diet-tracker/) | Log meals and exercise, analyze food photos, and provide diet advice with diabetes guidelines. |
| [📊 Auto PPT Generator](./auto-ppt-generator/) | One-click generation of structured, professional PowerPoint presentations. |
| [🤝 Social CRM](./social-crm/) | Manage contacts, business cards, and relationship notes with an AI-powered social database. |

## 🚀 Getting Started

Each skill lives in its own subdirectory and includes a `SKILL.md` with detailed usage instructions. All Python scripts are designed to run with [uv](https://github.com/astral-sh/uv):

```bash
# Example: Fetch stock data for TSMC
uv run --with yfinance --with feedparser stock_analyst_tool/stock_fetcher.py 2330.TW

# Example: Run portfolio tracker
uv run --with yfinance portfolio_tracker/tracker.py
```

## 📋 Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager