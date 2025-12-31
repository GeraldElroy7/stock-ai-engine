import yfinance as yf
import pandas as pd
import sys
from pathlib import Path

# Import config for dynamic timeframe
try:
    from config import DATA_CONFIG
except (ImportError, ModuleNotFoundError):
    parent_dir = str(Path(__file__).parent.parent)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    try:
        from config import DATA_CONFIG
    except (ImportError, ModuleNotFoundError):
        DATA_CONFIG = {"LOOKBACK_PERIOD": "1y"}

def fetch_eod(ticker, use_5y=False, is_us=False):
    """
    Fetch end-of-day data for a ticker with error handling and timeout.
    
    Args:
        ticker: Stock symbol (e.g., "BBCA" for IDX, "COIN" for US)
        use_5y: If True, fetch 5 years for pattern recognition; else use config LOOKBACK_PERIOD
        is_us: If True, fetch as US stock (no .JK suffix); else assume IDX stock
    
    Returns:
        DataFrame with OHLCV data or None if failed
    """
    try:
        lookback = "5y" if use_5y else DATA_CONFIG.get("LOOKBACK_PERIOD", "1y")
        
        # Auto-detect: if US stock, don't add .JK; if IDX, add .JK
        symbol = ticker if is_us else f"{ticker}.JK"
        
        print(f"  Fetching data for {ticker} ({lookback})...", end=" ", flush=True)
        df = yf.download(
            symbol,
            period=lookback,
            interval="1d",
            auto_adjust=True,
            progress=False,
            timeout=30
        )
        
        if df is None or df.empty:
            print("❌ No data")
            return None
        
        print("✓")
        
        # Fix for MultiIndex columns returned by yfinance
        # The returned df has columns like ('Close', 'BBCA.JK'), ('High', 'BBCA.JK'), etc.
        if isinstance(df.columns, pd.MultiIndex):
            # Flatten MultiIndex columns to single level
            df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        
        # Ensure we have the required columns
        required = ["Open", "High", "Low", "Close", "Volume"]
        for col in required:
            if col not in df.columns:
                print(f"❌ Missing column: {col}")
                return None
        
        return df
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None
