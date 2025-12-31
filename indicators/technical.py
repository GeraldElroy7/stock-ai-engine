import ta
import pandas as pd
import numpy as np


def add_indicators(df):
    """
    Add comprehensive technical indicators to dataframe.
    These indicators provide transparent decision signals for institutional use.
    
    Indicators added:
    - EMAs (20, 50, 200): Trend identification
    - RSI: Momentum/overbought-oversold
    - MACD: Trend confirmation
    - Bollinger Bands: Volatility & breakout levels
    - ATR: Volatility-adjusted risk sizing
    - Volume: Trend strength confirmation
    """
    close = df["Close"]
    
    # Flatten if multi-dimensional
    if hasattr(close, "ndim") and close.ndim > 1:
        close = close.iloc[:, 0]
    
    # ===== TREND INDICATORS =====
    df["ema20"] = ta.trend.ema_indicator(close, window=20)
    df["ema50"] = ta.trend.ema_indicator(close, window=50)
    df["ema200"] = ta.trend.ema_indicator(close, window=200)
    
    # ===== MOMENTUM INDICATORS =====
    df["rsi"] = ta.momentum.rsi(close, window=14)
    
    # MACD for trend confirmation
    macd_obj = ta.trend.MACD(close, window_fast=12, window_slow=26, window_sign=9)
    df["macd"] = macd_obj.macd()
    df["macd_signal"] = macd_obj.macd_signal()
    df["macd_diff"] = macd_obj.macd_diff()
    
    # ===== VOLATILITY INDICATORS =====
    bb = ta.volatility.BollingerBands(close, window=20, window_dev=2)
    df["bb_upper"] = bb.bollinger_hband()
    df["bb_middle"] = bb.bollinger_mavg()
    df["bb_lower"] = bb.bollinger_lband()
    
    # ATR for volatility-adjusted risk sizing
    df["atr"] = ta.volatility.average_true_range(
        df["High"], df["Low"], close, window=14
    )
    
    # ===== VOLUME ANALYSIS =====
    if "Volume" in df.columns:
        df["volume_sma"] = df["Volume"].rolling(window=20).mean()
        df["volume_ratio"] = df["Volume"] / df["volume_sma"]
    
    return df

