---
name: stock_analyst_tool
description: "Fetch real-time stock prices, K-line data, and latest news from Yahoo Finance, cnyes, and Commercial Times. Outputs JSON for analysis. 內建終極雙向鐵血分析架構。"
metadata: { "openclaw": { "emoji": "📈", "requires": { "bins": ["python", "uv"] } } }
---

# Stock Analyst Tool

This skill provides a unified Python script to fetch stock market data (US and TW) and relevant news, outputting the result in a clean JSON format for further AI analysis.

## Features

1. **Market Data**: Fetches recent historical data (K-lines) and current prices using `yfinance`. Supports both US tickers (e.g., `AAPL`, `NVDA`) and Taiwan stock tickers (e.g., `2330.TW`).
2. **News Scraping**: Retrieves recent news headlines related to the ticker from Yahoo Finance (and includes placeholders/basic logic for TW news sites like cnyes/工商時報).
3. **JSON Output**: Formats all collected data into a structured JSON object.

## Usage

Use the `exec` tool to run the bundled Python script. Pass the stock ticker as an argument.

```bash
# Example: Fetch data for Nvidia
uv run --with yfinance --with feedparser python stock_fetcher.py NVDA

# Example: Fetch data for TSMC (Taiwan)
uv run --with yfinance --with feedparser python stock_fetcher.py 2330.TW
```

## 🏆 終極雙向鐵血投資分析架構 (Mandatory Analysis Framework)
每次使用本技能進行個股分析時，**必須強制套用以下五大模組**並產出格式化的報告：

### 🏢 模組一：基本面護欄（EPS 成長力追蹤）
*   **必須列出**：「過去兩年」的實際 EPS。
*   **必須列出**：法人對該公司「2026 年」與「2027 年」的 EPS 預估值。

### 📊 模組二：大盤環境濾網（順勢指標）
*   **加權指數/那斯達克**：大盤必須站穩「月線 (20MA)」之上，或同步出現右側止跌訊號。

### 📈 模組三：買進紀律（必須全數滿足，否則判定【維持觀望】）
1.  **位階夠深**：距離前波波段高點，必須**下跌 20% 以上**。*(必須點出「前波高點的確切日期與價格」)*
2.  **套牢籌碼判讀**：檢視前波高點發生時，是否伴隨**「爆量收黑」**等主力套牢特徵。
3.  **右側與真突破**：股價必須站上短期均線 (10MA/20MA) 且均線翻揚。
4.  **量能確認**：當日成交量必須大於**「近 5 日均量的 1.5 倍」**。

### 📉 模組四：賣出紀律（觸發任一項即判定【強烈賣出警告】）
1.  **鐵血停損**：帳面虧損達到 **-10%**（特別是槓桿型 ETF，無條件砍出）。
2.  **移動停利**：帳面獲利超過 +10% 後，改為動態防守。若「跌破月線 (20MA)」或「從最高點回落 10%」，即停利出場。
3.  **主力真實出貨**：早盤若出現**「爆量拉高，隨後跌破昨日收盤價或今日開盤價」**，確認主力倒貨，立刻逃命。

### 🛡️ 模組五：特殊核心持股（豁免名單）
*   **台積電 (2330)**：長線底倉，**完全豁免**上述的「賣出紀律」（模組四）。

### 🖼️ 模組六：強制附加 K 線圖
*   每次分析**必須自動生成並附上近 3 個月的 K 線圖**（包含成交量與 5/10/20 日均線）。

**輸出要求**：報告必須結構清晰，使用 Emoji 輔助標示達標/未達標，並給出最終的【AI 判決與策略】。
