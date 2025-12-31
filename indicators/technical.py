import ta
import pandas as pd
import numpy as np


def add_indicators(df):
    """
    Add comprehensive technical indicators with 5-year pattern recognition.
    
    Indicators:
    - EMAs (20, 50, 100, 200, 252, 630): Multi-timeframe trends
    - RSI: Momentum/overbought-oversold
    - MACD: Trend confirmation
    - Bollinger Bands: Volatility & support/resistance
    - ATR: Volatility-adjusted risk sizing
    - Volume: Trend strength confirmation
    - Support/Resistance: 52-week and all-time levels
    - Seasonality: Monthly patterns for IDX stocks
    """
    close = df["Close"]
    
    # Flatten if multi-dimensional
    if hasattr(close, "ndim") and close.ndim > 1:
        close = close.iloc[:, 0]
    
    # ===== TREND INDICATORS (MULTI-TIMEFRAME) =====
    df["ema20"] = ta.trend.ema_indicator(close, window=20)
    df["ema50"] = ta.trend.ema_indicator(close, window=50)
    df["ema100"] = ta.trend.ema_indicator(close, window=100)
    df["ema200"] = ta.trend.ema_indicator(close, window=200)
    
    # Long-term EMAs for 5-year pattern recognition
    df["ema_252"] = ta.trend.ema_indicator(close, window=252)   # 1 year of trading days
    df["ema_630"] = ta.trend.ema_indicator(close, window=630)   # ~2.5 years
    
    # ===== MOMENTUM INDICATORS =====
    df["rsi"] = ta.momentum.rsi(close, window=14)
    df["rsi_oversold"] = df["rsi"] < 30
    df["rsi_overbought"] = df["rsi"] > 70
    
    # MACD for trend confirmation
    macd_obj = ta.trend.MACD(close, window_fast=12, window_slow=26, window_sign=9)
    df["macd"] = macd_obj.macd()
    df["macd_signal"] = macd_obj.macd_signal()
    df["macd_diff"] = macd_obj.macd_diff()
    df["macd_bullish"] = df["macd"] > df["macd_signal"]
    
    # ===== VOLATILITY INDICATORS =====
    bb = ta.volatility.BollingerBands(close, window=20, window_dev=2)
    df["bb_upper"] = bb.bollinger_hband()
    df["bb_middle"] = bb.bollinger_mavg()
    df["bb_lower"] = bb.bollinger_lband()
    df["bb_percent"] = (close - df["bb_lower"]) / (df["bb_upper"] - df["bb_lower"])
    
    # ATR for volatility-adjusted risk sizing
    df["atr"] = ta.volatility.average_true_range(
        df["High"], df["Low"], close, window=14
    )
    df["volatility"] = close.rolling(window=20).std()
    
    # ===== VOLUME ANALYSIS =====
    if "Volume" in df.columns:
        df["volume_sma"] = df["Volume"].rolling(window=20).mean()
        df["volume_ratio"] = df["Volume"] / df["volume_sma"]
    
    # ===== SUPPORT & RESISTANCE (5-YEAR ZONES) =====
    # 52-week high/low
    df["high_52w"] = close.rolling(window=252).max()
    df["low_52w"] = close.rolling(window=252).min()
    
    # All-time high/low in dataset (5 years)
    df["all_time_high"] = close.expanding().max()
    df["all_time_low"] = close.expanding().min()
    
    # Distance to support/resistance (%)
    df["distance_to_high_pct"] = ((df["high_52w"] - close) / close * 100).round(2)
    df["distance_to_low_pct"] = ((close - df["low_52w"]) / close * 100).round(2)
    
    # ===== TREND STRENGTH =====
    df["trend_ema_alignment"] = (
        (close > df["ema20"]).astype(int) +
        (df["ema20"] > df["ema50"]).astype(int) +
        (df["ema50"] > df["ema200"]).astype(int)
    )  # 0-3 score
    
    df["long_term_trend"] = (
        (close > df["ema_252"]).astype(int) +
        (df["ema_252"] > df["ema_630"]).astype(int)
    )  # 0-2 score for 1Y+ trend
    
    # ===== SEASONALITY (MONTHLY PATTERN) =====
    if not isinstance(df.index, pd.DatetimeIndex):
        try:
            df.index = pd.to_datetime(df.index)
        except:
            pass
    
    df["month"] = df.index.month if isinstance(df.index, pd.DatetimeIndex) else 1
    df["daily_return_pct"] = close.pct_change() * 100
    
    return df

