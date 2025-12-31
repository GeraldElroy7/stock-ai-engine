#!/usr/bin/env python
"""
Test SHORT signals directly (no API)
Gunakan ini untuk verify SHORT signal logic bekerja
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from data.fetcher import fetch_eod
from indicators.technical import add_indicators
from engine.decision import decision_engine

TICKERS = ["BBCA", "BBRI", "ANTM", "UNVR"]

print("=" * 80)
print("LIVE SIGNAL TEST - SHORT SIGNALS")
print("=" * 80)
print()

for ticker in TICKERS:
    print(f"\n{'=' * 50}")
    print(f"Testing: {ticker}")
    print(f"{'=' * 50}")
    
    try:
        # Fetch with 1y timeframe
        df = fetch_eod(ticker)
        if df is None or df.empty:
            print(f"❌ No data for {ticker}")
            continue
        
        print(f"✅ Fetched {len(df)} bars")
        
        # Add indicators
        df = add_indicators(df)
        print(f"✅ Indicators calculated")
        
        # Generate signal
        signal = decision_engine(df)
        
        # Display results
        print(f"\n📊 CURRENT SIGNAL:")
        print(f"  Signal:      {signal['signal']}")
        print(f"  Score:       {signal['score']:.2f}")
        print(f"  Confidence:  {signal['confidence']:.1%}")
        print(f"  Position:    {signal['meta'].get('position_direction', 'N/A')}")
        print(f"  Trend:       {signal['meta'].get('trend_strength', 'N/A')}")
        
        print(f"\n💡 REASONS ({len(signal['reasons'])} factors):")
        for i, reason in enumerate(signal['reasons'], 1):
            print(f"  {i}. {reason}")
        
        # Check if SHORT signal
        if signal['signal'] == 'SHORT':
            print(f"\n⚡ SHORT SIGNAL DETECTED!")
            print(f"   → Entry price: {signal['meta'].get('close', 'N/A'):.0f}")
            print(f"   → Expected decline based on: {signal['meta'].get('trend_strength')}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

print(f"\n{'=' * 80}")
print("TEST COMPLETE")
print(f"{'=' * 80}")
