# 📈 Stock AI Engine

Institutional-grade stock trading signal engine with SHORT signal support and 1-year lookback data.

## 🎯 Features

✅ **4 Signal Types**: BUY, SELL, HOLD, SHORT  
✅ **Technical Indicators**: EMA, RSI, MACD, Bollinger Bands, ATR, Volume  
✅ **1-Year Timeframe**: 250 trading days for accurate pattern recognition  
✅ **Backtesting**: Complete with metrics (Sharpe ratio, recovery factor, win rate)  
✅ **REST API**: FastAPI with Swagger documentation  
✅ **Real-time Signals**: Live market data via yfinance  
✅ **Production Ready**: Error handling, logging, institutional standards  

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start API Server
```bash
python -m uvicorn main:app --reload
# API running on http://127.0.0.1:8000
# Docs: http://127.0.0.1:8000/docs
```

### 3. Test Live Signals
```bash
python test_signals.py
# Returns current signals for BBCA, BBRI, ANTM, UNVR
```

### 4. Run Backtest
```bash
cd scripts
python run_backtest.py BBCA BBRI ANTM --save
# Results saved to ../results/trades_*.csv
```

## 📊 API Endpoints

### Get Signal
```bash
GET /signal/{ticker}
# Example: GET /signal/BBCA
# Returns: {signal, score, confidence, reasons, metadata}
```

### Portfolio Status
```bash
GET /portfolio
# Returns current portfolio monitoring status
```

### Backtest
```bash
POST /backtest
{
  "symbols": ["BBCA", "BBRI", "ANTM"],
  "lookback_period": "1y"
}
```

### Health Check
```bash
GET /
# Returns: {status, service, version}
```

## 📈 Signal System

| Score | Signal | Meaning | Action |
|-------|--------|---------|--------|
| ≥ 4.0 | BUY | Strong uptrend | Open LONG |
| -0.5 to 4.0 | HOLD | Unclear trend | Wait |
| -7.0 to -0.5 | SELL | Downtrend | Exit LONG |
| ≤ -7.0 | SHORT | Extreme downtrend | Open SHORT |

## 🧪 Testing

### Unit Tests
```bash
pytest tests/ -v
```

### Live Signal Test
```bash
python test_signals.py
```

### Backtest Validation
```bash
python scripts/run_backtest.py --all --save
```

## 📁 Project Structure

```
stock_ai_engine/
├── main.py                 # FastAPI server
├── config.py              # Configuration & thresholds
├── engine/
│   └── decision.py        # Signal generation logic
├── data/
│   └── fetcher.py         # yfinance data fetching
├── indicators/
│   └── technical.py       # Technical indicators
├── backtest/
│   ├── simple_backtest.py
│   └── report.py          # Performance metrics
├── scripts/
│   └── run_backtest.py    # Backtest CLI
├── results/               # Backtest outputs (CSV)
├── docs/                  # 16 comprehensive guides
├── auto_sync.ps1          # GitHub auto-sync script
└── requirements.txt       # Dependencies
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
SIGNAL_CONFIG = {
    "BUY_THRESHOLD": 4.0,      # BUY signal threshold
    "SELL_THRESHOLD": -0.5,    # SELL signal threshold
    "SHORT_THRESHOLD": -7.0,   # SHORT signal threshold
}

DATA_CONFIG = {
    "LOOKBACK_PERIOD": "1y",   # 1 year of data
    "TIMEZONE": "Asia/Jakarta",
    "MARKET": "Indonesia (IDX)"
}
```

## 🔄 GitHub Auto-Sync

Automatically push changes to GitHub every 5 minutes:

```powershell
# PowerShell
powershell -File auto_sync.ps1

# Batch (Windows)
auto_sync.bat
```

## 📚 Documentation

- `docs/START_HERE.md` - Quick overview
- `docs/QUICK_REFERENCE.md` - Quick lookup
- `docs/MAIN_APP_INTEGRATION_STEPS.md` - Integration guide
- `docs/INTEGRATION_TESTING_GUIDE.md` - Testing procedures
- `docs/VISUAL_SUMMARY.md` - Diagrams & visuals

## 🧮 Institutional Metrics

The system calculates:
- ✅ Win Rate (%)
- ✅ Sharpe Ratio
- ✅ Recovery Factor
- ✅ Max Drawdown
- ✅ Profit Factor
- ✅ Expectancy

**Institutional Standards**:
- Min win rate: 55%
- Min recovery: 2.0
- Min Sharpe: 0.5
- Max consecutive losses: 5

## 🌐 Indonesian Market (IDX)

- **Market**: Indonesia Stock Exchange (IHSG)
- **Timezone**: Asia/Jakarta (WIB)
- **Trading Hours**: 09:00 - 16:00 WIB
- **Stocks Supported**: 30 major IDX stocks
- **Data Source**: yfinance (.JK suffix)

## 🛠️ Development

### Add New Indicator
1. Edit `indicators/technical.py`
2. Add to `add_indicators()` function
3. Use in `engine/decision.py`

### Modify Thresholds
1. Edit `config.py`
2. Run backtest to validate
3. Commit and push

### Deploy to Production
1. Set `--reload` to False in uvicorn
2. Add monitoring/logging
3. Deploy to cloud (AWS/GCP/Heroku)

## 📞 Support

## 🔎 Fundamentals Data & `results/` folder
- Fundamental data is loaded from JSON files placed under `data/fund_data/{SYMBOL}.json` (you will provide these). If a file is missing, the system returns a small mocked record so flows can run.
- Example fundamentals file (`data/fund_data/BBCA.json`):
```json
{
  "symbol": "BBCA",
  "pe_ratio": 7.2,
  "pb_ratio": 1.3,
  "roe_pct": 15.2,
  "revenue_growth_pct": 8.4,
  "market_cap_usd": 12000000000
}
```

`/backtest` and `/analysis` support an optional `save` boolean in the request body. When `save=true` the engine will persist:
- trades CSV: `results/trades_{SYMBOL}_{TIMESTAMP}.csv`
- report JSON: `results/report_{SYMBOL}_{TIMESTAMP}.json`
- analysis summary JSON: `results/analysis_summary_{SYMBOL}_{TIMESTAMP}.json`

Use examples:
```bash
# Backtest with save
curl -X POST http://127.0.0.1:8000/backtest -H "Content-Type: application/json" -d '{"symbols":["BBCA"],"save":true}'

# Analysis with save
curl -X POST http://127.0.0.1:8000/analysis -H "Content-Type: application/json" -d '{"symbols":["BBCA"],"mode":"both","save":true}'
```

#

- **Questions?** Check `docs/START_HERE.md`
- **Integration?** See `docs/MAIN_APP_INTEGRATION_STEPS.md`
- **Testing?** See `docs/INTEGRATION_TESTING_GUIDE.md`

## 📋 Version History

- **v1.0** - Initial release with SHORT signals
  - ✅ 4 signal types (BUY, SELL, HOLD, SHORT)
  - ✅ 1-year timeframe (250 trading days)
  - ✅ 9+ technical indicators
  - ✅ FastAPI REST interface
  - ✅ Institutional-grade backtesting

## 📄 License

All rights reserved. For authorized use only.

## 👤 Author

Gerald Elroy (@GeraldElroy7)

---

**Status**: ✅ Production Ready  
**Last Updated**: December 31, 2025  
**Repository**: https://github.com/GeraldElroy7/stock-ai-engine
