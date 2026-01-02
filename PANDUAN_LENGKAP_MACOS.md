# 📖 Panduan Lengkap - Stock AI Engine (macOS)

> **Panduan Step-by-Step untuk Menjalankan Website Stock AI Engine**  
> Dibuat: 3 Januari 2026  
> Platform: macOS

---

## 📋 Daftar Isi

1. [Persyaratan](#-persyaratan)
2. [Arsitektur Sistem](#-arsitektur-sistem)
3. [Instalasi Pertama Kali](#-instalasi-pertama-kali)
4. [Menjalankan Website](#-menjalankan-website)
5. [Cara Menggunakan UI](#-cara-menggunakan-ui)
6. [Troubleshooting](#-troubleshooting)
7. [FAQ](#-faq)

---

## ✅ Persyaratan

Sebelum mulai, pastikan sudah terinstall:

- ✅ **Python 3.11+** - Untuk backend API
- ✅ **Node.js 18+** - Untuk frontend React
- ✅ **Git** - Untuk version control

### Cek Versi:

```bash
python3 --version    # Harus >= 3.11
node --version       # Harus >= 18
npm --version        # Otomatis terinstall dengan Node.js
```

---

## 🏗 Arsitektur Sistem

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  Browser (http://localhost:5174)                │
│  ┌──────────────────────────────────────────┐   │
│  │  React Frontend (Vite)                   │   │
│  │  - Login Page                            │   │
│  │  - Dashboard                             │   │
│  │  - Stock Analysis                        │   │
│  └──────────────────────────────────────────┘   │
│                      ↓                           │
│              HTTP Requests                       │
│                      ↓                           │
│  ┌──────────────────────────────────────────┐   │
│  │  FastAPI Backend (http://127.0.0.1:8000) │   │
│  │  - Authentication (JWT)                  │   │
│  │  - Stock Data API                        │   │
│  │  - AI Analysis Engine                    │   │
│  └──────────────────────────────────────────┘   │
│                      ↓                           │
│  ┌──────────────────────────────────────────┐   │
│  │  Data Sources                            │   │
│  │  - Yahoo Finance (yfinance)              │   │
│  │  - Fundamental Data (JSON files)         │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘

2 KOMPONEN UTAMA yang HARUS jalan bersamaan:
1. Backend  (Port 8000) - Python/FastAPI
2. Frontend (Port 5174) - React/Vite
```

---

## 🚀 Instalasi Pertama Kali

### Step 1: Clone Repository

```bash
cd ~
git clone https://github.com/GeraldElroy7/stock-ai-engine.git
cd stock-ai-engine
```

### Step 2: Setup Backend (Python)

```bash
# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**✅ Selesai!** Backend sudah siap.

### Step 3: Setup Frontend (React)

```bash
# Pindah ke folder frontend (di luar folder backend)
cd /Users/zelda/stock-ai-frontend

# Install dependencies
npm install
```

**✅ Selesai!** Frontend sudah siap.

---

## 🎯 Menjalankan Website

### ⚠️ PENTING: Butuh 2 Terminal Terbuka Bersamaan!

```
Terminal 1: Backend (Port 8000)
Terminal 2: Frontend (Port 5174)
```

### Terminal 1: Start Backend 🟢

```bash
# Buka Terminal baru
cd /Users/zelda/stock-ai-engine
source venv/bin/activate
python -m uvicorn app_b2c:app --reload --port 8000
```

**Output yang benar:**

```
============================================================
🚀 Stock AI Engine - B2C Platform
============================================================
✅ Version: 2.0.0
✅ Status: Production Ready
✅ Stocks: 120+ Indonesian stocks
✅ Data: 10-year historical data
✅ Features: Technical + Fundamental + AI
✅ Auth: JWT enabled
✅ Webhooks: Available
============================================================
📚 Documentation: http://127.0.0.1:8000/docs
🔐 Demo Account:
   Email: demo@example.com
   Password: demo123
============================================================

INFO:     Uvicorn running on http://127.0.0.1:8000
```

**✅ Backend JALAN** - Jangan tutup terminal ini!

### Terminal 2: Start Frontend 🔵

```bash
# Buka Terminal BARU (jangan tutup yang pertama!)
cd /Users/zelda/stock-ai-frontend
npm run dev
```

**Output yang benar:**

```
  VITE v7.3.0  ready in 388 ms

  ➜  Local:   http://localhost:5174/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**✅ Frontend JALAN** - Jangan tutup terminal ini!

### ✅ Cek Status Kedua Server

Buka browser:

- **Backend API:** http://127.0.0.1:8000/docs (Harus bisa buka Swagger UI)
- **Frontend UI:** http://localhost:5174 (Harus tampil website)

---

## 💻 Cara Menggunakan UI

### 1. Buka Website

```
Buka browser → http://localhost:5174
```

**Tampilan Landing Page:**
```
┌────────────────────────────────────────────────┐
│  Stock AI Engine          [Sign In] [Sign Up]  │
├────────────────────────────────────────────────┤
│                                                │
│         📈 Stock AI Analysis Platform          │
│                                                │
│   AI-powered stock analysis untuk investor     │
│                                                │
│        [Get Started]  [Learn More]             │
│                                                │
└────────────────────────────────────────────────┘
```

### 2. Klik "Sign In" atau "Get Started"

**Tampilan Login Page:**
```
┌────────────────────────────────────────────────┐
│              Stock AI Engine Logo               │
├────────────────────────────────────────────────┤
│                                                │
│              Welcome Back!                      │
│         Sign in to your account                 │
│                                                │
│  Email:    [                          ]         │
│  Password: [                          ]         │
│                                                │
│           [Sign In] button                      │
│                                                │
│       ┌──────────────────────────┐              │
│       │  Try Demo Account        │              │
│       │  Quick login for testing │              │
│       └──────────────────────────┘              │
│                                                │
│  Don't have account? [Sign Up]                  │
│                                                │
└────────────────────────────────────────────────┘
```

### 3. Login dengan Demo Account

**Cara 1: Klik "Try Demo Account"** (Otomatis terisi)

**Cara 2: Input Manual:**
- **Email:** `demo@example.com`
- **Password:** `demo123`

Kemudian klik **"Sign In"**

### 4. Dashboard (Setelah Login)

**Tampilan Dashboard:**
```
┌────────────────────────────────────────────────┐
│  Stock AI Engine    [Search] 🔍  [Profile] 👤  │
├────────────────────────────────────────────────┤
│                                                │
│  📊 Dashboard                                   │
│  Welcome, Demo User!                            │
│                                                │
│  Featured Stocks:                               │
│  ┌──────────┬──────────┬──────────┐            │
│  │ BBCA     │ BBRI     │ ASII     │            │
│  │ Rp 10,000│ Rp 5,500 │ Rp 6,200 │            │
│  │ ↑ +2.5%  │ ↑ +1.8%  │ ↓ -0.5%  │            │
│  │ BUY 78   │ BUY 72   │ HOLD 55  │            │
│  └──────────┴──────────┴──────────┘            │
│                                                │
│  Search Stocks:                                 │
│  [Search by ticker or name...]                  │
│                                                │
└────────────────────────────────────────────────┘
```

### 5. Analisa Saham

**Klik salah satu saham (misal: BBCA):**

```
┌────────────────────────────────────────────────┐
│  ← Back to Dashboard                            │
├────────────────────────────────────────────────┤
│                                                │
│  BBCA - Bank Central Asia Tbk                  │
│  Current Price: Rp 10,000  (+2.5%)              │
│                                                │
│  📈 Price Chart (Last 1 Year)                   │
│  [Line chart showing price movement]            │
│                                                │
│  📊 Technical Analysis                          │
│  Signal: BUY                                    │
│  Confidence: 78.5%                              │
│  Score: 6.5                                     │
│                                                │
│  Technical Indicators:                          │
│  • RSI: 45.2 (Neutral)                          │
│  • MACD: Positive crossover                     │
│  • EMA: Uptrend                                 │
│                                                │
│  💡 Fundamental Analysis                        │
│  • P/E Ratio: 15.2                              │
│  • P/B Ratio: 3.5                               │
│  • ROE: 18.5%                                   │
│  • Market Cap: $50.2B                           │
│                                                │
│  🤖 AI Recommendation                           │
│  "Strong BUY signal detected. Technical        │
│   indicators show positive momentum with       │
│   solid fundamentals. Good entry point for     │
│   swing traders."                               │
│                                                │
│  Action Items:                                  │
│  ✓ Consider buying at current price            │
│  ✓ Set stop loss at Rp 9,500                   │
│  ✓ Target price: Rp 11,000 (10% gain)          │
│                                                │
└────────────────────────────────────────────────┘
```

---

## 🔧 Troubleshooting

### ❌ Problem: "Failed to connect" saat login

**Penyebab:** Backend tidak jalan

**Solusi:**

```bash
# Cek apakah backend jalan
curl http://127.0.0.1:8000/health

# Jika error, jalankan backend:
cd /Users/zelda/stock-ai-engine
source venv/bin/activate
python -m uvicorn app_b2c:app --reload --port 8000
```

### ❌ Problem: "Port 5174 already in use"

**Penyebab:** Frontend sudah jalan sebelumnya

**Solusi 1:** Gunakan port yang disediakan (misal 5175)

**Solusi 2:** Kill process yang pakai port 5174:

```bash
lsof -ti:5174 | xargs kill -9
npm run dev
```

### ❌ Problem: "Invalid email or password"

**Penyebab:** Typo atau backend belum sync

**Solusi:**

1. Pastikan email: `demo@example.com` (EXACT, lowercase)
2. Pastikan password: `demo123` (EXACT, no spaces)
3. Restart backend jika perlu

### ❌ Problem: "Cannot read package.json"

**Penyebab:** Salah folder

**Solusi:** Pastikan di folder frontend:

```bash
pwd  # Harus show /Users/zelda/stock-ai-frontend
cd /Users/zelda/stock-ai-frontend
npm run dev
```

### ❌ Problem: Blank page / tidak load

**Penyebab:** Backend tidak respond

**Solusi:**

1. Buka DevTools (F12 atau Cmd+Option+I)
2. Lihat tab Console untuk error
3. Lihat tab Network untuk failed requests
4. Pastikan backend jalan di http://127.0.0.1:8000

---

## ❓ FAQ

### Q: Apakah harus menjalankan 2 terminal?

**A:** YA! Backend dan Frontend harus jalan bersamaan.

```
Terminal 1: Backend  (Port 8000) ← Wajib
Terminal 2: Frontend (Port 5174) ← Wajib
```

### Q: Berapa lama waktu startup?

**A:** 
- Backend: ~3-5 detik
- Frontend: ~2-3 detik

Total: sekitar 5-8 detik sampai siap

### Q: Bisa pakai Chrome/Safari/Firefox?

**A:** Bisa semua browser modern. Rekomendasi: Chrome atau Edge.

### Q: Apakah perlu koneksi internet?

**A:** YA, untuk:
- Fetch data saham dari Yahoo Finance
- Load beberapa library eksternal

### Q: Port 8000 dan 5174 bisa diganti?

**A:** 
- Backend: Bisa ganti port di command `--port XXXX`
- Frontend: Otomatis pakai port lain jika 5174 terpakai
- **PENTING:** Jika ganti port backend, update juga di frontend config

### Q: Data saham real-time atau delayed?

**A:** Delayed ~15 menit (standard Yahoo Finance free tier)

### Q: Berapa banyak saham yang didukung?

**A:** 120+ saham Indonesian (IDX-30, LQ45, Banking, Mining, dll)

### Q: Demo account bisa ganti password?

**A:** Tidak. Demo account read-only. Untuk ganti, buat account baru via Sign Up.

---

## 🎯 Quick Start Checklist

Gunakan checklist ini setiap kali mau jalankan website:

```
□ Backend folder:     /Users/zelda/stock-ai-engine
□ Frontend folder:    /Users/zelda/stock-ai-frontend

□ Terminal 1 terbuka
  □ cd /Users/zelda/stock-ai-engine
  □ source venv/bin/activate
  □ python -m uvicorn app_b2c:app --reload --port 8000
  □ Tunggu muncul "Uvicorn running on http://127.0.0.1:8000"

□ Terminal 2 terbuka  
  □ cd /Users/zelda/stock-ai-frontend
  □ npm run dev
  □ Tunggu muncul "Local: http://localhost:5174/"

□ Test Backend:       http://127.0.0.1:8000/docs
□ Test Frontend:      http://localhost:5174

□ Login dengan:
  □ Email: demo@example.com
  □ Password: demo123

✅ READY! Mulai analisa saham!
```

---

## 📞 Butuh Bantuan?

### Jika masih error setelah ikuti panduan ini:

1. **Buka DevTools** di browser (F12 atau Cmd+Option+I)
2. **Lihat tab Console** - screenshot error yang muncul
3. **Lihat tab Network** - cek request yang failed
4. **Kirim info ke GitHub Issues:**
   - Screenshot error
   - Output dari terminal backend
   - Output dari terminal frontend
   - Versi Python, Node.js, dan macOS

### GitHub Repository

🔗 https://github.com/GeraldElroy7/stock-ai-engine

---

## 📚 Dokumentasi Tambahan

- [README.md](README.md) - Overview proyek
- [QUICK_START.md](QUICK_START.md) - Quick start guide
- [SETUP_FRONTEND.md](SETUP_FRONTEND.md) - Frontend setup details
- [B2C_UPDATE.md](B2C_UPDATE.md) - B2C platform features
- [MACOS_QUICK_COMMANDS.md](MACOS_QUICK_COMMANDS.md) - macOS command reference

---

**Last Updated:** 3 Januari 2026  
**Version:** 2.0.0  
**Platform:** macOS  
**Status:** ✅ Production Ready

---

🎉 **Selamat! Anda sudah siap menggunakan Stock AI Engine!**
