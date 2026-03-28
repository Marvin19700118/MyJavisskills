import yfinance as yf
t = yf.Ticker("2408.TW")
hist = t.history(period='3mo')
print(f"Close Today: {hist['Close'].iloc[-1]}")
print(f"Low 3mo: {hist['Low'].min()}")
print(f"1.3x Low: {hist['Low'].min() * 1.3}")
print(f"High 3mo: {hist['High'].max()}")
