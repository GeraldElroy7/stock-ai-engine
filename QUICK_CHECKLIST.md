# ✅ Quick Checklist - Jalankan Website dalam 2 Menit

> Panduan singkat untuk start website setiap kali dibutuhkan

---

## 🎯 Quick Start (2 Menit)

### 1️⃣ Terminal 1: Backend (30 detik)

```bash
cd /Users/zelda/stock-ai-engine
source venv/bin/activate
python -m uvicorn app_b2c:app --reload --port 8000
```

**✅ Tunggu muncul:** `Uvicorn running on http://127.0.0.1:8000`

---

### 2️⃣ Terminal 2: Frontend (30 detik)

```bash
cd /Users/zelda/stock-ai-frontend
npm run dev
```

**✅ Tunggu muncul:** `Local: http://localhost:5174/`

---

### 3️⃣ Buka Browser (30 detik)

```
http://localhost:5174
```

**✅ Klik "Sign In"** → **"Try Demo Account"** → **Login**

---

## 🚦 Status Check

### Backend Check:
```bash
curl http://127.0.0.1:8000/health
```

**✅ Harus return:** `{"status":"healthy"}`

### Frontend Check:
Buka browser: http://localhost:5174

**✅ Harus tampil:** Landing page website

---

## 🔑 Demo Credentials

```
Email:    demo@example.com
Password: demo123
```

**Jangan typo!** Copy-paste untuk aman.

---

## ⚠️ Troubleshooting 1-Menit

### Backend tidak jalan?

```bash
# Kill process yang pakai port 8000
lsof -ti:8000 | xargs kill -9

# Jalankan ulang
cd /Users/zelda/stock-ai-engine
source venv/bin/activate
python -m uvicorn app_b2c:app --reload --port 8000
```

### Frontend tidak jalan?

```bash
# Kill process yang pakai port 5174
lsof -ti:5174 | xargs kill -9

# Jalankan ulang
cd /Users/zelda/stock-ai-frontend
npm run dev
```

### Login error?

1. **Pastikan backend jalan** - Cek http://127.0.0.1:8000/health
2. **Buka DevTools** - F12 atau Cmd+Option+I
3. **Lihat Console** - Ada error apa?
4. **Lihat Network tab** - Request ke `/api/v2/auth/login` berhasil?

---

## 📋 Full Checklist

```
SEBELUM MULAI:
□ Terminal 1 siap
□ Terminal 2 siap
□ Browser siap (Chrome/Safari/Firefox)

START BACKEND:
□ cd /Users/zelda/stock-ai-engine
□ source venv/bin/activate
□ python -m uvicorn app_b2c:app --reload --port 8000
□ Tunggu "Uvicorn running on http://127.0.0.1:8000"
□ Test: curl http://127.0.0.1:8000/health

START FRONTEND:
□ cd /Users/zelda/stock-ai-frontend
□ npm run dev
□ Tunggu "Local: http://localhost:5174/"
□ Test: Buka http://localhost:5174 di browser

LOGIN:
□ Klik "Sign In"
□ Klik "Try Demo Account" ATAU input manual
□ Email: demo@example.com
□ Password: demo123
□ Klik "Sign In" button
□ Tunggu redirect ke Dashboard

SUKSES!
✅ Backend jalan
✅ Frontend jalan
✅ Login berhasil
✅ Dashboard muncul
```

---

## 🛑 Stop Servers

### Stop Backend:
Di terminal backend, tekan: `Ctrl + C`

### Stop Frontend:
Di terminal frontend, tekan: `Ctrl + C`

---

## 📁 Folder Locations

```
Backend:  /Users/zelda/stock-ai-engine
Frontend: /Users/zelda/stock-ai-frontend
```

**Jangan kebalik!** npm run dev hanya jalan di folder frontend.

---

## 🔗 Important URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:5174 | Website UI |
| Backend API | http://127.0.0.1:8000 | REST API |
| API Docs | http://127.0.0.1:8000/docs | Swagger UI |
| Health Check | http://127.0.0.1:8000/health | Server status |

---

## ⏱️ Startup Time

- Backend: ~3-5 seconds
- Frontend: ~2-3 seconds
- **Total: ~5-8 seconds** until ready

---

## 💡 Pro Tips

1. **Keep terminals open** - Jangan close terminal yang ada server
2. **One terminal per server** - Backend di terminal 1, Frontend di terminal 2
3. **Check logs** - Kalau ada error, lihat output di terminal
4. **Restart if needed** - Ctrl+C untuk stop, jalankan command lagi
5. **Use demo account** - Jangan buat account baru untuk testing

---

## 📞 Need Help?

Baca dokumentasi lengkap: [PANDUAN_LENGKAP_MACOS.md](PANDUAN_LENGKAP_MACOS.md)

---

**Ready to analyze stocks!** 📈✨
