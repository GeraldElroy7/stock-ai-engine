# 📈 Stock AI Engine - Backend API

> **Institutional-Grade Stock Analysis Platform with AI-Powered Recommendations**

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green?logo=fastapi)
![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-red)

---

## ✨ Core Features

### 📊 Data & Analysis
- **120+ Indonesian Stocks** - IDX-30, LQ45, Banking, Mining, Tech, Consumer, etc
- **10-Year Historical Data** - 2,520+ trading days for deep analysis
- **9+ Technical Indicators** - RSI, MACD, EMA, Bollinger Bands, ATR, Stochastic, ADX, OBV, Volume
- **100+ Fundamental Metrics** - P/E, P/B, ROE, Debt-to-Equity, Dividend Yield, Revenue Growth, etc
- **AI-Powered Analysis** - Smart recommendations with confidence scores

### 🎯 Trading Signals
| Score | Signal | Interpretation | Action |
|-------|--------|-----------------|--------|
| ≥ 4.0 | BUY | Strong uptrend | Open LONG |
| -0.5 to 4.0 | HOLD | Unclear trend | Wait |
| -7.0 to -0.5 | SELL | Downtrend | Exit LONG |
| ≤ -7.0 | SHORT | Extreme downtrend | Open SHORT |

### 🔐 B2C Platform
- **JWT Authentication** - Secure user authentication with token-based system
- **User Personalization** - 20+ customizable parameters for user preferences
- **AI Recommendations** - Smart buy/sell advice with action items and risk assessment
- **Webhook Alerts** - Real-time signal notifications for multiple stocks
- **18 RESTful Endpoints** - Comprehensive API with Swagger/ReDoc documentation
- **Production Ready** - Error handling, logging, CORS enabled, institutional standards

### 🎨 Personalization Parameters
- Trading Style (Scalper, Day Trader, Swing Trader, Position Trader, Long-term Investor)
- Risk Level (Conservative, Moderate, Aggressive, Very Aggressive)
- Investment Goal (Capital Preservation, Income, Balanced, Appreciation, Aggressive Growth)
- Capital Size (in IDR - minimum 1 million)
- Sector Preferences (Banking, Tech, Mining, etc)
- Time Horizon (Short-term, Medium-term, Long-term)
- Minimum Confidence Level (0-100%)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- macOS/Linux/WSL (Windows with WSL recommended)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/GeraldElroy7/stock-ai-engine.git
cd stock-ai-engine

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or: venv\Scripts\activate  # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start API server
python -m uvicorn app_b2c:app --reload --port 8000
```

**API will be available at:**
- **Swagger UI (Interactive):** http://127.0.0.1:8000/docs
- **ReDoc (Documentation):** http://127.0.0.1:8000/redoc
- **Health Check:** http://127.0.0.1:8000/health

### Demo Account
```
Email:    demo@example.com
Password: demo123
```

---

## 📁 Project Structure

```
stock-ai-engine/
├── api/
│   ├── auth.py                  # JWT authentication system
│   ├── b2c_endpoints.py         # B2C platform API routes
│   └── __init__.py
├── engine/
│   ├── decision.py              # Trading signal generation
│   ├── ai_agent.py              # AI analysis agent
│   ├── ai_summary.py            # AI recommendation summarizer
│   └── __init__.py
├── data/
│   ├── fetcher.py               # yfinance data fetcher
│   ├── fundamentals.py          # Fundamental data processing
│   ├── enhanced_fundamentals.py # Enhanced fundamental analysis
│   └── __init__.py
├── indicators/
│   ├── technical.py             # Technical indicator calculations
│   └── __init__.py
├── backtest/
│   ├── simple_backtest.py       # Backtesting engine
│   ├── report.py                # Performance report generation
│   └── __init__.py
├── scripts/
│   ├── run_backtest.py          # Backtest CLI tool
│   └── __init__.py
├── config.py                    # Configuration & thresholds
├── main.py                      # Legacy API (backward compatible)
├── app_b2c.py                   # Main B2C API application
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI 0.109+ |
| Web Server | Uvicorn |
| Authentication | JWT (python-jose) |
| Password Hashing | Passlib + bcrypt |
| Data Fetching | yfinance |
| Data Processing | Pandas, NumPy |
| Database | In-memory (Demo), JSON files |
| Validation | Pydantic |

---

## 📊 API Endpoints

### Authentication (V2)
```
POST   /api/v2/auth/register     → Register new user
POST   /api/v2/auth/login        → Login with email/password
POST   /api/v2/auth/logout       → Logout and invalidate token
POST   /api/v2/auth/refresh      → Refresh access token
GET    /api/v2/auth/me           → Get current user info (requires auth)
```

### Stock Analysis (V2)
```
POST   /api/v2/stock/info        → Get comprehensive stock analysis
GET    /api/v2/stocks/list       → Get all supported stocks
GET    /api/v2/stocks/search     → Search stocks by ticker/name
GET    /api/v2/stocks/sector     → Get stocks by sector
GET    /api/v2/user/parameters   → Get available user parameters
```

