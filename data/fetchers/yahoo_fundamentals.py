"""
Auto-fetch real fundamental data from Yahoo Finance API.
Saves to data/fund_data/ with local caching.
"""

import os
import json
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "fund_data")
CACHE_AGE_HOURS = 24  # Refresh fundamentals daily


def _get_cached_data(symbol: str) -> Optional[Dict]:
    """Load cached fundamental data if recent enough."""
    cache_file = os.path.join(DATA_DIR, f"{symbol}_cache.json")
    if not os.path.exists(cache_file):
        return None
    
    try:
        with open(cache_file, "r") as f:
            data = json.load(f)
        
        # Check if cache is fresh
        last_updated = datetime.fromisoformat(data.get("_cached_at", "2000-01-01"))
        age = datetime.now() - last_updated
        
        if age < timedelta(hours=CACHE_AGE_HOURS):
            logger.debug(f"{symbol}: Using cached fundamentals (age={age.total_seconds()/3600:.1f}h)")
            return data
    except Exception as e:
        logger.warning(f"Could not read cache for {symbol}: {e}")
    
    return None


def _save_cached_data(symbol: str, data: Dict):
    """Save fundamental data with cache timestamp."""
    os.makedirs(DATA_DIR, exist_ok=True)
    cache_file = os.path.join(DATA_DIR, f"{symbol}_cache.json")
    
    data["_cached_at"] = datetime.now().isoformat()
    try:
        with open(cache_file, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved cache for {symbol}")
    except Exception as e:
        logger.warning(f"Could not save cache for {symbol}: {e}")


def fetch_fundamentals_yahoo(ticker: str, use_cache: bool = True) -> Dict:
    """
    Fetch real fundamental data from Yahoo Finance.
    
    Args:
        ticker: Stock symbol (e.g., "BBCA")
        use_cache: If True, use cached data if <24h old
    
    Returns:
        Dict with fundamental metrics and history
    """
    # Try cache first
    if use_cache:
        cached = _get_cached_data(ticker)
        if cached:
            return cached
    
    try:
        logger.info(f"Fetching fundamentals for {ticker} from Yahoo Finance...")
        
        # Download with .JK suffix for IDX stocks
        stock = yf.Ticker(f"{ticker}.JK")
        
        # Get info dict (latest metrics)
        info = stock.info or {}
        
        # Extract current fundamentals
        current = {
            "year": datetime.now().year,
            "period": f"Q{(datetime.now().month - 1) // 3 + 1}",
            "pe_ratio": info.get("trailingPE") or info.get("forwardPE"),
            "pb_ratio": info.get("priceToBook"),
            "roe_pct": info.get("returnOnEquity"),
            "roa_pct": info.get("returnOnAssets"),
            "dividend_yield_pct": info.get("dividendYield"),
            "revenue_growth_pct": info.get("revenueGrowth"),
            "earnings_growth_pct": info.get("earningsGrowth"),
            "market_cap": info.get("marketCap"),
            "debt_to_equity": info.get("debtToEquity"),
            "current_ratio": info.get("currentRatio"),
            "fetched_at": datetime.now().isoformat()
        }
        
        # Try to get historical data (last 5 years)
        try:
            quarterly = stock.quarterly_financials
            if quarterly is not None and not quarterly.empty:
                # Convert to fundamentals history format
                historical = extract_historical_from_financials(quarterly, ticker)
                result = {
                    "symbol": ticker,
                    "company_name": info.get("longName", ticker),
                    "currency": info.get("currency", "IDR"),
                    "fundamentals": [current] + historical,
                    "source": "Yahoo Finance",
                    "last_updated": datetime.now().isoformat()
                }
            else:
                result = {
                    "symbol": ticker,
                    "company_name": info.get("longName", ticker),
                    "currency": info.get("currency", "IDR"),
                    "fundamentals": [current],
                    "source": "Yahoo Finance",
                    "last_updated": datetime.now().isoformat(),
                    "note": "Only current data available (history not found)"
                }
        except Exception as e:
            logger.warning(f"Could not fetch quarterly data for {ticker}: {e}")
            result = {
                "symbol": ticker,
                "company_name": info.get("longName", ticker),
                "currency": info.get("currency", "IDR"),
                "fundamentals": [current],
                "source": "Yahoo Finance",
                "last_updated": datetime.now().isoformat()
            }
        
        # Save to cache
        _save_cached_data(ticker, result)
        
        return result
    
    except Exception as e:
        logger.error(f"Failed to fetch fundamentals for {ticker}: {e}")
        return {"error": str(e), "symbol": ticker}


def extract_historical_from_financials(financials, ticker: str) -> list:
    """Extract historical fundamental metrics from quarterly financials."""
    history = []
    try:
        # This is complex as Yahoo structure varies; simplified version
        # In production, you'd parse quarterly balance sheets and income statements
        logger.debug(f"Quarterly financials shape for {ticker}: {financials.shape}")
        # For now, return empty (would require detailed financial parsing)
    except Exception as e:
        logger.debug(f"Could not extract history: {e}")
    
    return history


def fetch_fundamentals_indonesia_idx(ticker: str) -> Optional[Dict]:
    """
    Fetch from Indonesia Stock Exchange (IDX) official API if available.
    
    Note: Requires valid API key and endpoint documentation.
    This is a placeholder for future integration.
    """
    # Placeholder for IDX API integration
    # Example: https://api.idx.co.id/data/fundamental/{ticker}
    logger.info(f"IDX API integration pending for {ticker}")
    return None


def auto_fetch_and_cache_portfolio(symbols: list) -> Dict[str, Dict]:
    """
    Auto-fetch fundamentals for a portfolio of symbols.
    Returns dict of symbol -> fundamentals.
    """
    results = {}
    for symbol in symbols:
        try:
            results[symbol] = fetch_fundamentals_yahoo(symbol, use_cache=True)
        except Exception as e:
            logger.error(f"Failed for {symbol}: {e}")
            results[symbol] = {"error": str(e)}
    
    return results


if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    
    print("\n=== Fetching Real Fundamentals ===")
    
    # Test single stock
    bbca = fetch_fundamentals_yahoo("BBCA")
    print(f"\nBBCA: {bbca.get('fundamentals', [{}])[0]}")
    
    # Test portfolio
    portfolio = auto_fetch_and_cache_portfolio(["BBCA", "BBRI", "BMRI"])
    for symbol, data in portfolio.items():
        if "error" not in data:
            print(f"{symbol}: PE={data['fundamentals'][0].get('pe_ratio')}")
        else:
            print(f"{symbol}: {data['error']}")
