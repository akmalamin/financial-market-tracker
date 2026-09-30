"""
app.py — Interactive Streamlit Market Tracker and Candlestick Charting App.
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

from config import DEFAULT_STOCKS, DEFAULT_CRYPTOS, PERIODS, INTERVALS
from scraper.market_engine import MarketEngine

st.set_page_config(
    page_title="NovaTrack Financial Portal",
    page_icon="📈",
    layout="wide"
)

st.title("📈 NovaTrack Financial Market Dashboard")
st.caption("Live Institutional-Grade Financial Feed, Candlestick Charting & Moving Average Indicators")

# Sidebar - Asset Selector
st.sidebar.header("🕹️ Market Selector")

asset_type = st.sidebar.radio("Select Asset Class", ["Cryptocurrencies", "Equities / Stocks", "Custom Ticker"])

if asset_type == "Cryptocurrencies":
    selected_name = st.sidebar.selectbox("Choose Crypto Asset", list(DEFAULT_CRYPTOS.keys()))
    ticker_symbol = DEFAULT_CRYPTOS[selected_name]
elif asset_type == "Equities / Stocks":
    selected_name = st.sidebar.selectbox("Choose Stock Ticker", list(DEFAULT_STOCKS.keys()))
    ticker_symbol = DEFAULT_STOCKS[selected_name]
else:
    ticker_symbol = st.sidebar.text_input("Enter Custom Symbol (e.g. GOOG, SOL-USD)", "GOOG").strip().upper()

# Time Controls
period = st.sidebar.selectbox("Date Range (Period)", PERIODS, index=2)
interval = st.sidebar.selectbox("Data Resolution (Interval)", INTERVALS, index=0)

# Technical Indicator toggles
st.sidebar.subheader("📐 Technical Overlays")
show_sma = st.sidebar.checkbox("Simple Moving Average (SMA 20)", value=True)
show_ema = st.sidebar.checkbox("Exponential Moving Average (EMA 20)", value=False)

# Fetch Data
meta = MarketEngine.fetch_ticker_meta(ticker_symbol)
df = MarketEngine.fetch_history(ticker_symbol, period=period, interval=interval)

if not df.empty:
    # Calculate indicators
    df["SMA_20"] = MarketEngine.calculate_sma(df, 20)
    df["EMA_20"] = MarketEngine.calculate_ema(df, 20)

    # 1. Company Profile Block
    st.markdown(f"### {meta['name']} (`{ticker_symbol}`)")
    st.write(meta["summary"])

    # 2. Performance Metric Cards
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2] if len(df) > 1 else last_row

    price_change = last_row["close"] - prev_row["close"]
    pct_change = (price_change / prev_row["close"]) * 100
    color_p = "green" if price_change >= 0 else "red"

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(
        "Current Close Price",
        f"{meta['currency']} {last_row['close']:.2f}",
        f"{price_change:+.2f} ({pct_change:+.2f}%)"
    )
    c2.metric("Previous Session Close", f"{meta['currency']} {prev_row['close']:.2f}")
    c3.metric("Session High Price", f"{meta['currency']} {last_row['high']:.2f}")
    c4.metric("Session Low Price", f"{meta['currency']} {last_row['low']:.2f}")

    st.write("")

    # 3. Interactive Candlestick Chart (Plotly)
    st.subheader("Price Action Chart (OHLC)")

    fig = go.Figure()

    # Candlestick base trace
    fig.add_trace(go.Candlestick(
        x=df["date"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="Price Action",
        increasing_line_color="#10B981",  # Bullish Emerald Green
        decreasing_line_color="#EF4444"  # Bearish Rose Red
    ))

    # Overlay indicator SMA
    if show_sma:
        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["SMA_20"],
            name="SMA 20",
            line=dict(color="#F59E0B", width=2.5)  # Amber
        ))

    # Overlay indicator EMA
    if show_ema:
        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["EMA_20"],
            name="EMA 20",
            line=dict(color="#3B82F6", width=2.5, dash="dash")  # Blue
        ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=10, b=10),
        yaxis=dict(title=f"Price ({meta['currency']})", gridcolor="#334155"),
        xaxis=dict(gridcolor="#334155")
    )

    st.plotly_chart(fig, use_container_width=True)

    # 4. View raw OHLC table
    with st.expander("📋 View Raw OHLC Price Feed"):
        st.dataframe(df.sort_values(by="date", ascending=False), use_container_width=True)
else:
    st.error(
        f"❌ Could not download trading data for symbol `{ticker_symbol}`. Please verify the ticker symbol is valid.")