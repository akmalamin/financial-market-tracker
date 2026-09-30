"""
main.py — CLI Runner for Financial Market Tracker.

Usage:
    python main.py --symbol AAPL --period 6mo
"""

import argparse
import os
import pandas as pd
from scraper.market_engine import MarketEngine


def main():
    parser = argparse.ArgumentParser(description="📈 Financial Market Data CLI Tool")
    parser.add_argument("--symbol", default="BTC-USD", help="Asset ticker symbol (e.g. AAPL, BTC-USD)")
    parser.add_argument("--period", default="3mo", help="Data period (1mo, 3mo, 6mo, 1y)")
    args = parser.parse_args()

    print("""
╔══════════════════════════════════════════════════════════╗
║   📈  FINANCIAL MARKET TRACKER — Day 113                 ║
║   Ingest Live Ticker Data & Analyze Price Trends         ║
╚══════════════════════════════════════════════════════════╝
    """)

    meta = MarketEngine.fetch_ticker_meta(args.symbol)
    df = MarketEngine.fetch_history(args.symbol, period=args.period)

    if df.empty:
        print("❌ No historical market data loaded.")
        return

    # Add technical indicators
    df["SMA_20"] = MarketEngine.calculate_sma(df, 20)
    df["EMA_20"] = MarketEngine.calculate_ema(df, 20)

    print(f"\n📊 Asset Profile: {meta['name']}")
    print(f"   Open Price:      {meta['currency']} {meta['open_price']}")
    print(f"   Previous Close:  {meta['currency']} {meta['previous_close']}")
    print(f"\n📈 Last 5 Trading Sessions:")
    print(df[["date", "open", "high", "low", "close", "volume", "SMA_20"]].tail(5).to_string(index=False))

    # Save to CSV
    os.makedirs("output", exist_ok=True)
    out_path = f"output/{args.symbol.lower()}_market_data.csv"
    df.to_csv(out_path, index=False)
    print(f"\n💾 Saved detailed metrics → {out_path}")


if __name__ == "__main__":
    main()