import json
import yfinance as yf
import pandas as pd
import sys
import warnings

warnings.filterwarnings('ignore')
sys.stdout.reconfigure(encoding='utf-8')

with open('My_Portfolio.json', 'r', encoding='utf-8') as f:
    port = json.load(f)

def get_index_status(ticker):
    try:
        hist = yf.Ticker(ticker).history(period="3mo")
        if len(hist) < 20: return True
        close = hist['Close'].iloc[-1]
        ma20 = hist['Close'].rolling(20).mean().iloc[-1]
        return close > ma20
    except:
        return True

tw_bull = get_index_status('^TWII')
us_bull = get_index_status('^IXIC')

def analyze(ticker, cost, is_held, is_exempt, market_bull):
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="1y")
        if len(hist) < 20: return "資料不足"
        
        close = hist['Close'].iloc[-1]
        high_52w = hist['High'].max()
        drop_pct = (high_52w - close) / high_52w * 100
        
        ma10 = hist['Close'].rolling(10).mean().iloc[-1]
        ma20 = hist['Close'].rolling(20).mean().iloc[-1]
        
        vol = hist['Volume'].iloc[-1]
        vol5 = hist['Volume'].rolling(5).mean().iloc[-1]
        
        res = []
        
        if is_held:
            if is_exempt:
                res.append("🛡️ 豁免名單：長抱策略 (尋找加碼點)")
            else:
                if cost:
                    roi = (close - cost) / cost * 100
                    res.append(f"現價:{close:.2f} | 成本:{cost:.2f} | 報酬率:{roi:.2f}%")
                    if roi <= -10:
                        res.append("🔴 觸發【鐵血停損】(虧損達-10%)，建議無情砍出")
                    elif roi > 10:
                        if close < ma20:
                            res.append("🟢 觸發【移動停利】(獲利>10%且跌破月線)，建議獲利入袋")
                        elif close < high_52w * 0.9:
                            res.append("🟢 觸發【移動停利】(獲利>10%且自高點回檔10%)，建議獲利入袋")
                        else:
                            res.append("✅ 獲利續抱 (未跌破移動停利防守線)")
                    else:
                        res.append("✅ 區間震盪續抱 (未觸發10%停損/停利點)")
        else:
            # check buy rules
            pass_drop = drop_pct >= 20
            # right side: above MA10/MA20 and volume >= 1.5 * vol5
            pass_right = (close > ma10) and (close > ma20) and (vol >= 1.5 * vol5)
            
            if pass_drop and pass_right and market_bull:
                res.append(f"🚀 【買進訊號】(跌幅 {drop_pct:.1f}% >= 20%, 帶量突破)")
            else:
                fail_reasons = []
                if not pass_drop: fail_reasons.append(f"跌幅僅 {drop_pct:.1f}%(未達20%)")
                if not pass_right: fail_reasons.append("未帶量站上短均線")
                if not market_bull: fail_reasons.append("大盤破月線")
                res.append("👀 【維持觀望】: " + ", ".join(fail_reasons))
                
        return " | ".join(res)
    except Exception as e:
        return f"處理錯誤"

print("### 📊 大盤環境濾網")
print(f"- 🇹🇼 台股大盤 (^TWII) 月線之上: {'✅ 是 (可順勢買進)' if tw_bull else '❌ 否 (逆勢環境)'}")
print(f"- 🇺🇸 美股納指 (^IXIC) 月線之上: {'✅ 是 (可順勢買進)' if us_bull else '❌ 否 (逆勢環境)'}\n")

for region, holdings in port.get('holdings', {}).items():
    print(f"### {region} 股市部位分析")
    for h in holdings:
        name = h.get('name')
        tkr = h.get('ticker')
        cost = h.get('cost_price')
        
        yf_tkr = tkr
        market_bull = tw_bull if region == 'TW' else us_bull
        
        if region == 'TW' and not tkr.endswith('.TW') and not tkr.endswith('.TWO'):
            yf_tkr = tkr + '.TW'
            
        is_held = (cost is not None)
        is_exempt = (tkr == '2330')
        
        status = analyze(yf_tkr, cost, is_held, is_exempt, market_bull)
        if "處理錯誤" in status and region == 'TW':
            yf_tkr = tkr + '.TWO'
            status = analyze(yf_tkr, cost, is_held, is_exempt, market_bull)
            
        print(f"- **{name} ({tkr})**: {status}")
