import sys
import json
import yfinance as yf
import pandas as pd

# Fix print encoding on Windows
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

def calculate_rsi(data, periods=14):
    delta = data.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=periods - 1, adjust=False).mean()
    ema_down = down.ewm(com=periods - 1, adjust=False).mean()
    rs = ema_up / ema_down
    rsi = 100 - (100 / (1 + rs))
    return rsi

def analyze_technical(ticker_symbol):
    try:
        t = yf.Ticker(ticker_symbol)
        # Fetch 6 months of data for meaningful MA and RSI calculations
        hist = t.history(period="6mo")
        if hist.empty:
            return json.dumps({"error": f"No data found for {ticker_symbol}"})

        # Calculate Moving Averages
        hist['MA10'] = hist['Close'].rolling(window=10).mean()
        hist['MA20'] = hist['Close'].rolling(window=20).mean()
        hist['MA60'] = hist['Close'].rolling(window=60).mean()

        # Calculate RSI
        hist['RSI'] = calculate_rsi(hist['Close'])

        last_row = hist.iloc[-1]
        
        # Determine basic Support and Resistance (Simplified: Min/Max of last 20 days)
        recent_20 = hist.tail(20)
        support = recent_20['Low'].min()
        resistance = recent_20['High'].max()

        result = {
            "ticker": ticker_symbol,
            "current_price": round(last_row['Close'], 2),
            "technical_indicators": {
                "MA10": round(last_row['MA10'], 2) if not pd.isna(last_row['MA10']) else None,
                "MA20": round(last_row['MA20'], 2) if not pd.isna(last_row['MA20']) else None,
                "MA60": round(last_row['MA60'], 2) if not pd.isna(last_row['MA60']) else None,
                "RSI_14": round(last_row['RSI'], 2) if not pd.isna(last_row['RSI']) else None,
                "Support_20d": round(support, 2),
                "Resistance_20d": round(resistance, 2)
            }
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No ticker provided."}))
        sys.exit(1)
    
    ticker = sys.argv[1]
    print(analyze_technical(ticker))
