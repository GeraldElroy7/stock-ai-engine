#!/usr/bin/env python
"""Test API endpoints using FastAPI TestClient"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("=" * 60)
print("Testing API endpoints with TestClient")
print("=" * 60)

# Test 1: Root endpoint
print("\n1. Testing GET / endpoint...")
try:
    response = client.get("/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Backtest endpoint
print("\n2. Testing POST /backtest endpoint...")
try:
    response = client.post("/backtest", json={"symbols": ["BBCA"]})
    print(f"   Status: {response.status_code}")
    data = response.json()
    if isinstance(data, list) and len(data) > 0:
        print(f"   Trades found: {data[0].get('total_trades')}")
        print(f"   Win rate: {data[0].get('win_rate')}%")
        print(f"   ✅ Backtest endpoint working!")
    else:
        print(f"   Response: {data}")
except Exception as e:
    print(f"   Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Tests complete!")
print("=" * 60)
