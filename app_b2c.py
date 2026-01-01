"""
Stock AI Engine - Main Application with B2C Features
Enhanced API with authentication, comprehensive stock info, and webhooks
Author: Stock AI Engine Team
Date: January 1, 2026
Version: 2.0.0
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import sys
from pathlib import Path

# Add directories to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import original routes from main.py
from main import app as original_app

# Import new B2C routes
from api.b2c_endpoints import setup_b2c_routes
from api.auth import setup_auth_routes

# Create new enhanced app
app = FastAPI(
    title="Stock AI Engine - B2C Platform",
    description="""
    🎯 **Stock AI Engine API - Production Ready**
    
    Platform analisis saham lengkap dengan AI-powered insights untuk retail investors.
    
    ## 🌟 Key Features
    
    ### 📊 Comprehensive Stock Analysis
    - **120+ Indonesian Stocks** - IDX-30, LQ45, dan semua sektor utama
    - **10-Year Historical Data** - Analisis mendalam dengan 2,520 trading days
    - **Technical Analysis** - 9+ indicators (RSI, MACD, EMA, Bollinger Bands, dll)
    - **Fundamental Analysis** - P/E, PB, ROE, Debt-to-Equity, Dividend Yield, dll
    - **AI Recommendations** - Smart insights berdasarkan technical + fundamental
    
    ### 🎨 Personalization
    - **Trading Style** - Scalper, Day Trader, Swing Trader, Position Trader, Long-term Investor
    - **Risk Level** - Conservative, Moderate, Aggressive, Very Aggressive
    - **Investment Goals** - Capital Preservation, Income, Balanced Growth, Appreciation
    - **Sector Preferences** - Customize sector focus
    - **Capital Size** - Personalized position sizing
    
    ### 🔐 Authentication
    - **JWT-Based** - Secure token authentication
    - **User Management** - Registration, login, profile
    - **Premium Tiers** - Free and Premium subscriptions
    
    ### 🔔 Webhooks
    - **Real-time Alerts** - Signal changes, price alerts
    - **Customizable** - Set your own alert conditions
    - **Multi-ticker Support** - Monitor multiple stocks
    
    ## 🚀 Quick Start
    
    ### 1. Register Account
    ```
    POST /api/v2/auth/register
    {
      "email": "your@email.com",
      "password": "yourpassword"
    }
    ```
    
    ### 2. Login
    ```
    POST /api/v2/auth/login
    {
      "email": "your@email.com",
      "password": "yourpassword"
    }
    ```
    
    Demo Account:
    - Email: demo@example.com
    - Password: demo123
    
    ### 3. Get Stock Info
    ```
    POST /api/v2/stock/info
    Authorization: Bearer <your_token>
    {
      "ticker": "BBCA",
      "user_preferences": {
        "trading_style": "swing_trader",
        "risk_level": "moderate",
        "capital_size": 50000000
      }
    }
    ```
    
    ## 📚 Documentation Sections
    
    - **V1 Endpoints** - Legacy endpoints (kept for backward compatibility)
    - **V2 Auth** - Authentication system (register, login, refresh)
    - **V2 Stock** - Comprehensive stock information API
    - **V2 Webhooks** - Real-time alert system
    - **V2 User** - User parameters and preferences
    
    ## 💡 User Input Parameters
    
    Check `/api/v2/user/parameters` untuk list lengkap parameter yang bisa user input:
    - trading_style: scalper | day_trader | swing_trader | position_trader | long_term_investor
    - risk_level: conservative | moderate | aggressive | very_aggressive
    - capital_size: Modal dalam IDR (min: 1,000,000)
    - investment_goal: capital_preservation | income_generation | balanced_growth | capital_appreciation | aggressive_growth
    - sector_preference: List sektor yang disukai
    - exclude_sectors: List sektor yang dihindari
    - min_confidence_level: Minimum confidence untuk signal (0-100)
    - enable_short_signals: true | false
    - time_horizon: short_term | medium_term | long_term
    
    ## 🎯 Response Format
    
    All endpoints return consistent JSON format:
    ```json
    {
      "ticker": "BBCA",
      "company_info": {...},
      "current_price": 10000,
      "technical_analysis": {...},
      "fundamental_analysis": {...},
      "trading_signal": {
        "signal": "BUY",
        "confidence": 78.5,
        "score": 6.5
      },
      "ai_recommendation": {
        "summary": "✅ STRONG BUY signal...",
        "action_items": [...]
      },
      "risk_assessment": {...},
      "personalized_insights": {...}
    }
    ```
    
    ## 🔗 Resources
    
    - GitHub: https://github.com/GeraldElroy7/stock-ai-engine
    - Documentation: /docs
    - Status: [PROJECT_STATUS.md](https://github.com/GeraldElroy7/stock-ai-engine/blob/main/PROJECT_STATUS.md)
    
    ## 📞 Support
    
    For API support and questions:
    - GitHub Issues: https://github.com/GeraldElroy7/stock-ai-engine/issues
    - Email: support@stockaiengine.com (placeholder)
    
    ---
    
    **Version:** 2.0.0  
    **Last Updated:** January 1, 2026  
    **Status:** Production Ready ✅
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Health & Info",
            "description": "API status and information endpoints"
        },
        {
            "name": "V1 - Legacy Endpoints",
            "description": "Original endpoints (backward compatible)"
        },
        {
            "name": "V2 - Authentication",
            "description": "🔐 User authentication system - Register, login, and manage tokens"
        },
        {
            "name": "V2 - Stock Information",
            "description": "📊 Comprehensive stock data with AI insights and personalization"
        },
        {
            "name": "V2 - Webhooks",
            "description": "🔔 Real-time alert system for signal changes and price movements"
        },
        {
            "name": "V2 - User Management",
            "description": "👤 User preferences and parameter management"
        }
    ]
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== ROOT ENDPOINTS =====

