"""config.py — Global settings for the Market Tracker."""

# Default popular tickers
DEFAULT_STOCKS = {
    "Apple (AAPL)": "AAPL",
    "Tesla (TSLA)": "TSLA",
    "NVIDIA (NVDA)": "NVDA",
    "Microsoft (MSFT)": "MSFT",
    "Amazon (AMZN)": "AMZN"
}

DEFAULT_CRYPTOS = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD",
    "Cardano (ADA)": "ADA-USD"
}

# Supported intervals and date ranges
PERIODS = ["1mo", "3mo", "6mo", "1y", "2y"]
INTERVALS = ["1d", "1wk", "1mo"]