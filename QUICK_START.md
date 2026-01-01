# Quick Start Guide - Stock AI Engine v2.0

## ✅ Setup Complete - B2C Platform Ready!

**Version:** 2.0.0 | **Updated:** January 1, 2026

---

## 🚀 Start B2C API Server (RECOMMENDED)

### 1. Verify Installation:
```bash
cd ~/stock-ai-engine
python3 --version
python3 -c "import pandas, numpy, yfinance, fastapi; print('✅ All dependencies OK!')"
```

### 2. Start the B2C API Server:
```bash
cd ~/stock-ai-engine
python3 -m uvicorn app_b2c:app --reload --port 8000
```

**🌐 Access API**:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- API Base: http://127.0.0.1:8000

**🔐 Demo Account (Ready to Use)**:
- Email: `demo@example.com`
- Password: `demo123`

### 3. Test the API:
```bash
cd ~/stock-ai-engine
python3 test_b2c_api.py
```
This tests:
- ✅ User login with demo account
- ✅ Stock list (120+ stocks)
- ✅ Comprehensive stock info (BBCA example)
- ✅ Webhook registration
- ✅ All API endpoints

---

## 📖 How to Use

### Step 1: Open Swagger UI
Visit: http://127.0.0.1:8000/docs

### Step 2: Login
1. Expand: `POST /api/v2/auth/login`
2. Click "Try it out"
3. Use demo credentials:
```json
{
  "email": "demo@example.com",
  "password": "demo123"
}
```
4. Copy the `access_token` from response

### Step 3: Authorize
1. Click 🔒 "Authorize" button (top right)
2. Paste token: `Bearer {your_access_token}`
3. Click "Authorize" then "Close"

### Step 4: Get Stock Info
1. Expand: `POST /api/v2/stock/info`
2. Try with BBCA:
```json
{
  "ticker": "BBCA",
  "trading_style": "swing_trader",
  "risk_level": "moderate",
  "capital_size": 100000000,
  "investment_goal": "balanced"
}
```
3. Get comprehensive analysis!

---

## 🔄 Alternative: Legacy API Server

For backward compatibility:
```bash
cd ~/stock-ai-engine
python3 -m uvicorn main:app --reload
```
→ Visit: http://localhost:8000/docs

---

## 🧪 Development Tools

### Open in VS Code:
```bash
code ~/stock-ai-engine
```

### Run Unit Tests:
```bash
cd ~/stock-ai-engine
python3 -m pytest tests/ -v
```

### View All Stocks:
```bash
python3 -c "from config import SUPPORTED_STOCKS; print(f'Total: {len(SUPPORTED_STOCKS)} stocks'); [print(f'{k}: {v}') for k,v in list(SUPPORTED_STOCKS.items())[:5]]"
```

---

## 📚 Documentation

- **[B2C Platform Guide](B2C_UPDATE.md)** - Complete B2C features
- **[Implementation Summary](IMPLEMENTATION_COMPLETE.md)** - What was built
- **[Session 3 Summary](SESSION_3_SUMMARY.md)** - Latest updates
- **[Quick Reference](QUICK_REFERENCE.md)** - API quick reference
- **[Project Status](PROJECT_STATUS.md)** - Detailed status

---

## 🛠️ Useful Commands

### Package Management:
```bash
# Install new package
python3 -m pip install <package-name>

# Update requirements
python3 -m pip freeze > requirements.txt

# View installed packages
python3 -m pip list
```

### Python Environment:
```bash
# Check Python version
python3 --version

# Activate virtual environment (if using)
source venv/bin/activate

# Deactivate
deactivate
```

### Git Operations:
```bash
# Check status
git status

# Commit changes
git add .
git commit -m "Your message"

# Push to GitHub
git push origin main
```

---

## 🐛 Troubleshooting

### Issue: Python version shows 3.9
**Solution**: Run `exec zsh` to reload shell config

### Issue: Missing dependencies
**Solution**: 
```bash
python3 -m pip install -r requirements.txt
```

### Issue: Port 8000 already in use
**Solution**: Use different port:
```bash
python3 -m uvicorn app_b2c:app --reload --port 8001
```

### Issue: Authentication not working
**Solution**: Make sure to:
1. Login first to get token
2. Click "Authorize" button in Swagger
3. Paste token with "Bearer " prefix

---

## 🎯 What You Get

### Technical Analysis:
- 9+ indicators (EMA, RSI, MACD, Bollinger, ATR, Volume)
- Signal: BUY, SELL, HOLD, SHORT
- Confidence score: 0-100%

### Fundamental Analysis:
- 100+ financial metrics
- Fundamental score: 0-100
- Rating: EXCELLENT, GOOD, FAIR, WEAK, POOR

### AI Recommendations:
- Buy/Sell advice with reasoning
- Entry/exit prices
- Position sizing
- Action items

### Personalization:
- Risk assessment
- Sector match analysis
- Custom insights based on your profile

---

**Project:** stock-ai-engine  
**Status:** ✅ Production Ready (B2C Platform v2.0)  
**Python:** 3.11.14  
**API:** FastAPI + JWT Authentication  
**Stocks:** 120+ Indonesian Stocks  
**Data:** 10 Years Historical Data
