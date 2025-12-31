#!/usr/bin/env python
"""Test script to verify backtest imports work correctly"""

from data.fetcher import fetch_eod
from indicators.technical import add_indicators
from engine.decision import decision_engine
from backtest.simple_backtest import backtest
from backtest.report import summarize

print("Testing backtest functions...")

# Test with BBCA
df = fetch_eod("BBCA")
print(f"✓ Data fetched: {df.shape}")

df = add_indicators(df)
print(f"✓ Indicators added: {len(df.columns)} columns")

# Simulate backtest
records = []
for i in range(len(df)):
    if i < 50:
        records.append({"signal": None, "score": None, "confidence": None, "reasons": None, "meta": None})
    else:
        temp_df = df.iloc[:i+1]
        decision = decision_engine(temp_df)
        records.append(decision)

df["signal"] = [r["signal"] for r in records]
print(f"✓ Signals generated: {len([s for s in df['signal'] if s])}")

# Run backtest
trades = backtest(df)
print(f"✓ Trades generated: {len(trades)}")

# Summarize
report = summarize(trades)
print(f"✓ Report created: {len(report)} metrics")

print("\n✅ SUCCESS: All backtest functions work correctly!")
print(f"   - Backtest & summarize imports are working")
print(f"   - No NameError on 'backtest' or 'summarize'")