### Webhooks (V2)
```
POST   /api/v2/webhook/register  → Register webhook for alerts
GET    /api/v2/webhook/list      → List user's webhooks (requires auth)
DELETE /api/v2/webhook/:id       → Delete webhook (requires auth)
```

### Legacy Endpoints (V1)
```
GET    /signal/{ticker}          → Get signal for stock (deprecated)
POST   /backtest                 → Run backtest (deprecated)
GET    /portfolio                → Portfolio signals (deprecated)
```

---

## 🔐 Authentication Flow

### 1. Register User
```bash
curl -X POST http://127.0.0.1:8000/api/v2/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password",
    "full_name": "Your Name"
  }'
```

### 2. Login
```bash
curl -X POST http://127.0.0.1:8000/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password"
  }'
# Returns: { "access_token": "...", "refresh_token": "...", ... }
```

### 3. Use Token in Requests
```bash
curl -X POST http://127.0.0.1:8000/api/v2/stock/info \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "BBCA",
    "trading_style": "swing_trader",
    "risk_level": "moderate"
  }'
```

---

## 📈 Stock Analysis Example

### Request
```json
POST /api/v2/stock/info

{
  "ticker": "BBCA",
  "trading_style": "swing_trader",
  "risk_level": "moderate",
  "capital_size": 100000000,
  "investment_goal": "balanced_growth"
}
```

### Response
```json
{
  "ticker": "BBCA",
  "company_info": {
    "name": "Bank Central Asia Tbk",
    "sector": "Banking"
  },
  "current_price": 10000,
  "price_change": 2.5,
  "price_change_pct": 2.5,
  "technical_analysis": {
    "signal": "BUY",
    "score": 6.5,
    "confidence": 78.5,
    "indicators": {
      "rsi": 45.2,
      "macd": "positive",
      "ema": "uptrend"
    }
  },
  "fundamental_analysis": {
    "score": 72.5,
    "rating": "GOOD",
    "pe_ratio": 15.2,
    "pb_ratio": 3.5,
    "roe": 18.5
  },
  "ai_recommendation": {
    "summary": "✅ STRONG BUY signal. Technical indicators show positive momentum with solid fundamentals.",
    "action_items": [
      "Consider buying at current price",
      "Set stop loss at 9,500",
      "Target price: 11,000 (10% gain)"
    ]
  },
  "risk_assessment": {
    "risk_score": 35,
    "volatility": "moderate",
    "recommendation": "Suitable for swing traders"
  }
}
```

---

## 🧪 Testing

### Unit Tests
```bash
pytest tests/ -v
```

### API Testing
```bash
# Test with demo account
python test_b2c_api.py

# Test signals
python test_signals.py

# Test specific stock
curl http://127.0.0.1:8000/signal/BBCA
```

### Backtesting
```bash
# Backtest all stocks
python scripts/run_backtest.py --all

# Backtest specific stock
python scripts/run_backtest.py --ticker BBCA

# Backtest and save results
python scripts/run_backtest.py --ticker BBCA --save
```

---

## 📊 Configuration

Edit `config.py` to customize:

```python
SIGNAL_CONFIG = {
    "BUY_THRESHOLD": 4.0,        # Buy signal threshold
    "SELL_THRESHOLD": -0.5,      # Sell signal threshold
    "SHORT_THRESHOLD": -7.0,     # Short signal threshold
}

DATA_CONFIG = {
    "LOOKBACK_PERIOD": "10y",    # Historical data period
    "TIMEZONE": "Asia/Jakarta",
    "MARKET": "Indonesia (IDX)"
}
```

---

## 🔄 Related Repositories

- **Frontend:** https://github.com/GeraldElroy7/stock-ai-frontend
- **Deploy with:** Docker, AWS, GCP, Heroku

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [PANDUAN_LENGKAP_MACOS.md](PANDUAN_LENGKAP_MACOS.md) | Complete macOS setup guide |
| [QUICK_CHECKLIST.md](QUICK_CHECKLIST.md) | 2-minute quick start |
| [SETUP_FRONTEND.md](SETUP_FRONTEND.md) | Frontend setup instructions |
| [B2C_UPDATE.md](B2C_UPDATE.md) | B2C platform features |
| [FRONTEND_SETUP.md](FRONTEND_SETUP.md) | Frontend repository guide |
| [QUICK_START.md](QUICK_START.md) | Original quick start guide |

---

## 🐛 Troubleshooting

### Port 8000 Already in Use
```bash
lsof -ti:8000 | xargs kill -9
python -m uvicorn app_b2c:app --reload --port 8000
```

### Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### yfinance Data Not Fetching
```bash
# Update yfinance
pip install --upgrade yfinance

# Check internet connection
curl -I https://query1.finance.yahoo.com
```

---

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Open Pull Request

---

## 📄 License

All rights reserved. For authorized use only.

---

## 👤 Author

**Gerald Elroy** ([@GeraldElroy7](https://github.com/GeraldElroy7))

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/GeraldElroy7/stock-ai-engine/issues)
- **Documentation:** [Complete Setup Guide](PANDUAN_LENGKAP_MACOS.md)
- **API Docs:** http://127.0.0.1:8000/docs (when backend running)

---

**Version:** 2.0.0 | **Updated:** January 3, 2026 | **Status:** ✅ Production Ready
