# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "yfinance",
#     "pandas",
#     "matplotlib",
#     "mplfinance"
# ]
# ///

import sys
import yfinance as yf
import mplfinance as mpf
import pandas as pd

def draw_kline(ticker_symbol):
    try:
        t = yf.Ticker(ticker_symbol)
        # Fetch 3 months of data to make candles clear
        hist = t.history(period="3mo")
        if hist.empty:
            print(f"No data found for {ticker_symbol}")
            return
            
        # mplfinance requires specific column names: Open, High, Low, Close, Volume
        # yfinance already provides these, but we need to ensure the index is DatetimeIndex
        
        # Define moving averages to plot
        kwargs = dict(type='candle', mav=(10, 20, 60), volume=True, figratio=(12, 8), figscale=1.5)
        
        # Save to file
        filename = f"{ticker_symbol.replace('.TW', '').replace('.TWO', '')}_kline.png"
        mpf.plot(hist, **kwargs, style='yahoo', title=f"{ticker_symbol} Daily K-Line (3 Months)", savefig=filename)
        
        print(f"SUCCESS:{filename}")

    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No ticker provided.")
        sys.exit(1)
    
    ticker = sys.argv[1]
    draw_kline(ticker)
