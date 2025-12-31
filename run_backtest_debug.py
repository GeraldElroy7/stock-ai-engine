from main import run_backtest, BacktestRequest
import json, traceback
req = BacktestRequest(symbols=["BBCA","BBRI"], lookback_period="6mo")
try:
    res = run_backtest(req)
    print(json.dumps(res, indent=2, ensure_ascii=False))
except Exception:
    traceback.print_exc()
