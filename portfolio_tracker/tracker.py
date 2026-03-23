import json
import os
import sys
import yfinance as yf

# Fix print encoding on Windows
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

def get_latest_price(ticker):
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="1d")
        if not hist.empty:
            return round(hist['Close'].iloc[-1], 2)
    except Exception:
        pass
    return None

def main():
    # Use argument for filename if provided, else default to My_Portfolio.json
    portfolio_file = sys.argv[1] if len(sys.argv) > 1 else 'My_Portfolio.json'
    
    if not os.path.exists(portfolio_file):
        print(f"找不到 {portfolio_file} 檔案。")
        return

    with open(portfolio_file, 'r', encoding='utf-8') as f:
        port = json.load(f)

    portfolio_name = port.get('portfolio_name', portfolio_file)
    report = [f"# 📊 {portfolio_name} - 每日持倉損益自動結算報告\n"]
    alerts = []

    holdings_data = port.get('holdings', {})
    
    for region, holdings in holdings_data.items():
        report.append(f"## {region} 股市部位")
        for h in holdings:
            name = h.get('name', '')
            ticker = h.get('ticker', '')
            cost = h.get('cost_price')
            total_shares = h.get('total_shares', 0)
            
            yf_ticker = ticker
            price = None
            if region == 'TW' and not ticker.endswith('.TW') and not ticker.endswith('.TWO'):
                price = get_latest_price(f"{ticker}.TW")
                if price is None:
                    yf_ticker = f"{ticker}.TWO"
                    price = get_latest_price(yf_ticker)
                else:
                    yf_ticker = f"{ticker}.TW"
            else:
                price = get_latest_price(yf_ticker)
            
            if price is not None:
                if cost is not None:
                    roi = ((price - cost) / cost) * 100
                    pnl = (price - cost) * total_shares
                    
                    status_alert = ""
                    if roi <= -10:
                        status_alert = "🔴 【風險預警：已達停損位】"
                        alerts.append(f"{status_alert} {name}({ticker}) 報酬率: {roi:.2f}% | 虧損: {pnl:,.0f}")
                    elif roi >= 20:
                        status_alert = "🟢 【獲利提醒：建議分批入袋】"
                        alerts.append(f"{status_alert} {name}({ticker}) 報酬率: {roi:.2f}% | 獲利: {pnl:,.0f}")
                    
                    line = f"- **{name} ({ticker})**: 現價 {price:.2f} | 成本 {cost:.2f} | 報酬率 **{roi:.2f}%** | 損益 **{pnl:,.0f}**"
                    if status_alert:
                        line = f"{status_alert}\n  {line}"
                    report.append(line)
                else:
                    report.append(f"- **{name} ({ticker})**: 現價 {price:.2f} | 成本 未設定 (👀 觀察中)")
            else:
                report.append(f"- **{name} ({ticker})**: ⚠️ 無法取得最新報價")
        report.append("\n")

    if alerts:
        report.insert(1, "### ⚠️ 系統觸發警示 (Auto-Sync Alerts)")
        for a in alerts:
            report.insert(2, f"- {a}")
        report.insert(len(alerts) + 2, "\n---\n")

    print("\n".join(report))

if __name__ == "__main__":
    main()