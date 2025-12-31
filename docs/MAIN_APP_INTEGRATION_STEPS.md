# Integration Steps: Menggabungkan SHORT Signals ke Main App

**Updated:** December 31, 2025  
**Estimated Time:** 2-3 hours untuk full integration  
**Difficulty:** Medium (mostly copy-paste + testing)

---

## 🎯 Goal

Integrate SHORT signal engine dengan app utama Anda sehingga:
- ✅ Real-time signals (BUY, SELL, HOLD, SHORT)
- ✅ Works dengan existing UI/database
- ✅ Automatic daily/hourly updates
- ✅ Alerts untuk HIGH conviction trades

---

## 📍 Step 1: Backup Your Current App

```bash
# Backup sebelum merubah apapun
cd c:\Users\Bittime\Documents\Script
cp -r [your-main-app-folder] [your-main-app-folder].backup
```

---

## 📍 Step 2: Copy Engine Files ke Main App

```bash
# Struktur folder yang diperlukan:
your-main-app/
├── signal_engine/              # ← New folder
│   ├── config.py              # ← Copy dari stock_ai_engine/config.py
│   ├── data/
│   │   └── fetcher.py         # ← Copy dari stock_ai_engine/data/fetcher.py
│   ├── indicators/
│   │   └── technical.py       # ← Copy dari stock_ai_engine/indicators/technical.py
│   ├── engine/
│   │   └── decision.py        # ← Copy dari stock_ai_engine/engine/decision.py
│   └── __init__.py
├── your-existing-app.py       # ← Your main app
└── requirements.txt           # ← Add yfinance, pandas, numpy
```

**Copy commands:**
```bash
mkdir your-main-app/signal_engine
cp stock_ai_engine/config.py your-main-app/signal_engine/
cp -r stock_ai_engine/data your-main-app/signal_engine/
cp -r stock_ai_engine/indicators your-main-app/signal_engine/
cp -r stock_ai_engine/engine your-main-app/signal_engine/
cp stock_ai_engine/__init__.py your-main-app/signal_engine/
```

---

## 📍 Step 3: Update Main App with Signal Integration

### Option A: FastAPI Integration (Recommended)
```python
# your-main-app/app.py
from fastapi import FastAPI
from signal_engine.data.fetcher import fetch_eod
from signal_engine.indicators.technical import add_indicators
from signal_engine.engine.decision import decision_engine

app = FastAPI()

@app.get("/api/signal/{ticker}")
async def get_signal(ticker: str):
    """Get current trading signal"""
    try:
        df = fetch_eod(ticker)
        if df is None or df.empty:
            return {"error": f"No data for {ticker}"}
        
        df = add_indicators(df)
        signal = decision_engine(df)
        
        return {
            "ticker": ticker,
            "signal": signal["signal"],
            "score": signal["score"],
            "confidence": signal["confidence"],
            "reasons": signal["reasons"],
            "position_direction": signal["meta"].get("position_direction"),
            "trend": signal["meta"].get("trend_strength"),
        }
    except Exception as e:
        return {"error": str(e)}
```

**Usage:**
```bash
# Start server
uvicorn app:app --reload

# Test in browser/curl
curl http://localhost:8000/api/signal/BBCA
```

### Option B: Batch Processing Integration (For Scheduled Jobs)

```python
# your-main-app/get_all_signals.py
import pandas as pd
from signal_engine.data.fetcher import fetch_eod
from signal_engine.indicators.technical import add_indicators
from signal_engine.engine.decision import decision_engine
from datetime import datetime

def get_portfolio_signals(tickers):
    """Get signals for multiple stocks"""
    results = []
    
    for ticker in tickers:
        try:
            df = fetch_eod(ticker)
            if df is None or df.empty:
                continue
            
            df = add_indicators(df)
            signal = decision_engine(df)
            
            results.append({
                "timestamp": datetime.now().isoformat(),
                "ticker": ticker,
                "signal": signal["signal"],
                "score": signal["score"],
                "confidence": signal["confidence"],
                "position_direction": signal["meta"].get("position_direction"),
                "trend": signal["meta"].get("trend_strength"),
                "close_price": signal["meta"].get("close"),
                "rsi": signal["meta"].get("rsi"),
                "reasons": "|".join(signal["reasons"]),
            })
        except Exception as e:
            print(f"Error for {ticker}: {str(e)}")
    
    return pd.DataFrame(results)

# Usage
if __name__ == "__main__":
    PORTFOLIO = ["BBCA", "BBRI", "ANTM", "UNVR", "MDKA", "TLKM", "ASII"]
    
    signals_df = get_portfolio_signals(PORTFOLIO)
    
    # Save to CSV
    signals_df.to_csv("signals_latest.csv", index=False)
    print(f"✅ Signals saved: {len(signals_df)} stocks")
    
    # Alert on high-conviction signals
    high_conviction = signals_df[signals_df['confidence'] > 0.70]
    for _, row in high_conviction.iterrows():
        if row['signal'] in ['BUY', 'SHORT']:
            print(f"⚡ ALERT: {row['ticker']} → {row['signal']} ({row['confidence']:.0%})")
```

