from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

payload = {
    "symbols": ["BBCA", "BBRI"],
    "trading_style": "swing",
    "risk_level": "moderate",
    "mode": "both",
    "save": False
}

resp = client.post('/agent/analyze', json=payload)
print('status', resp.status_code)
try:
    js = resp.json()
    for r in js.get('results', []):
        print(r['symbol'], '->', r.get('recommendation'))
except Exception as e:
    print('failed to parse response:', e)
    print(resp.text)
