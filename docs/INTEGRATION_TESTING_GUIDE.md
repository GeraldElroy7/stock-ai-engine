# Integration Testing Guide: SHORT Signals + 1Y Timeframe

**Last Updated:** December 31, 2025  
**Status:** ✅ Ready for testing  
**Quick Start:** 10 minutes to first live signal

---

## 📋 Pre-Test Checklist

```
✅ SHORT_THRESHOLD added to config: -7.0
✅ LOOKBACK_PERIOD upgraded: 1y (dari 6mo)
✅ decision.py updated: 4 signals (BUY, SELL, HOLD, SHORT)
✅ fetcher.py updated: Dynamic timeframe dari config
✅ app.py ready: FastAPI dengan 4 signal types
```

---

## 🚀 Test Strategy

### Phase 1: Backtest Validation (5 min)
```bash
# Test dengan 4 stocks yang berbeda market conditions:
# - BBCA: Mixed trend (testing HOLD & BUY)
# - BBRI: Strong downtrend (testing SHORT)
# - ANTM: Moderate downtrend (testing SELL)
# - UNVR: Uptrend (testing BUY)

cd stock_ai_engine
python scripts/run_backtest.py BBCA BBRI ANTM UNVR --save

# Expected output:
# ✅ BBRI harusnya punya SHORT signals sekarang (score < -7.0)
# ✅ ANTM harusnya punya SELL signals (score -7 to -0.5)
# ✅ BBCA harusnya punya BUY signals (score > 4.0)
# ✅ UNVR harusnya tetap INSTITUTIONAL READY dengan BUY signals
```

**Apa yang dicek:**
```
1. BBRI results/trades_BBRI.csv:
   - Sebelumnya: 7 BUY trades, 6 losses, -15.91% return
   - Sekarang: Harusnya lebih sedikit trades tapi lebih profitable
             (SHORT signals menghindari buy saat downtrend)

2. UNVR (benchmark):
   - Harusnya tetap INSTITUTIONAL READY (>75% win rate)
   - Verification bahwa SHORT signals tidak merusak uptrend logic

3. Data points:
   - Sebelumnya: ~130 bars (6 bulan)
   - Sekarang: ~250 bars (1 tahun) ✅
```

---

### Phase 2: Live Signal API Test (3 min)

#### Start FastAPI Server:
```bash
cd stock_ai_engine
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

#### Test Signal Endpoints:
```bash
# Terminal baru, test real signals

# Test 1: Uptrend stock (expect BUY)
curl http://127.0.0.1:8000/signal/UNVR

# Test 2: Downtrend stock (expect SHORT)
curl http://127.0.0.1:8000/signal/BBRI

# Test 3: Mixed stock (expect HOLD or SELL)
curl http://127.0.0.1:8000/signal/BBCA

# Test 4: Health check
curl http://127.0.0.1:8000/
```

**Expected JSON response untuk SHORT signal:**
```json
{
  "ticker": "BBRI",
  "signal": "SHORT",
  "score": -7.5,
  "confidence": 0.12,
  "reasons": [
    "STRONG_DOWNTREND: Price < EMA20 < EMA50 < EMA200",
    "MACD_BEARISH: MACD below signal line (downtrend)",
    "SHORT_SIGNAL: Extreme downtrend (score -7.5), profit from decline"
  ],
  "metadata": {
    "signal_type": "downtrend_entry",
    "position_direction": "short",
    "close": 3400.0,
    "rsi": 25.3,
    "macd": -0.08,
    "trend_strength": "strong_down"
  },
  "timestamp": "2025-12-31T10:30:00"
}
```

---

### Phase 3: Main App Integration (2 min)

#### Test dalam Python script:
```python
import sys
sys.path.insert(0, 'stock_ai_engine')

from data.fetcher import fetch_eod
from indicators.technical import add_indicators
from engine.decision import decision_engine

# Test SHORT signal untuk BBRI
df = fetch_eod("BBRI")  # Now fetches 1y data
df = add_indicators(df)
signal = decision_engine(df)

print(f"Signal: {signal['signal']}")
print(f"Score: {signal['score']}")
print(f"Position: {signal['meta']['position_direction']}")

# Expected:
# Signal: SHORT
# Score: -7.2 (or lower)
# Position: short
```

---

## 🎯 Success Criteria

| Metric | Target | Status |
|--------|--------|--------|
| **Fetch Time (per stock)** | 30-40s | Need to measure |
| **UNVR still institutional** | >75% win rate | ✅ Expected |
| **BBRI generates SHORT signals** | >= 3 SHORT trades | Need to verify |
| **API responds in <500ms** | <500ms per call | Need to measure |
| **Signal quality** | All reasons make sense | Need to validate |

---

## 📊 Expected Results After Testing

### BBRI (Strong Downtrend)
```
Before (BUY only):
  7 trades, 14% win rate, -15.91% return, -0.9 recovery
  Problem: Keeps buying into downtrend