---

## 📍 Step 4: Database Integration (Optional)

### Save signals to SQLite:
```python
# your-main-app/db_manager.py
import sqlite3
import pandas as pd
from datetime import datetime

def save_signals_to_db(signals_df):
    """Save signal results to SQLite"""
    conn = sqlite3.connect("trading_signals.db")
    
    # Add timestamp
    signals_df['saved_at'] = datetime.now().isoformat()
    
    # Save to table
    signals_df.to_sql(
        'signals',
        conn,
        if_exists='append',
        index=False
    )
    
    conn.close()
    print(f"✅ Saved {len(signals_df)} signals to database")

def get_latest_signals():
    """Get latest signals for each ticker"""
    conn = sqlite3.connect("trading_signals.db")
    query = """
    SELECT DISTINCT ON (ticker) *
    FROM signals
    ORDER BY ticker, saved_at DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
```

---

## 📍 Step 5: Scheduling (Daily/Hourly Updates)

### Option A: Windows Task Scheduler
```batch
# Create batch file: run_signals.bat
@echo off
cd c:\path\to\your-main-app
python get_all_signals.py
pause
```

Then schedule via Task Scheduler:
- Run every: 30 minutes / 1 hour / Daily
- Trigger: On startup / On schedule
- Action: `run_signals.bat`

### Option B: Python APScheduler
```python
# your-main-app/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from get_all_signals import get_portfolio_signals
from db_manager import save_signals_to_db
import atexit

scheduler = BackgroundScheduler()

def scheduled_signal_update():
    """Run every 30 minutes"""
    signals = get_portfolio_signals(["BBCA", "BBRI", "ANTM", "UNVR"])
    save_signals_to_db(signals)
    print("✅ Signals updated")

# Start scheduler
scheduler.add_job(func=scheduled_signal_update, trigger="interval", minutes=30)
scheduler.start()

# Shutdown on exit
atexit.register(lambda: scheduler.shutdown())
```

### Option C: Cron Job (Linux/Mac)
```bash
# Add to crontab
# Every 30 minutes
*/30 * * * * cd /path/to/app && python get_all_signals.py >> signals.log 2>&1

# Every hour
0 * * * * cd /path/to/app && python get_all_signals.py >> signals.log 2>&1

# Every morning at 9 AM
0 9 * * * cd /path/to/app && python get_all_signals.py >> signals.log 2>&1
```

---

## 📍 Step 6: Alert System

### Send Telegram Alerts:
```python
# your-main-app/alerts.py
import requests

TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

def send_telegram_alert(message):
    """Send alert via Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

# Usage in get_all_signals.py:
high_conviction = signals_df[
    (signals_df['confidence'] > 0.75) & 
    (signals_df['signal'].isin(['BUY', 'SHORT']))
]

for _, row in high_conviction.iterrows():
    message = f"""
⚡ NEW SIGNAL: {row['ticker']}
Signal: {row['signal']}
Score: {row['score']:.2f}
Confidence: {row['confidence']:.0%}
Trend: {row['trend']}
Price: Rp {row['close_price']:.0f}
"""
    send_telegram_alert(message)
```

---

## 📍 Step 7: Testing Checklist

