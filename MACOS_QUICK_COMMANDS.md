# 🚀 Quick Reference - macOS Commands

## Virtual Environment

### Activate (Do this FIRST every time)
```bash
cd /Users/zelda/stock-ai-engine
source venv/bin/activate
# You should see (venv) at the beginning of your terminal
```

### Deactivate (When done)
```bash
deactivate
```

---

## Run the API Server

### Start in foreground (see all messages)
```bash
cd /Users/zelda/stock-ai-engine
source venv/bin/activate
python3 -m uvicorn main:app --reload --port 8000
# Ctrl+C to stop
```

### Start in background (keep working)
```bash
cd /Users/zelda/stock-ai-engine
source venv/bin/activate
python3 -m uvicorn main:app --reload --port 8000 > /tmp/api.log 2>&1 &
```

### Kill background process
```bash
pkill -f "uvicorn main:app"
```

---

## Test Endpoints

### Health Check
```bash
curl http://127.0.0.1:8000/
# Returns: {"status":"operational","service":"Stock AI Engine","version":"1.0.0"}
```

### Get Single Signal
```bash
curl http://127.0.0.1:8000/signal/BBCA
curl http://127.0.0.1:8000/signal/BBRI
curl http://127.0.0.1:8000/signal/ANTM
```

### Run Backtest
```bash
curl -X POST "http://127.0.0.1:8000/backtest" \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["BBCA", "BBRI", "ANTM"], "lookback_period": "1y"}'
```

### View API Documentation (Interactive)
```
Open browser: http://127.0.0.1:8000/docs
```

---

## Run Tests

### Unit Tests
```bash
cd /Users/zelda/stock-ai-engine
source venv/bin/activate
python3 -m pytest tests/ -v
```

### Test Signals (Live Market Data)
```bash
cd /Users/zelda/stock-ai-engine
source venv/bin/activate
python3 test_signals.py
```

### Test API Endpoints
```bash
cd /Users/zelda/stock-ai-engine
source venv/bin/activate
python3 test_api_endpoints.py
```

---

## Run Backtests

### Single Stock
```bash
cd /Users/zelda/stock-ai-engine
source venv/bin/activate
cd scripts
python3 run_backtest.py BBCA
```

### Multiple Stocks
```bash
cd /Users/zelda/stock-ai-engine
source venv/bin/activate
cd scripts
python3 run_backtest.py BBCA BBRI ANTM UNVR
```

### Save Results to CSV
```bash
cd /Users/zelda/stock-ai-engine
source venv/bin/activate
cd scripts
python3 run_backtest.py BBCA BBRI --save
# Check: ../results/trades_*.csv
```

---

## Useful Commands

### Check Python Version
```bash
python3 --version
```

### View Installed Packages
```bash
pip list
```

### Update a Package
```bash
pip install --upgrade pandas
```

### Freeze Current Environment
```bash
pip freeze > requirements.txt
```

### Clear Cache
```bash
rm -rf __pycache__ .pytest_cache
find . -type d -name __pycache__ -exec rm -r {} +
```

---

## Troubleshooting

### "command not found: python3"
```bash
# Install via Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3
```

### "venv not activated"
```bash
# Make sure you're in the right directory
cd /Users/zelda/stock-ai-engine

# Then activate
source venv/bin/activate
```

### "ModuleNotFoundError: No module named 'pandas'"
```bash
# Make sure venv is activated, then reinstall
source venv/bin/activate
pip install -r requirements.txt
```

### "Port 8000 already in use"
```bash
# Check what's using it
lsof -i :8000

# Kill it
pkill -f "uvicorn main:app"

# Or use different port
python3 -m uvicorn main:app --port 8001
```

### "ImportError: cannot import name..."
```bash
# Usually means venv is not activated
source venv/bin/activate
python3 -c "import main"  # Test import
```

---

## File Locations

```
/Users/zelda/stock-ai-engine/
├── main.py                 # API server
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── engine/
│   ├── decision.py       # Signal generation
│   └── ai_agent.py       # AI analysis
├── data/
│   ├── fetcher.py        # Data fetching
│   └── fundamentals.py   # Fundamental data
├── indicators/
│   └── technical.py      # Technical indicators
├── backtest/
│   └── simple_backtest.py # Backtest engine
├── results/              # Backtest results (auto-created)
├── venv/                 # Virtual environment
└── docs/                 # Documentation
```

---

## Key API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/signal/{ticker}` | GET | Get current signal for stock |
| `/portfolio` | GET | Monitor multiple stocks |
| `/backtest` | POST | Run backtest |
| `/docs` | GET | Interactive API documentation |

---

## Next Steps

1. **Explore the codebase**
   ```bash
   open -a "Visual Studio Code" /Users/zelda/stock-ai-engine
   ```

2. **Read documentation**
   - Start with: `docs/MACOS_SETUP_AND_ROADMAP.md`
   - Then: `docs/START_HERE.md`

3. **Run live tests**
   ```bash
   source venv/bin/activate
   python3 test_signals.py
   ```

4. **Plan next feature**
   - Read: `docs/NEXT_STEPS.md`
   - Choose: B2B, B2C, or Hybrid approach

---

**Remember:** Always activate venv before running anything!
```bash
source venv/bin/activate
```

