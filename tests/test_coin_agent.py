#!/usr/bin/env python3
"""Test /agent/analyze directly without full server"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Simulate the endpoint logic
from data.fetcher import fetch_eod
from indicators.technical import add_indicators
from engine.decision import decision_engine
from data.fundamentals import fetch_fundamentals
from engine.ai_agent import generate_layout, synthesize_recommendation
from engine.ai_summary import summarize_analysis
import json

def _convert_numpy_types(obj):
    """Recursively convert numpy types to native Python types for JSON serialization."""
    import numpy as np
    
    if isinstance(obj, dict):
        return {k: _convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_convert_numpy_types(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

print("\n=== Testing Agent Analyze with COIN ===\n")

symbol = "COIN"
is_us = True  # COIN is US stock
trading_style = "swing"
risk_level = "moderate"
mode = "both"

try:
    print(f"Fetching data for {symbol}...")
    df = fetch_eod(symbol, is_us=is_us)
    
    if df is None or df.empty:
        print(f"❌ No data for {symbol}")
    else:
        print(f"✅ Got {len(df)} rows of data")
        
        df = add_indicators(df)
        print("✅ Added indicators")
        
        tech = decision_engine(df)
        print(f"✅ Technical signal: {tech.get('signal')} (score={tech.get('score'):.2f})")
        
        fund = fetch_fundamentals(symbol)
        print(f"✅ Got fundamentals")
        
        df5y = fetch_eod(symbol, use_5y=True, is_us=is_us)
        tech_data_5y = None
        if df5y is not None and not df5y.empty:
            tech_data_5y = add_indicators(df5y)
            print(f"✅ Got 5Y data ({len(df5y)} rows)")
        
        layout = generate_layout(trading_style, risk_level, symbol)
        print("✅ Generated layout")
        
        summary = summarize_analysis(tech, fund, mode=mode, tech_data=tech_data_5y)
        print("✅ Generated summary")
        
        recommendation = synthesize_recommendation(
            summary.get("technical_score", 0),
            summary.get("fundamental_score", 0),
            layout,
            symbol
        )
        print(f"✅ Recommendation: {recommendation[:80]}...")
        
        # Test JSON serialization
        layout_clean = _convert_numpy_types(layout)
        summary_clean = _convert_numpy_types(summary)
        
        result = {
            "symbol": symbol,
            "layout": layout_clean,
            "summary": summary_clean,
            "recommendation": recommendation
        }
        
        json_str = json.dumps(result, indent=2, default=str)
        print(f"\n✅ JSON serialization successful ({len(json_str)} bytes)")
        print("\nFinal result structure:")
        print(f"  Symbol: {result['symbol']}")
        print(f"  Trading Style: {result['layout']['trading_style']}")
        print(f"  Risk/Trade: {result['layout']['risk_management']['risk_per_trade_pct']}%")
        print(f"  Technical Score: {result['summary']['technical_score']}")
        print(f"  Recommendation: {result['recommendation'][:60]}...")
        
        print("\n✅ ALL TESTS PASSED!\n")

except Exception as e:
    import traceback
    print(f"\n❌ Error: {e}")
    traceback.print_exc()
    print()