@app.get("/", tags=["Health & Info"])
async def root():
    """
    **API Root** 🏠
    
    Welcome endpoint with API information and quick links
    """
    return {
        "status": "operational",
        "service": "Stock AI Engine - B2C Platform",
        "version": "2.0.0",
        "features": [
            "120+ Indonesian Stocks",
            "10-Year Historical Data",
            "Technical + Fundamental Analysis",
            "AI-Powered Recommendations",
            "User Personalization",
            "JWT Authentication",
            "Webhook Alerts"
        ],
        "quick_links": {
            "documentation": "/docs",
            "redoc": "/redoc",
            "register": "/api/v2/auth/register",
            "login": "/api/v2/auth/login",
            "stock_info": "/api/v2/stock/info",
            "supported_stocks": "/api/v2/stocks/list",
            "user_parameters": "/api/v2/user/parameters"
        },
        "demo_account": {
            "email": "demo@example.com",
            "password": "demo123",
            "note": "Use this account to test the API"
        },
        "github": "https://github.com/GeraldElroy7/stock-ai-engine",
        "last_updated": "2026-01-01"
    }


@app.get("/health", tags=["Health & Info"])
async def health_check():
    """
    **Health Check** ❤️
    
    Simple health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "service": "stock-ai-engine",
        "version": "2.0.0",
        "timestamp": "2026-01-01"
    }


@app.get("/api-info", tags=["Health & Info"])
async def api_info():
    """
    **API Information** ℹ️
    
    Detailed API information and capabilities
    """
    return {
        "name": "Stock AI Engine API",
        "version": "2.0.0",
        "description": "AI-powered stock analysis platform for Indonesian market",
        "capabilities": {
            "stocks_supported": 120,
            "data_lookback": "10 years",
            "indicators": ["RSI", "MACD", "EMA", "Bollinger Bands", "ATR", "Volume", "Stochastic", "ADX", "OBV"],
            "fundamental_metrics": ["P/E", "P/B", "ROE", "ROA", "Debt-to-Equity", "Dividend Yield", "EPS Growth"],
            "signal_types": ["BUY", "SELL", "HOLD", "SHORT"],
            "authentication": "JWT Bearer Token",
            "personalization": True,
            "webhooks": True
        },
        "api_versions": {
            "v1": "Legacy endpoints (backward compatible)",
            "v2": "Enhanced B2C platform with auth and personalization"
        },
        "rate_limits": {
            "free_tier": "60 requests/hour",
            "premium_tier": "1000 requests/hour"
        },
        "support": {
            "documentation": "/docs",
            "github": "https://github.com/GeraldElroy7/stock-ai-engine",
            "email": "support@stockaiengine.com"
        }
    }


# ===== MOUNT V1 ENDPOINTS (Legacy) =====

# Copy V1 routes from original app and add tags
@app.get("/signal/{ticker}", tags=["V1 - Legacy Endpoints"])
async def get_signal_v1(ticker: str):
    """
    **[V1] Get Signal** (Legacy)
    
    Get trading signal for a ticker - original endpoint for backward compatibility
    
    **Recommended:** Use `/api/v2/stock/info` for comprehensive analysis
    """
    # Import and call original function
    from main import get_signal
    return get_signal(ticker)


@app.post("/backtest", tags=["V1 - Legacy Endpoints"])
async def run_backtest_v1(request: dict):
    """
    **[V1] Run Backtest** (Legacy)
    
    Run backtest on historical data - original endpoint
    """
    from main import run_backtest, BacktestRequest
    req = BacktestRequest(**request)
    return run_backtest(req)


@app.get("/portfolio", tags=["V1 - Legacy Endpoints"])
async def get_portfolio_v1(symbols: str):
    """
    **[V1] Portfolio Signals** (Legacy)
    
    Get signals for multiple stocks - original endpoint
    """
    from main import get_portfolio_signals
    return get_portfolio_signals(symbols)


# ===== SETUP V2 ROUTES =====

# Setup authentication routes
setup_auth_routes(app)

# Setup B2C routes
setup_b2c_routes(app)


# ===== ERROR HANDLERS =====

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Not Found",
        "message": "The requested endpoint does not exist",
        "suggestion": "Check /docs for available endpoints",
        "status_code": 404
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "suggestion": "Please try again or contact support",
        "status_code": 500
    }


# ===== STARTUP EVENT =====

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("=" * 60)
    print("🚀 Stock AI Engine - B2C Platform")
    print("=" * 60)
    print("✅ Version: 2.0.0")
    print("✅ Status: Production Ready")
    print("✅ Stocks: 120+ Indonesian stocks")
    print("✅ Data: 10-year historical data")
    print("✅ Features: Technical + Fundamental + AI")
    print("✅ Auth: JWT enabled")
    print("✅ Webhooks: Available")
    print("=" * 60)
    print("📚 Documentation: http://127.0.0.1:8000/docs")
    print("🔐 Demo Account:")
    print("   Email: demo@example.com")
    print("   Password: demo123")
    print("=" * 60)
    print("🔗 GitHub: https://github.com/GeraldElroy7/stock-ai-engine")
    print("=" * 60)


if __name__ == "__main__":
    import uvicorn
    
    print("\n🚀 Starting Stock AI Engine API Server...\n")
    
    uvicorn.run(
        "app_b2c:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