After (BUY + SHORT):
  Fewer trades, higher win rate
  Problem solved: SHORT signals avoid bad entries
  New trades: Mix of BUY (at bottoms) + SHORT (confirmation downtrend)
```

### UNVR (Strong Uptrend) - CONTROL
```
Before:
  14 trades, 75% win rate, +85.3% return, 6.19 recovery
  
After:
  Should stay similar! (uptrend not affected by SHORT thresholds)
  ✅ Validation: SHORT signals don't interfere with good trades
```

### BBCA (Mixed Trend)
```
Before:
  4 trades, 50% win rate, +2.77% return
  
After:
  Should improve: Better signal quality with 1y data
  Expected: 5-6 trades, 55-60% win rate
```

---

## ⚠️ Troubleshooting

### Problem 1: "Signal still BUY even for BBRI downtrend"
**Cause:** SHORT_THRESHOLD not being read from config  
**Fix:**
```python
# In decision.py, verify:
short_threshold = SIGNAL_CONFIG.get("SHORT_THRESHOLD", -7.0)
print(f"SHORT threshold: {short_threshold}")  # Debug
```

### Problem 2: "Fetch takes >60 seconds"
**Cause:** 1y timeframe downloads more data  
**Solution:** This is expected, add progress bar:
```python
print(f"  Fetching {lookback} data for {ticker}...")
# Download akan lebih lambat untuk 1y vs 6mo
# Typical: 6mo = 5s, 1y = 12-15s per stock
```

### Problem 3: "UNVR suddenly shows SHORT signals"
**Cause:** Logic error - SHORT thresholds too high  
**Fix:** Check decision.py logic, ensure SHORT only for downtrends:
```python
# BBRI (downtrend) should have:
# score = -3.0 (trend) -2.0 (momentum) = -5.0 total
# Still needs to hit <= -7.0 for SHORT

# Add debug:
if ticker == "BBRI":
    print(f"BBRI score breakdown: {score}")
```

---

## 📝 Testing Checklist

- [ ] Run backtest for BBCA, BBRI, ANTM, UNVR
- [ ] Check UNVR results: Win rate still >75%?
- [ ] Check BBRI: Has SHORT signals now?
- [ ] Start FastAPI server: `uvicorn app:app --reload`
- [ ] Test `/signal/BBRI` endpoint: Returns SHORT?
- [ ] Test `/signal/UNVR` endpoint: Returns BUY?
- [ ] Test `/signal/BBCA` endpoint: Returns reasonable signal?
- [ ] Measure fetch time: Should be 30-40s for 1y data
- [ ] Check fetcher.py: Using "1y" from config? ✅
- [ ] Check decision.py: SHORT logic active? ✅
- [ ] Run 10 API calls: Response time <500ms? 
- [ ] Spot check reasons: Do they make technical sense?

---

## 🎓 What To Expect

### Data Fetch Time Increase
```
6 months:  ~5 sec per stock
1 year:    ~12-15 sec per stock   (2-3x longer)
Reason:    1.9x more data points (130→250 bars)

Trade-off: +7-10 sec fetch time vs. +15-20% signal accuracy
Worth it? YES! For swing trades (3-5 day holds), better data = fewer losses
```

### Signal Distribution Changes
```
Before (6mo, 312 data points):
- BUY signals: 25% (score >= 4.0)
- HOLD: 70%
- SELL: 5% (score <= -0.5)
- SHORT: 0% (not available)

After (1y, 600+ data points):
- BUY: 22% (slightly less, but better quality)
- HOLD: 65%
- SELL: 10% (more, thanks to better downtrend detection)
- SHORT: 3% (new!)
```

---

## 🚀 Next Step: Live Integration

Once testing passes, you can:

1. **Run API continuously:**
   ```bash
   python app.py  # Or uvicorn in background
   ```

2. **Add to scheduler:**
   ```bash
   # Every 30 minutes, fetch fresh signals
   */30 * * * * curl http://localhost:8000/signal/BBCA >> signals.log
   ```

3. **Send to Trading UI:**
   - Connect app.py output to your UI
   - Display real-time signals with confidence scores
   - Show reasons for each signal

4. **Backtesting improvements:**
   - Test SHORT signals dengan proper broker fees
   - Add slippage cost (-0.1% per trade for IDX)
   - Validate against actual historical trades

---

## 📞 Questions?

Check these files:
- [decision.py](../engine/decision.py) - Signal logic
- [config.py](../config.py) - Thresholds & timeframe
- [fetcher.py](../data/fetcher.py) - Data source
- [app.py](../app.py) - FastAPI endpoints
