import yfinance as yf
t = yf.Ticker("2344.TW")
hist_3mo = t.history(period='3mo')
if not hist_3mo.empty:
    print(f"High 3mo: {hist_3mo['High'].max()}")
    idx = hist_3mo['High'].idxmax()
    print(f"High Date: {idx}")
    print(f"Close Today: {hist_3mo['Close'].iloc[-1]}")
    print(f"Today Vol: {hist_3mo['Volume'].iloc[-1]}")
    if len(hist_3mo) >= 5:
        print(f"Avg Vol 5D: {hist_3mo['Volume'].iloc[-5:-1].mean()}")
else:
    print("No data")
