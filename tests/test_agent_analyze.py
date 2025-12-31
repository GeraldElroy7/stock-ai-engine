#!/usr/bin/env python3
"""Quick test of /agent/analyze endpoint with COIN (US) and BBCA (IDX)"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("\n=== Testing /agent/analyze Endpoint ===\n")

# Test 1: COIN (US stock)
print("Test 1: COIN (US stock, swing trader, moderate risk)")
payload = {
    "symbols": ["COIN"],
    "trading_style": "swing",
    "risk_level": "moderate",
    "mode": "both"
}
response = client.post("/agent/analyze", json=payload)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    if data.get("results"):
        result = data["results"][0]
        if "error" not in result:
            print(f"Symbol: {result['symbol']}")
            print(f"Trading Style: {result['layout'].get('trading_style')}")
            print(f"Recommendation: {result['recommendation'][:100]}...")
            print(f"Risk/Trade: {result['layout']['risk_management']['risk_per_trade_pct']}%")
            print("✅ COIN test PASSED\n")
        else:
            print(f"❌ Error: {result['error']}\n")
else:
    print(f"❌ Status {response.status_code}\n")

# Test 2: BBCA (IDX stock)
print("Test 2: BBCA (IDX stock, value investor, conservative)")
payload = {
    "symbols": ["BBCA"],
    "trading_style": "value",
    "risk_level": "conservative",
    "mode": "both"
}
response = client.post("/agent/analyze", json=payload)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    if data.get("results"):
        result = data["results"][0]
        if "error" not in result:
            print(f"Symbol: {result['symbol']}")
            print(f"Trading Style: {result['layout'].get('trading_style')}")
            print(f"Recommendation: {result['recommendation'][:100]}...")
            print(f"Risk/Trade: {result['layout']['risk_management']['risk_per_trade_pct']}%")
            print("✅ BBCA test PASSED\n")
        else:
            print(f"❌ Error: {result['error']}\n")
else:
    print(f"❌ Status {response.status_code}\n")

print("=== Tests Complete ===\n")
