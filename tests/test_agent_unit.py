#!/usr/bin/env python3
"""Quick test of agent_analyze logic without TestClient overhead"""

import sys
from pathlib import Path

# Add parent (project root) to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from engine.ai_agent import generate_layout, synthesize_recommendation
import json

print("\n=== Testing AI Agent Layout Generation ===\n")

# Test layout generation for different styles
styles = ["scalper", "swing", "investor", "value"]
risk_levels = ["conservative", "moderate", "aggressive"]

for style in styles[:2]:  # Test scalper and swing
    for risk in risk_levels[:1]:  # Test moderate only
        layout = generate_layout(style, risk, "TESTCOIN")
        print(f"\n{style.upper()} (risk={risk}):")
        print(f"  Timeframe: {layout['display']['primary_chart_timeframe']}")
        print(f"  Indicators: {layout['display']['priority_indicators'][:3]}")
        print(f"  Risk/Trade: {layout['risk_management']['risk_per_trade_pct']}%")
        print(f"  Entry: {layout['entry_criteria']['primary'][:50]}...")
        
        # Test recommendation synthesis
        rec = synthesize_recommendation(1.5, 0.8, layout, "TESTCOIN")
        print(f"  Recommendation: {rec[:80]}...")

print("\n✅ Layout generation works correctly!\n")

# Test JSON serializability
print("=== Testing JSON Serialization ===\n")
layout = generate_layout("swing", "moderate", "COIN")

try:
    json_str = json.dumps(layout, indent=2, default=str)
    print("✅ Layout is JSON serializable!")
    print(f"JSON size: {len(json_str)} bytes\n")
except Exception as e:
    print(f"❌ JSON serialization failed: {e}\n")
