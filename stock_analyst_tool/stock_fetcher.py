import sys
import json
import feedparser
import yfinance as yf
from datetime import datetime, timedelta

def get_stock_data(ticker_symbol):
    try:
        t = yf.Ticker(ticker_symbol)
        hist = t.history(period="5d")
        
        k_line_data = []
        for date, row in hist.iterrows():
            k_line_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "open": round(row['Open'], 2),
                "high": round(row['High'], 2),
                "low": round(row['Low'], 2),
                "close": round(row['Close'], 2),
                "volume": int(row['Volume'])
            })
            
        current_price = k_line_data[-1]["close"] if k_line_data else None
        
        # Yahoo Finance News (for US mostly, but works for TW too)
        news_items = []
        for news in t.news[:5]:
            news_items.append({
                "title": news.get("title", ""),
                "link": news.get("link", ""),
                "published": datetime.fromtimestamp(news.get("providerPublishTime", 0)).strftime("%Y-%m-%d %H:%M:%S") if news.get("providerPublishTime") else "",
                "source": news.get("publisher", "Yahoo Finance")
            })

        # Basic TW News RSS parsing (cnyes/工商時報) - just generic news for demonstration
        if ".TW" in ticker_symbol or ".TWO" in ticker_symbol:
            # Example: Fetching general market news for TW stocks
            # Note: For specific scraping, BeautifulSoup & requests would be used, but RSS is safer here.
            tw_rss_url = "https://news.cnyes.com/api/v3/news/category/tw_stock?limit=3"
            try:
                import requests
                resp = requests.get(tw_rss_url, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    for item in data.get('items', {}).get('data', [])[:3]:
                        news_items.append({
                            "title": item.get('title', ''),
                            "link": f"https://news.cnyes.com/news/id/{item.get('newsId', '')}",
                            "published": datetime.fromtimestamp(item.get('publishAt', 0)).strftime("%Y-%m-%d %H:%M:%S"),
                            "source": "鉅亨網 (cnyes)"
                        })
            except Exception as e:
                pass
        
        result = {
            "ticker": ticker_symbol,
            "current_price": current_price,
            "k_line_5d": k_line_data,
            "recent_news": news_items
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No ticker provided. Usage: python stock_fetcher.py <ticker>"}))
        sys.exit(1)
        
    ticker = sys.argv[1]
    print(get_stock_data(ticker))
