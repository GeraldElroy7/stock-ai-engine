import os
import json
from typing import Dict

DATA_DIR = os.path.join(os.path.dirname(__file__), "fund_data")


def fetch_fundamentals(symbol: str) -> Dict:
    """Fetch basic fundamental metrics for a symbol.

    Looks for a JSON file at data/fund_data/{symbol}.json. If not found,
    returns a small mocked dict so the pipeline can run.
    """
    try:
        path = os.path.join(DATA_DIR, f"{symbol}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass

    # Fallback mock values (these will be replaced when you provide real data)
    return {
        "symbol": symbol,
        "pe_ratio": None,
        "pb_ratio": None,
        "roe_pct": None,
        "revenue_growth_pct": None,
        "market_cap_usd": None,
        "note": "mocked - provide real fundamentals in data/fund_data/{symbol}.json"
    }
