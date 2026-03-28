import yfinance as yf
tickers = ["2330.TW", "1773.TW", "2233.TW", "2344.TW", "6239.TW"]
results = {}
for t in tickers:
    ticker = yf.Ticker(t)
    hist = ticker.history(period='1d')
    if not hist.empty:
        results[t] = hist['Close'].iloc[-1]
    else:
        results[t] = 0.0
print(results)
