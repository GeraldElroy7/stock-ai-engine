import pandas as pd
import numpy as np


def _normalize_signal(sig):
    if sig is None:
        return None
    if isinstance(sig, str):
        return sig
    if isinstance(sig, (list, tuple)) and len(sig) > 0:
        return sig[-1]
    if isinstance(sig, pd.Series) or isinstance(sig, np.ndarray):
        try:
            arr = np.asarray(sig)
            if arr.size == 0:
                return None
            if arr.size == 1:
                return arr.item()
            return arr[-1]
        except Exception:
            return None
    # fallback
    try:
        return str(sig)
    except Exception:
        return None


def backtest(df, initial_capital=100_000_000):
    position = None
    entry_price = 0
    entry_date = None

    trades = []


    for _, row in df.iterrows():
        raw_signal = row["signal"]
        signal = _normalize_signal(raw_signal)

        if signal is None:
            continue

        # normalize price to scalar
        raw_price = row["Close"]
        if isinstance(raw_price, (pd.Series, np.ndarray)):
            arr = np.asarray(raw_price)
            price = float(arr[-1]) if arr.size > 0 else None
        else:
            try:
                price = float(raw_price)
            except Exception:
                price = None

        # ENTRY
        if position is None and signal == "BUY":
            position = "LONG"
            entry_price = price
            entry_date = row.name

        # EXIT
        elif position == "LONG":
            # ensure entry_price and price are scalar numbers
            try:
                change_pct = (price - float(entry_price)) / float(entry_price)
            except Exception:
                change_pct = None

            if signal == "SELL" or (change_pct is not None and change_pct <= -0.05) or (change_pct is not None and change_pct >= 0.10):
                trades.append({
                    "entry_date": entry_date,
                    "exit_date": row.name,
                    "entry_price": entry_price,
                    "exit_price": price,
                    "return_pct": round(change_pct * 100, 2)
                })
                position = None

    return trades
