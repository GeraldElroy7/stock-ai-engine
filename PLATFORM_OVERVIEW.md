# 📈 Stock AI Engine - Complete Platform

> **AI-Powered Stock Analysis Platform for Indonesian Market**

[![Backend](https://img.shields.io/badge/Backend-FastAPI-green?logo=fastapi&logoColor=white)](https://github.com/GeraldElroy7/stock-ai-engine)
[![Frontend](https://img.shields.io/badge/Frontend-React-blue?logo=react&logoColor=white)](https://github.com/GeraldElroy7/stock-ai-frontend)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![Node](https://img.shields.io/badge/Node-18+-green?logo=node.js)](https://nodejs.org)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success)](#)

---

## 🎯 What is Stock AI Engine?

Stock AI Engine is a **complete AI-powered stock analysis platform** designed for Indonesian traders and investors. It provides:

- 📊 **Deep Technical Analysis** (9+ indicators)
- 💡 **Smart AI Recommendations** (confidence scores 0-100%)
- 📈 **Fundamental Metrics** (100+ data points)
- 🎯 **Trading Signals** (BUY/SELL/HOLD/SHORT)
- 🔐 **Secure B2C Platform** (JWT authentication)
- 📱 **Modern Web Interface** (React 18)

**120+ Indonesian Stocks | 10-Year Data | Production Ready** ✅

---

## 📂 Project Structure

```
Stock AI Engine (Complete Platform)
│
├── 📦 Backend (Python/FastAPI)
│   └── https://github.com/GeraldElroy7/stock-ai-engine
│       ├── API Server (Port 8000)
│       ├── Trading Signals
│       ├── AI Analysis
│       └── Data Processing
│
└── 🎨 Frontend (React/Vite)
    └── https://github.com/GeraldElroy7/stock-ai-frontend
        ├── Web UI (Port 5174)
        ├── Login/Auth
        ├── Dashboard
        └── Stock Analysis Pages
```

---

## 🚀 Quick Start

### System Architecture
```
┌──────────────────┐
│   Browser        │
│ (localhost:5174) │
└────────┬─────────┘
         │ HTTP
         ↓
┌──────────────────────────────────┐
│  React Frontend (Vite)           │
│  - Landing, Login, Dashboard     │
│  - Stock Analysis, Settings      │
└────────┬────────────────────────┘
         │ API Requests
         ↓
┌──────────────────────────────────┐
│  FastAPI Backend (Port 8000)     │
│  - Authentication (JWT)          │
│  - Stock Analysis                │
│  - Technical Indicators          │
│  - AI Recommendations            │
│  - Data Fetching                 │
└────────┬────────────────────────┘
         │ Data
         ↓
┌──────────────────────────────────┐
│  Data Sources                    │
│  - Yahoo Finance (yfinance)      │
│  - Fundamental Data (JSON)       │
└──────────────────────────────────┘
```

### Setup (5 Minutes)

#### 1️⃣ Backend Setup
```bash
# Terminal 1
git clone https://github.com/GeraldElroy7/stock-ai-engine.git
cd stock-ai-engine
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app_b2c:app --reload --port 8000
```

**✅ Backend running:** http://127.0.0.1:8000

#### 2️⃣ Frontend Setup
```bash
# Terminal 2
git clone https://github.com/GeraldElroy7/stock-ai-frontend.git
cd stock-ai-frontend
npm install
npm run dev
```

**✅ Frontend running:** http://localhost:5174

#### 3️⃣ Login & Test
1. Open http://localhost:5174
2. Click "Sign In"
3. Use demo account:
   - Email: `demo@example.com`
   - Password: `demo123`
4. Start analyzing stocks! 📈

---

## 📚 Repository Links

### Backend Repository
**https://github.com/GeraldElroy7/stock-ai-engine**

| Document | Purpose |
|----------|---------|
| [README.md](https://github.com/GeraldElroy7/stock-ai-engine/blob/main/README.md) | Backend overview & API reference |
| [PANDUAN_LENGKAP_MACOS.md](https://github.com/GeraldElroy7/stock-ai-engine/blob/main/PANDUAN_LENGKAP_MACOS.md) | Complete macOS setup guide |
| [QUICK_CHECKLIST.md](https://github.com/GeraldElroy7/stock-ai-engine/blob/main/QUICK_CHECKLIST.md) | 2-minute quick start |
| [SETUP_FRONTEND.md](https://github.com/GeraldElroy7/stock-ai-engine/blob/main/SETUP_FRONTEND.md) | Frontend setup instructions |
| [FRONTEND_SETUP.md](https://github.com/GeraldElroy7/stock-ai-engine/blob/main/FRONTEND_SETUP.md) | Frontend repository guide |

### Frontend Repository
**https://github.com/GeraldElroy7/stock-ai-frontend**

| Document | Purpose |
|----------|---------|
| [README.md](https://github.com/GeraldElroy7/stock-ai-frontend/blob/main/README.md) | Frontend features & setup |

---

## 🎯 Key Features

### 🔐 Security & Auth
- ✅ JWT-based authentication
- ✅ Secure password hashing (bcrypt)
- ✅ Token refresh mechanism
- ✅ Demo account for testing
- ✅ CORS enabled

### 📊 Stock Analysis
- ✅ **120+ Indonesian Stocks**
  - IDX-30 (top 30 stocks)
  - LQ45 (most liquid)
  - Banking sector (BBCA, BBRI, BMRI, etc)
  - Tech sector (ASII, TLKM, EXCL)
  - Mining (ANTM, BUMI)
  - Consumer (UNVR, HMSP, INDF)
  - Property & Real Estate
  - Transportation & Logistics
  - Media & Telecom

- ✅ **10-Year Historical Data** (2,520 trading days)
- ✅ **9+ Technical Indicators**
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - EMA (Exponential Moving Average)
  - SMA (Simple Moving Average)
  - Bollinger Bands
  - ATR (Average True Range)
  - Stochastic Oscillator
  - ADX (Average Directional Index)
  - OBV (On-Balance Volume)

- ✅ **100+ Fundamental Metrics**
  - Valuation: P/E, P/B, P/S
  - Profitability: ROE, ROA, Net Margin
  - Liquidity: Current Ratio, Quick Ratio
  - Leverage: Debt-to-Equity, Debt Ratio
  - Market: Market Cap, Volume, Float
  - Growth: Revenue Growth, EPS Growth
  - Dividend: Dividend Yield, Payout Ratio

### 🤖 AI Analysis
- ✅ Smart buy/sell recommendations
- ✅ Confidence scores (0-100%)
- ✅ Action items for trading
- ✅ Risk assessment
- ✅ Portfolio suitability analysis

### 🎨 Modern UI/UX
- ✅ React 18 with Vite
- ✅ Responsive design (mobile-first)
- ✅ Light/Dark mode toggle
- ✅ Smooth animations
- ✅ Interactive charts
- ✅ Real-time updates

---

## 💡 Use Cases

### For Traders
- Screen stocks for trading opportunities
- Check technical indicators before entry
- Get AI-powered entry/exit signals
- Monitor risk levels
- Track portfolio performance

### For Investors
- Analyze fundamentals of stocks
- Compare valuation metrics
- Assess long-term growth potential
- Check dividend yields
- Build diversified portfolios

### For Analysts
- Research company fundamentals
- Analyze technical patterns
- Compare industry peers
- Generate trading reports
- Backtest strategies

---

## 📊 Signal System

| Score | Signal | Meaning | Action |
|-------|--------|---------|--------|
| ≥ 4.0 | **BUY** | Strong uptrend | Open LONG position |
| -0.5 to 4.0 | **HOLD** | Unclear trend | Wait for clarity |
| -7.0 to -0.5 | **SELL** | Downtrend | Exit LONG position |
| ≤ -7.0 | **SHORT** | Extreme downtrend | Open SHORT position |

**Confidence Score:** 0-100% (higher = more confident)

---

## 🧪 Testing

### Live Testing with Demo Account
```bash
Email:    demo@example.com
Password: demo123
```

1. Go to http://localhost:5174
2. Click "Sign In"
3. Use demo credentials above
4. Explore dashboard & analysis pages

### API Testing
```bash
# Health check
curl http://127.0.0.1:8000/health

# Login
curl -X POST http://127.0.0.1:8000/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"demo123"}'

# Get all stocks
curl http://127.0.0.1:8000/api/v2/stocks/list

# API documentation
curl http://127.0.0.1:8000/docs
```

---

## 📈 Performance Metrics

| Metric | Value | Status |
|--------|-------|--------|
| **Backend Response Time** | <1 second | ✅ |
| **Frontend Load Time** | <2 seconds | ✅ |
| **Bundle Size (gzip)** | ~150KB | ✅ |
| **Stocks Supported** | 120+ | ✅ |
| **Historical Data** | 10 years | ✅ |
| **Technical Indicators** | 9+ | ✅ |
| **Fundamental Metrics** | 100+ | ✅ |
| **API Endpoints** | 18+ | ✅ |
| **Database** | In-memory + JSON | ✅ |
| **Production Ready** | YES | ✅ |

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Activate venv & restart
source venv/bin/activate
python -m uvicorn app_b2c:app --reload --port 8000
```

### Frontend won't start
```bash
# Kill process on port 5174
lsof -ti:5174 | xargs kill -9

# Restart
npm run dev
```

### Login fails
- Check backend is running (curl http://127.0.0.1:8000/health)
- Verify email: `demo@example.com` (lowercase)
- Verify password: `demo123`
- Check browser console for errors (F12 → Console tab)

### Data not loading
- Check network tab in DevTools (F12 → Network)
- Verify backend API returns data (curl http://127.0.0.1:8000/api/v2/stocks/list)
- Check for CORS errors in console

---

## 📝 Installation Checklist

```
Sebelum Mulai:
□ Python 3.11+ installed
□ Node.js 18+ installed
□ Git installed
□ 2 terminal windows ready

Backend:
□ Clone backend repo
□ Create virtual environment
□ pip install -r requirements.txt
□ Start with: python -m uvicorn app_b2c:app --reload --port 8000
□ Verify: http://127.0.0.1:8000/health

Frontend:
□ Clone frontend repo
□ npm install
□ npm run dev
□ Verify: http://localhost:5174

Test:
□ Login with demo@example.com / demo123
□ Search for stock (BBCA, BBRI, ASII)
□ View analysis & signals
□ Explore dashboard

✅ READY TO USE!
```

---

## 🔗 Quick Links

| Link | Purpose |
|------|---------|
| **Backend Repo** | https://github.com/GeraldElroy7/stock-ai-engine |
| **Frontend Repo** | https://github.com/GeraldElroy7/stock-ai-frontend |
| **API Docs** | http://127.0.0.1:8000/docs |
| **Setup Guide** | [PANDUAN_LENGKAP_MACOS.md](https://github.com/GeraldElroy7/stock-ai-engine/blob/main/PANDUAN_LENGKAP_MACOS.md) |
| **Quick Start** | [QUICK_CHECKLIST.md](https://github.com/GeraldElroy7/stock-ai-engine/blob/main/QUICK_CHECKLIST.md) |

---

## 📄 License

All rights reserved. For authorized use only.

---

## 👤 Author

**Gerald Elroy** ([@GeraldElroy7](https://github.com/GeraldElroy7))

---

## 📞 Support

- **Backend Issues:** [Backend Issues](https://github.com/GeraldElroy7/stock-ai-engine/issues)
- **Frontend Issues:** [Frontend Issues](https://github.com/GeraldElroy7/stock-ai-frontend/issues)
- **Documentation:** [Complete Setup Guide](https://github.com/GeraldElroy7/stock-ai-engine/blob/main/PANDUAN_LENGKAP_MACOS.md)

---

**Version:** 2.0.0 | **Updated:** January 3, 2026 | **Status:** ✅ Production Ready

---

## 🎉 Ready to Get Started?

1. **Clone both repositories**
2. **Follow setup instructions above**
3. **Login with demo account**
4. **Start analyzing stocks!**

**Happy Trading! 📈**
