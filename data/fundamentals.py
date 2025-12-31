import os
import json
from typing import Dict

DATA_DIR = os.path.join(os.path.dirname(__file__), "fund_data")


def fetch_fundamentals(symbol: str) -> Dict:
    """
    Fetch fundamental metrics for a symbol.
    
    Looks for JSON files in data/fund_data/:
    1. First tries {symbol}_2025Q2.json (latest 2025 Q2 data)
    2. Falls back to {symbol}.json (historical or backup)
    3. Returns mock if not found
    
    Returns Dict with fundamentals history (newest first).
    """
    try:
        # Try 2025 Q2 data first (most recent)
        path_2025 = os.path.join(DATA_DIR, f"{symbol}_2025Q2.json")
        if os.path.exists(path_2025):
            with open(path_2025, "r", encoding="utf-8") as f:
                return json.load(f)
        
        # Fallback to main file
        path = os.path.join(DATA_DIR, f"{symbol}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass

    # Fallback mock values
    return {
        "symbol": symbol,
        "fundamentals": [
            {
                "year": 2025,
                "period": "Q2",
                "pe_ratio": None,
                "pb_ratio": None,
                "roe_pct": None,
                "revenue_growth_pct": None,
            }
        ],
        "note": "mocked - provide real fundamentals in data/fund_data/{symbol}_2025Q2.json"
    }

