"""scraper/market_engine.py — Pulls market data and calculates technical indicators."""

import yfinance as yf
import pandas as pd


class MarketEngine:
    """Core financial analytics engine using yfinance API."""

    @staticmethod
    def fetch_ticker_meta(symbol: str) -> dict:
        """Fetch asset name, business summary, and currency."""
        print(f"📊 Querying metadata for ticker: {symbol}...")
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                "name": info.get("longName", symbol),
                "summary": info.get("longBusinessSummary", "No summary available.")[:350] + "...",
                "currency": info.get("currency", "USD"),
                "market_cap": info.get("marketCap", 0),
                "open_price": info.get("open", 0.0),
                "previous_close": info.get("previousClose", 0.0)
            }
        except Exception as e:
            print(f"   ⚠️ Error fetching metadata: {e}")
            return {"name": symbol, "summary": "N/A", "currency": "USD", "market_cap": 0}

    @staticmethod
    def fetch_history(symbol: str, period="6mo", interval="1d") -> pd.DataFrame:
        """Fetch OHLC historical transaction data."""
        print(f"📈 Querying historical data for {symbol} (Period: {period}, Interval: {interval})...")
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            if df.empty:
                return pd.DataFrame()
            df = df.reset_index()
            # Standardize date column header
            df.rename(columns={"Date": "date", "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"}, inplace=True)
            return df
        except Exception as e:
            print(f"   ❌ Error fetching history: {e}")
            return pd.DataFrame()

    @staticmethod
    def calculate_sma(df: pd.DataFrame, window: int) -> pd.Series:
        """Calculate Simple Moving Average (SMA)."""
        return df["close"].rolling(window=window).mean()

    @staticmethod
    def calculate_ema(df: pd.DataFrame, span: int) -> pd.Series:
        """Calculate Exponential Moving Average (EMA)."""
        return df["close"].ewm(span=span, adjust=False).mean()