### Unit Tests:
```python
# your-main-app/test_integration.py
def test_signal_generation():
    """Test signal generation works"""
    from signal_engine.data.fetcher import fetch_eod
    from signal_engine.indicators.technical import add_indicators
    from signal_engine.engine.decision import decision_engine
    
    df = fetch_eod("BBCA")
    assert df is not None
    
    df = add_indicators(df)
    signal = decision_engine(df)
    
    assert signal['signal'] in ['BUY', 'SELL', 'HOLD', 'SHORT']
    assert -10 <= signal['score'] <= 10
    assert 0 <= signal['confidence'] <= 1
    print("✅ Signal generation test passed")

def test_all_portfolio():
    """Test for all stocks"""
    from get_all_signals import get_portfolio_signals
    
    TICKERS = ["BBCA", "BBRI", "ANTM", "UNVR"]
    signals = get_portfolio_signals(TICKERS)
    
    assert len(signals) == len(TICKERS)
    print(f"✅ Portfolio test passed: {len(signals)} stocks")

if __name__ == "__main__":
    test_signal_generation()
    test_all_portfolio()
```

**Run tests:**
```bash
python test_integration.py
```

---

## 📊 Example Main App Usage

```python
# your-main-app/main.py
import pandas as pd
from get_all_signals import get_portfolio_signals
from db_manager import save_signals_to_db
from alerts import send_telegram_alert

def main():
    # Your portfolio
    PORTFOLIO = ["BBCA", "BBRI", "ANTM", "UNVR", "MDKA", "TLKM", "ASII", "PTPP"]
    
    print("=" * 60)
    print("📊 PORTFOLIO SIGNAL UPDATE")
    print("=" * 60)
    
    # Get signals
    signals = get_portfolio_signals(PORTFOLIO)
    
    # Display summary
    print(f"\nTotal stocks: {len(signals)}")
    print(f"BUY signals:  {(signals['signal'] == 'BUY').sum()}")
    print(f"SHORT signals: {(signals['signal'] == 'SHORT').sum()}")
    print(f"SELL signals: {(signals['signal'] == 'SELL').sum()}")
    print(f"HOLD signals: {(signals['signal'] == 'HOLD').sum()}")
    
    # Display high-conviction signals
    print("\n🔥 HIGH CONVICTION SIGNALS (>75% confidence):")
    high = signals[signals['confidence'] > 0.75]
    if len(high) > 0:
        for _, row in high.iterrows():
            print(f"  {row['ticker']}: {row['signal']} ({row['confidence']:.0%}) - {row['trend']}")
    else:
        print("  None")
    
    # Save to database
    save_signals_to_db(signals)
    
    # Send alerts
    for _, row in high.iterrows():
        if row['signal'] in ['BUY', 'SHORT']:
            msg = f"⚡ {row['ticker']}: {row['signal']} @ Rp {row['close_price']:.0f} ({row['confidence']:.0%})"
            send_telegram_alert(msg)
    
    print("\n✅ Update complete")

if __name__ == "__main__":
    main()
```

---

## 📋 Final Checklist

- [ ] Files copied to main app
- [ ] Import paths updated
- [ ] Dependencies installed: `pip install yfinance pandas numpy`
- [ ] Signal engine tested with 4+ stocks
- [ ] Database setup (if using SQLite)
- [ ] Scheduler configured
- [ ] Alerts configured (Telegram/Email)
- [ ] Run full test suite
- [ ] Deployed to production
- [ ] Monitor for 1 week (no changes, just observe)
- [ ] Fine-tune thresholds if needed

---

## 🚀 Deployment Command

```bash
# Final check before going live
cd your-main-app
python test_integration.py  # Should show all ✅
python get_all_signals.py   # Should show signals
python main.py              # Should show summary + save + alert

# If all good:
# Start scheduler in background
python scheduler.py &

# Monitor logs
tail -f signals.log
```

---

## 💪 Support

**Need help?** Check:
- [../docs/SHORT_SIGNAL_IMPLEMENTATION_SUMMARY.md](./SHORT_SIGNAL_IMPLEMENTATION_SUMMARY.md)
- [../docs/INTEGRATION_TESTING_GUIDE.md](./INTEGRATION_TESTING_GUIDE.md)
- [../engine/decision.py](../engine/decision.py) - Signal logic
- [../config.py](../config.py) - Thresholds

**Status:** Ready for production integration ✅
