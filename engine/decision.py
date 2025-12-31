import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Try to import config from parent directory
try:
    # When running as module (-m stock_ai_engine.scripts.run_backtest)
    from config import SIGNAL_CONFIG
except (ImportError, ModuleNotFoundError):
    # Fallback: add parent to path and try again
    parent_dir = str(Path(__file__).parent.parent)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    try:
        from config import SIGNAL_CONFIG
    except (ImportError, ModuleNotFoundError):
        # Use hardcoded defaults
        SIGNAL_CONFIG = {
            "BUY_THRESHOLD": 4.0,
            "SELL_THRESHOLD": -0.5,
        }


def _as_scalar(val):
    """Safely reduce a pandas scalar/1-element Series/ndarray to a Python float if possible."""
    if isinstance(val, pd.Series):
        val = val.iloc[-1]
    if isinstance(val, (np.ndarray, list, tuple)):
        try:
            return float(val[-1])
        except Exception:
            return None
    try:
        return float(val)
    except Exception:
        return None


def decision_engine(df):
    """
    INSTITUTIONAL-GRADE DECISION ENGINE (with SHORT signal support)
    
    Generates transparent, indicator-based buy/sell/hold/short signals.
    All decisions are traceable to specific technical indicators.
    
    Scoring system (-10 to +10 range):
    - Trend confirmation (EMA alignment): ±3 points
    - Momentum confirmation (RSI + MACD): ±3 points  
    - Volatility context (Bollinger Bands): ±2 points
    - Volume confirmation: ±2 points
    
    Signal thresholds (configurable):
    - SHORT signal: score <= -7.0 (extreme downtrend, profit from decline)
    - SELL signal: score <= -0.5 (downtrend confirmation, close position)
    - HOLD: score between -0.5 and 4.0 (no clear direction)
    - BUY signal: score >= 4.0 (uptrend, high conviction)
    
    Args:
        df: DataFrame with OHLCV data and all technical indicators
    
    Returns:
        dict with signal, score, confidence, reasons, and detailed metadata
    """
    latest = df.iloc[-1]
    
    close = _as_scalar(latest.get("Close"))
    ema20 = _as_scalar(latest.get("ema20"))
    ema50 = _as_scalar(latest.get("ema50"))
    ema200 = _as_scalar(latest.get("ema200"))
    rsi = _as_scalar(latest.get("rsi"))
    macd = _as_scalar(latest.get("macd"))
    macd_signal = _as_scalar(latest.get("macd_signal"))
    macd_diff = _as_scalar(latest.get("macd_diff"))
    bb_upper = _as_scalar(latest.get("bb_upper"))
    bb_lower = _as_scalar(latest.get("bb_lower"))
    atr = _as_scalar(latest.get("atr"))
    vol_ratio = _as_scalar(latest.get("volume_ratio"))
    
    score = 0.0
    reasons = []
    meta = {
        "close": close,
        "ema20": ema20,
        "ema50": ema50,
        "ema200": ema200,
        "rsi": rsi,
        "macd": macd,
        "macd_signal": macd_signal,
        "atr": atr,
        "vol_ratio": vol_ratio
    }
    
    # ===== 1. TREND CONFIRMATION (Up to 3 points) =====
    if (close is not None) and (ema20 is not None) and (ema50 is not None) and (ema200 is not None):
        if close > ema20 > ema50 > ema200:
            score += 3.0
            reasons.append("STRONG_UPTREND: Price > EMA20 > EMA50 > EMA200")
            meta["trend_strength"] = "strong_up"
        elif close > ema20 > ema50:
            score += 2.0
            reasons.append("UPTREND: Price > EMA20 > EMA50")
            meta["trend_strength"] = "moderate_up"
        elif close > ema50:
            score += 1.0
            reasons.append("WEAK_UPTREND: Price > EMA50")
            meta["trend_strength"] = "weak_up"
        elif close < ema20 < ema50 < ema200:
            score -= 3.0
            reasons.append("STRONG_DOWNTREND: Price < EMA20 < EMA50 < EMA200")
            meta["trend_strength"] = "strong_down"
        elif close < ema20 < ema50:
            score -= 2.0
            reasons.append("DOWNTREND: Price < EMA20 < EMA50")
            meta["trend_strength"] = "moderate_down"
        elif close < ema50:
            score -= 1.0
            reasons.append("WEAK_DOWNTREND: Price < EMA50")
            meta["trend_strength"] = "weak_down"
        else:
            meta["trend_strength"] = "mixed"
    
    # ===== 2. MOMENTUM CONFIRMATION (Up to 3 points) =====
    
    # RSI signals
    if rsi is not None:
        if 30 < rsi < 70:
            score += 1.0
            reasons.append("RSI_NEUTRAL: 30-70 range (no overbought/oversold)")
        elif rsi >= 70:
            score -= 1.0
            reasons.append("RSI_OVERBOUGHT: >= 70 (potential reversal)")
            meta["rsi_state"] = "overbought"
        elif rsi <= 30:
            score += 1.0  # oversold can be good entry
            reasons.append("RSI_OVERSOLD: <= 30 (potential bounce)")
            meta["rsi_state"] = "oversold"
    
    # MACD confirmation
    if (macd is not None) and (macd_signal is not None):
        macd_diff_calc = macd - macd_signal if macd_signal != 0 else 0
        if macd > macd_signal and macd_diff_calc > 0:
            score += 2.0
            reasons.append("MACD_BULLISH: MACD above signal line (uptrend)")
            meta["macd_state"] = "bullish"
        elif macd < macd_signal and macd_diff_calc < 0:
            score -= 2.0
            reasons.append("MACD_BEARISH: MACD below signal line (downtrend)")
            meta["macd_state"] = "bearish"
        else:
            reasons.append("MACD_NEUTRAL: Transitioning")
            meta["macd_state"] = "neutral"
    
    # ===== 3. VOLATILITY CONTEXT (Up to 2 points) =====
    if (bb_upper is not None) and (bb_lower is not None) and (close is not None):
        if close > bb_upper:
            score += 0.5
            reasons.append("BREAKOUT_UP: Price above upper Bollinger Band")
            meta["bb_state"] = "above_upper"
        elif close < bb_lower:
            score += 0.5
            reasons.append("OVERSOLD_BB: Price below lower Bollinger Band")
            meta["bb_state"] = "below_lower"
        else:
            meta["bb_state"] = "in_range"
    
    # ===== 4. VOLUME CONFIRMATION (Up to 2 points) =====
    if vol_ratio is not None:
        if vol_ratio > 1.5:
            score += 1.5
            reasons.append(f"HIGH_VOLUME: {vol_ratio:.2f}x avg (strong conviction)")
            meta["volume_state"] = "high"
        elif vol_ratio > 1.2:
            score += 0.5
            reasons.append(f"ABOVE_AVG_VOLUME: {vol_ratio:.2f}x avg")
            meta["volume_state"] = "above_avg"
        elif vol_ratio < 0.7:
            score -= 0.5
            reasons.append(f"LOW_VOLUME: {vol_ratio:.2f}x avg (weak signal)")
            meta["volume_state"] = "low"
        else:
            meta["volume_state"] = "normal"
    
    # ===== RISK SIZING INFO =====
    if atr is not None:
        meta["atr"] = atr
        meta["stop_loss_distance"] = atr  # Can be used to calculate stop loss
        if close is not None and atr > 0:
            meta["stop_loss_pct"] = round((atr / close) * 100, 2)
    
    # Clamp score to -10 to 10 range
    score = max(-10, min(score, 10))
    confidence = round((score + 10) / 20, 2)  # Normalize to 0-1
    
    # ===== SIGNAL GENERATION =====
    # Use thresholds from config (optimized via historical analysis)
    buy_threshold = SIGNAL_CONFIG.get("BUY_THRESHOLD", 4.0)
    sell_threshold = SIGNAL_CONFIG.get("SELL_THRESHOLD", -0.5)
    short_threshold = SIGNAL_CONFIG.get("SHORT_THRESHOLD", -7.0)
    
    if score >= buy_threshold:
        signal = "BUY"
        meta["signal_type"] = "uptrend_entry"
        meta["position_direction"] = "long"
    elif score <= short_threshold:
        signal = "SHORT"
        meta["signal_type"] = "downtrend_entry"
        meta["position_direction"] = "short"
        reasons.append(f"SHORT_SIGNAL: Extreme downtrend (score {score:.1f}), profit from decline")
    elif score <= sell_threshold:
        signal = "SELL"
        meta["signal_type"] = "exit_or_avoid"
        meta["position_direction"] = "neutral"
    else:
        signal = "HOLD"
        meta["signal_type"] = "wait"
        meta["position_direction"] = "neutral"
    
    return {
        "signal": signal,
        "score": round(score, 2),
        "confidence": confidence,
        "reasons": reasons,
        "meta": meta
    }



