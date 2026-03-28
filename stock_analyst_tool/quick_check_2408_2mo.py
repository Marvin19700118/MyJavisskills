import yfinance as yf
t = yf.Ticker("2408.TW")
hist = t.history(period='2mo')
if not hist.empty:
    print(f"Close Today: {hist['Close'].iloc[-1]}")
    low_2mo = hist['Low'].min()
    print(f"Low 2mo: {low_2mo}")
    print(f"1.3x Low (2mo): {low_2mo * 1.3}")
else:
    print("No data")
