"""
REST API for Stock AI Engine
Ready for institutional deployment

Usage:
    pip install fastapi uvicorn
    uvicorn app:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sys
import os
from pathlib import Path
import json
import pandas as pd

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
    from backtest.simple_backtest import backtest
    from backtest.report import summarize
    from data.fundamentals import fetch_fundamentals
    from engine.ai_summary import summarize_analysis
    from data.fetchers.yahoo_fundamentals import fetch_fundamentals_yahoo, auto_fetch_and_cache_portfolio
    from engine.ai_agent import generate_layout, synthesize_recommendation
    print("✅ All imports successful from relative paths")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Current dir: {os.getcwd()}")
    print(f"sys.path: {sys.path[:3]}")
    raise


# ===== Helpers: saving results =====
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

def _save_json(obj, filename: str):
    path = RESULTS_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return str(path)


def _save_trades_csv(trades, filename: str):
    path = RESULTS_DIR / filename
    try:
        df = pd.DataFrame(trades)
        df.to_csv(path, index=False)
        return str(path)
    except Exception:
        # fallback - save as json
        _save_json(trades, filename + ".json")
        return str(path) + ".json"


def _convert_numpy_types(obj):
    """Recursively convert numpy types to native Python types for JSON serialization."""
    import numpy as np
    
    if isinstance(obj, dict):
        return {k: _convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_convert_numpy_types(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

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
    save: Optional[bool] = False


class AnalysisRequest(BaseModel):
    symbols: List[str]
    mode: Optional[str] = "both"  # technical, fundamental, or both
    save: Optional[bool] = False


class AgentAnalysisRequest(BaseModel):
    symbols: List[str]
    trading_style: Optional[str] = "swing"  # scalper, swing, investor, value
    risk_level: Optional[str] = "moderate"  # conservative, moderate, aggressive
    mode: Optional[str] = "both"
    save: Optional[bool] = False


class AnalysisResponse(BaseModel):
    symbol: str
    technical: Optional[dict]
    fundamental: Optional[dict]
    summary: Optional[dict]


class FundamentalRefreshRequest(BaseModel):
    """Request to refresh fundamental data"""
    symbols: List[str]


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
def run_backtest(request: BacktestRequest):
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
                results.append({"symbol": symbol, "error": "no data"})
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

            # Safe extract signals (some decisions may be missing keys)
            df["signal"] = [r.get("signal") if isinstance(r, dict) else None for r in records]

            # Run backtest (may raise) and summarize
            trades = backtest(df)
            report = summarize(trades)

            # Ensure report contains only JSON-serializable native types
            try:
                report_clean = jsonable_encoder(report)
            except Exception:
                # Fallback: convert numpy scalars to native Python types
                import numpy as _np
                report_clean = {}
                for k, v in (report or {}).items():
                    if isinstance(v, (_np.integer,)):
                        report_clean[k] = int(v)
                    elif isinstance(v, (_np.floating,)):
                        report_clean[k] = float(v)
                    elif isinstance(v, (_np.bool_,)):
                        report_clean[k] = bool(v)
                    else:
                        report_clean[k] = v

            # Save results if requested
            saved_paths = {}
            if getattr(request, 'save', False):
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                # save trades
                try:
                    trades_path = _save_trades_csv(trades, f"trades_{symbol}_{ts}.csv")
                    saved_paths['trades'] = trades_path
                except Exception:
                    pass
                # save report
                try:
                    report_path = _save_json(report_clean, f"report_{symbol}_{ts}.json")
                    saved_paths['report'] = report_path
                except Exception:
                    pass

            results.append({
                "symbol": symbol,
                "report": report_clean,
                "saved": saved_paths
            })

        except Exception as e:
            import traceback, logging
            logging.exception(f"Backtest error for {symbol}")
            results.append({"symbol": symbol, "error": str(e)})

    return {"ok": True, "results": results, "timestamp": datetime.now().isoformat()}


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


@app.post("/analysis")
def run_analysis(request: AnalysisRequest):
    """Run combined analysis (technical + fundamental) with 5-year patterns and AI insights."""
    results = []
    for symbol in request.symbols:
        tech = None
        fund = None
        tech_data_5y = None
        try:
            # Technical analysis (1-year by default)
            df = fetch_eod(symbol)
            if df is not None and not df.empty and request.mode in ("technical", "both"):
                df = add_indicators(df)
                tech = decision_engine(df)
            
            # 5-year technical data for pattern recognition
            if request.mode in ("technical", "both"):
                try:
                    df_5y = fetch_eod(symbol, use_5y=True)
                    if df_5y is not None and not df_5y.empty:
                        tech_data_5y = add_indicators(df_5y)
                except:
                    pass  # Fallback to 1-year if 5-year fails
            
            # Fundamentals
            if request.mode in ("fundamental", "both"):
                fund = fetch_fundamentals(symbol)

            # AI summary with 5-year pattern analysis
            summary = summarize_analysis(tech, fund, mode=request.mode or "both", tech_data=tech_data_5y)

            # Save analysis if requested
            saved_paths = {}
            if getattr(request, 'save', False):
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                try:
                    summary_path = _save_json(summary, f"analysis_summary_{symbol}_{ts}.json")
                    saved_paths['summary'] = summary_path
                except Exception:
                    pass
                try:
                    _save_json(fund or {}, f"analysis_fund_{symbol}_{ts}.json")
                    saved_paths['fundamental'] = str(RESULTS_DIR / f"analysis_fund_{symbol}_{ts}.json")
                except Exception:
                    pass

            results.append({
                "symbol": symbol,
                "technical": jsonable_encoder(tech),
                "fundamental": jsonable_encoder(fund),
                "summary": jsonable_encoder(summary),
                "pattern_analysis": jsonable_encoder(summary.get("pattern_analysis", {})),
                "saved": saved_paths
            })

        except Exception as e:
            import logging
            logging.exception(f"Analysis error for {symbol}")
            results.append({"symbol": symbol, "error": str(e)})

    return {"ok": True, "results": results, "timestamp": datetime.now().isoformat()}


@app.get("/config")
def get_config():
    """Get current signal configuration (for transparency)"""
    return {
        "BUY_THRESHOLD": SIGNAL_CONFIG["BUY_THRESHOLD"],
        "SELL_THRESHOLD": SIGNAL_CONFIG["SELL_THRESHOLD"],
        "BACKTEST_THRESHOLDS": BACKTEST_THRESHOLDS
    }


@app.get("/fundamental/refresh")
def refresh_fundamental(symbol: str):
    """
    Manually fetch and cache latest fundamental data from Yahoo Finance.
    
    Args:
        symbol: Stock symbol (e.g., "BBCA")
    
    Returns:
        Fresh fundamental data or error
    
    Example:
        GET /fundamental/refresh?symbol=BBCA
    """
    try:
        result = fetch_fundamentals_yahoo(symbol, use_cache=False)  # Force refresh
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "ok": True,
            "symbol": symbol,
            "fundamentals": result.get("fundamentals", []),
            "source": result.get("source", "unknown"),
            "updated_at": result.get("last_updated")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/fundamental/refresh-portfolio")
def refresh_portfolio(request: FundamentalRefreshRequest):
    """
    Batch fetch fundamentals for multiple symbols.
    
    Args:
        symbols: List of symbols
    
    Returns:
        Dict of symbol -> fundamental data
    
    Example:
        POST /fundamental/refresh-portfolio
        {"symbols": ["BBCA", "BBRI", "BMRI"]}
    """
    try:
        symbols = request.symbols
        if not symbols:
            raise HTTPException(status_code=400, detail="No symbols provided")
        
        results = auto_fetch_and_cache_portfolio(symbols)
        return {
            "ok": True,
            "count": len(results),
            "results": {
                sym: {
                    "fundamentals": data.get("fundamentals", [])[:1],  # Latest only
                    "source": data.get("source", "unknown")
                } if "error" not in data else {"error": data["error"]}
                for sym, data in results.items()
            },
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agent/analyze")
def agent_analyze(request: AgentAnalysisRequest):
    """
    Analyze symbols with a trading-style AI agent and return customized layouts.

    Request JSON example:
    {
      "symbols": ["BBCA", "BBRI"],
      "trading_style": "swing",
      "risk_level": "moderate",
      "mode": "both",
      "save": false
    }
    """
    results = []
    for symbol in request.symbols:
        try:
            # Auto-detect US vs IDX stocks
            is_us = symbol.isupper() and len(symbol) <= 4 and symbol not in ["BBCA", "BBRI", "BMRI", "ASII", "UNTR"]
            
            # Fetch technical (1y) and 5y for patterns
            df = fetch_eod(symbol, is_us=is_us)
            tech = None
            tech_data_5y = None
            if df is not None and not df.empty:
                df = add_indicators(df)
                tech = decision_engine(df)

            try:
                df5 = fetch_eod(symbol, use_5y=True, is_us=is_us)
                if df5 is not None and not df5.empty:
                    tech_data_5y = add_indicators(df5)
            except:
                tech_data_5y = None

            # Fundamentals (prefer cached recent or local file)
            fund = fetch_fundamentals(symbol)

            # Generate layout and recommendation
            layout = generate_layout(request.trading_style or "swing", request.risk_level or "moderate", symbol)
            summary = summarize_analysis(tech, fund, mode=request.mode or "both", tech_data=tech_data_5y)
            recommendation_text = synthesize_recommendation(summary.get("technical_score", 0), summary.get("fundamental_score", 0), layout, symbol)

            # Convert numpy types in layout and summary
            layout_clean = _convert_numpy_types(layout)
            summary_clean = _convert_numpy_types(summary)

            # Optional save
            saved = {}
            if getattr(request, 'save', False):
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                try:
                    saved['layout'] = _save_json(layout_clean, f"agent_layout_{symbol}_{ts}.json")
                except Exception:
                    pass

            results.append({
                "symbol": symbol,
                "layout": jsonable_encoder(layout_clean),
                "summary": jsonable_encoder(summary_clean),
                "recommendation": recommendation_text,
                "saved": saved
            })
        except Exception as e:
            import logging
            logging.exception(f"Agent analyze error for {symbol}")
            results.append({"symbol": symbol, "error": str(e)})

    return {"ok": True, "results": results, "timestamp": datetime.now().isoformat()}


# ===== HEALTH CHECK =====

@app.get("/health")
def health_check():
    """Kubernetes-style health check"""
    return {"status": "healthy"}


# ===== ERROR HANDLERS =====

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    """Global exception handler that returns JSONResponse"""
    # Ensure we return a proper Response object with JSON serializable content
    content = {"error": str(exc), "timestamp": datetime.now().isoformat()}
    return JSONResponse(status_code=500, content=content)


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
