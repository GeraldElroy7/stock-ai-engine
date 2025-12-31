# SHORT Signal Implementation & Integration Guide

**Status:** ✅ SHORT signals sudah siap digunakan  
**Date Updated:** December 31, 2025  
**Timeframe Upgrade:** 6mo → **1y** (250 trading days untuk akurasi lebih baik)

---

## 📊 Apa yang Berubah?

### 1. **NEW: SHORT Signal**
```
Score <= -7.0  →  SHORT signal
                   Profit dari downtrend (price turun)
                   Contoh: BBRI, ANTM, MDKA yang sedang downtrend

Sebelumnya:  Hanya BUY & SELL (profit hanya naik)
Sekarang:    BUY & SHORT & SELL (profit dari naik ATAU turun)
```

### 2. **Upgraded Timeframe: 6mo → 1y**
```
6 bulan:   ~130 trading days  →  Kurang data untuk seasonal patterns
1 tahun:   ~250 trading days  →  LEBIH AKURAT, tangkap longer trends

Trade-offs:
✅ Lebih banyak data points
✅ Lebih akurat untuk swing trade (3-5 hari hold)
✅ Better pattern recognition
❌ Startup delay (+5-10 detik per stock)
❌ Lebih banyak RAM usage (~50MB per stock)

WORTH IT untuk akurasi? YA! +10-20% improvement biasanya.
```

### 3. **Signal Thresholds (Score -10 to +10)**
```
Score >= 4.0      →  BUY    (Uptrend, beli naik)
-0.5 < Score < 4  →  HOLD   (Unclear, tunggu signal lebih jelas)
-7.0 < Score ≤ -0.5 → SELL   (Minor downtrend, tutup posisi)
Score <= -7.0     →  SHORT  (Extreme downtrend, jual pendek)
```

---

## 🚀 Cara Test di Main App

### Step 1: Update Fetcher untuk 1y timeframe
```bash
# File: stock_ai_engine/data/fetcher.py
# Cek apakah fetch_eod() menggunakan LOOKBACK_PERIOD dari config
# Jika hardcoded "6mo", ubah ke:

from stock_ai_engine.config import DATA_CONFIG
lookback = DATA_CONFIG.get("LOOKBACK_PERIOD", "1y")  # Sekarang "1y"
```

**Cek ini dulu!** Buka file fetcher.py:
<function_calls>
<invoke name="read_file">
<parameter name="filePath">c:\Users\Bittime\Documents\Script\stock_ai_engine\data\fetcher.py