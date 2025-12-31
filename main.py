"""
REST API for Stock AI Engine
Ready for institutional deployment

Usage:
    pip install fastapi uvicorn
    uvicorn app:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sys
import os
from pathlib import Path

# Add parent directory to path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(parent_dir))

# Change to current directory for relative imports
os.chdir(str(current_dir))

# Import with error reporting
try:
    from data.fetcher import fetch_eod
    from indicators.technical import add_indicators
    from engine.decision import decision_engine
    from config import SIGNAL_CONFIG, BACKTEST_THRESHOLDS
    print("✅ All imports successful from relative paths")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Current dir: {os.getcwd()}")
    print(f"sys.path: {sys.path[:3]}")
    raise

# ===== API MODELS =====

class SignalResponse(BaseModel):
    """Current trading signal for a ticker"""
    ticker: str
    signal: str  # "BUY", "SELL", "HOLD"
    score: float
    confidence: float
    reasons: List[str]
    metadata: dict
    timestamp: str


class BacktestRequest(BaseModel):
    """Request for backtest execution"""
    symbols: List[str]
    lookback_period: str = "6mo"


class BacktestResponse(BaseModel):
    """Backtest results"""
    symbol: str
    total_trades: int
    win_rate: float
    sharpe_ratio: float
    recovery_factor: float
    institution_ready: bool
    report: dict


# ===== FASTAPI APP =====

app = FastAPI(
    title="Stock AI Engine API",
    description="Institutional trading signals & backtesting",
    version="1.0.0"
)


@app.get("/")
def root():
    """API health check"""
    return {
        "status": "operational",
        "service": "Stock AI Engine",
        "version": "1.0.0"
    }


@app.get("/signal/{ticker}")
def get_signal(ticker: str) -> SignalResponse:
    """
    Get current buy/sell/hold signal for a ticker
    
    Args:
        ticker: Stock symbol (e.g., "BBCA")
    
    Returns:
        SignalResponse with current signal and reasons
    
    Example:
        GET /signal/BBCA
    """
    try:
        df = fetch_eod(ticker)
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail=f"No data for {ticker}")
        
        df = add_indicators(df)
        decision = decision_engine(df)
        
        return SignalResponse(
            ticker=ticker,
            signal=decision["signal"],
            score=decision["score"],
            confidence=decision["confidence"],
            reasons=decision["reasons"],
            metadata=decision["meta"],
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/backtest")
def run_backtest(request: BacktestRequest) -> List[BacktestResponse]:
    """
    Run backtest for one or more symbols
    
    Args:
        request: BacktestRequest with list of symbols
    
    Returns:
        List of backtest reports
    
    Example:
        POST /backtest
        {
            "symbols": ["BBCA", "BBRI"],
            "lookback_period": "6mo"
        }
    """
    results = []
    
    for symbol in request.symbols:
        try:
            df = fetch_eod(symbol)
            if df is None or df.empty:
                continue
            
            df = add_indicators(df)
            
            # Prepare backtest data
            records = []
            for i in range(len(df)):
                if i < 50:  # Warmup period
                    records.append({
                        "signal": None, "score": None, "confidence": None,
                        "reasons": None, "meta": None
                    })
                else:
                    temp_df = df.iloc[:i+1]
                    decision = decision_engine(temp_df)
                    records.append(decision)
            
            df["signal"] = [r["signal"] for r in records]
            
            # Run backtest
            trades = backtest(df)
            report = summarize(trades)
            
            results.append(BacktestResponse(
                symbol=symbol,
                total_trades=report.get("total_trades"),
                win_rate=report.get("win_rate"),
                sharpe_ratio=report.get("sharpe_ratio"),
                recovery_factor=report.get("recovery_factor"),
                institution_ready=report.get("institution_ready"),
                report=report
            ))
        
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            continue
    
    return results


@app.get("/portfolio")
def get_portfolio_signals(symbols: str) -> dict:
    """
    Get signals for entire portfolio at once
    
    Args:
        symbols: Comma-separated list (e.g., "BBCA,BBRI,BMRI")
    
    Returns:
        dict with signals for each symbol
    """
    ticker_list = [s.strip() for s in symbols.split(",")]
    signals = {}
    
    for ticker in ticker_list:
        try:
            df = fetch_eod(ticker)
            if df is not None and not df.empty:
                df = add_indicators(df)
                decision = decision_engine(df)
                signals[ticker] = {
                    "signal": decision["signal"],
                    "score": decision["score"],
                    "confidence": decision["confidence"]
                }
        except Exception as e:
            signals[ticker] = {"error": str(e)}
    
    return {
        "portfolio": ticker_list,
        "signals": signals,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/config")
def get_config():
    """Get current signal configuration (for transparency)"""
    return {
        "BUY_THRESHOLD": SIGNAL_CONFIG["BUY_THRESHOLD"],
        "SELL_THRESHOLD": SIGNAL_CONFIG["SELL_THRESHOLD"],
        "BACKTEST_THRESHOLDS": BACKTEST_THRESHOLDS
    }


# ===== HEALTH CHECK =====

@app.get("/health")
def health_check():
    """Kubernetes-style health check"""
    return {"status": "healthy"}


# ===== ERROR HANDLERS =====

@app.exception_handler(Exception)
async def exception_handler(exc: Exception):
    """Global exception handler"""
    return {
        "error": str(exc),
        "timestamp": datetime.now().isoformat()
    }


# ===== DEPLOYMENT INSTRUCTIONS =====

if __name__ == "__main__":
    import uvicorn
    
    # Run: python app.py
    # Then: curl http://localhost:8000/signal/BBCA
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

"""
USAGE EXAMPLES

1. Get current signal:
   curl http://localhost:8000/signal/BBCA

2. Get portfolio signals:
   curl "http://localhost:8000/portfolio?symbols=BBCA,BBRI,BMRI"

3. Run backtest (POST):
   curl -X POST http://localhost:8000/backtest \
     -H "Content-Type: application/json" \
     -d '{"symbols": ["BBCA", "BBRI"]}'

4. Check config:
   curl http://localhost:8000/config

5. Health check:
   curl http://localhost:8000/health

DEPLOYMENT (Docker):

FROM python:3.13
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

Build: docker build -t stock-ai-engine .
Run:   docker run -p 8000:8000 stock-ai-engine
"""
