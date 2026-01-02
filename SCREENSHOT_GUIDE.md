# 📸 Screenshot Guide - Cara Ambil Screenshot untuk Dokumentasi

> Panduan untuk mengambil screenshot UI Stock AI Engine

---

## 🎯 Screenshot yang Dibutuhkan

### 1. Landing Page
**URL:** http://localhost:5174

**Ambil screenshot:**
- Full page dengan navbar
- Tombol "Sign In" dan "Sign Up" terlihat
- Hero section dengan judul

**Simpan sebagai:** `docs/screenshots/01-landing-page.png`

---

### 2. Login Page
**URL:** http://localhost:5174/login

**Ambil screenshot:**
- Form login dengan field email & password
- Tombol "Try Demo Account"
- Tombol "Sign In"

**Simpan sebagai:** `docs/screenshots/02-login-page.png`

---

### 3. Dashboard (After Login)
**URL:** http://localhost:5174/dashboard

**Ambil screenshot:**
- Header dengan profile icon
- Search bar
- Featured stocks cards
- Watchlist jika ada

**Simpan sebagai:** `docs/screenshots/03-dashboard.png`

---

### 4. Stock Analysis Page
**URL:** http://localhost:5174/analysis/BBCA

**Ambil screenshot:**
- Stock price chart
- Technical indicators
- Fundamental metrics
- AI recommendation box
- Action items

**Simpan sebagai:** `docs/screenshots/04-stock-analysis.png`

---

### 5. Backend API Documentation
**URL:** http://127.0.0.1:8000/docs

**Ambil screenshot:**
- Swagger UI
- List of endpoints
- Authentication section visible

**Simpan sebagai:** `docs/screenshots/05-api-docs.png`

---

## 💻 Cara Ambil Screenshot di macOS

### Method 1: Full Screen
```
Cmd + Shift + 3
```
Otomatis save ke Desktop

### Method 2: Selected Area
```
Cmd + Shift + 4
```
Drag untuk select area, otomatis save ke Desktop

### Method 3: Specific Window
```
Cmd + Shift + 4, kemudian tekan Spacebar
```
Klik window yang mau di-screenshot

### Method 4: Screenshot Tool
```
Cmd + Shift + 5
```
Buka screenshot toolbar dengan berbagai opsi

---

## 📁 Struktur Folder Screenshot

```
stock-ai-engine/
└── docs/
    └── screenshots/
        ├── 01-landing-page.png
        ├── 02-login-page.png
        ├── 03-dashboard.png
        ├── 04-stock-analysis.png
        └── 05-api-docs.png
```

---

## 🔧 Edit Screenshot (Optional)

Gunakan **Preview** app di macOS:

1. Buka screenshot dengan Preview
2. **Tools → Annotate** untuk tambah:
   - Arrow (untuk point sesuatu)
   - Text box (untuk label)
   - Rectangle (untuk highlight area)
3. **File → Export** untuk save

---

## ✅ Checklist Screenshot

Sebelum upload ke GitHub, pastikan:

- [ ] Screenshot clear dan readable
- [ ] Tidak ada informasi sensitif (API keys, password, dll)
- [ ] Size tidak terlalu besar (< 500KB per file)
- [ ] Format PNG (lebih baik dari JPG untuk UI)
- [ ] Nama file descriptive

---

## 📤 Upload ke GitHub

### Via Terminal:

```bash
cd /Users/zelda/stock-ai-engine

# Create screenshots folder
mkdir -p docs/screenshots

# Move screenshots to folder
mv ~/Desktop/screenshot-*.png docs/screenshots/

# Rename according to guide
mv docs/screenshots/screenshot-1.png docs/screenshots/01-landing-page.png
# ... dst

# Commit and push
git add docs/screenshots/
git commit -m "docs: add UI screenshots"
git push origin main
```

### Via GitHub Web:

1. Go to https://github.com/GeraldElroy7/stock-ai-engine
2. Navigate to `docs/` folder
3. Click **Add file → Upload files**
4. Drag & drop screenshots
5. Commit changes

---

## 🎨 Tips untuk Screenshot yang Bagus

1. **Gunakan Light Mode** - Lebih mudah dibaca di dokumentasi
2. **Zoom 100%** - Jangan terlalu zoom in/out
3. **Clean browser** - Hide bookmarks bar, close tabs yang tidak perlu
4. **Full window** - Jangan minimize atau resize window
5. **Annotate important parts** - Pakai arrow atau box untuk highlight fitur penting

---

## 📝 Update Dokumentasi dengan Screenshot

Setelah upload screenshot, update `PANDUAN_LENGKAP_MACOS.md`:

```markdown
### 1. Buka Website

![Landing Page](docs/screenshots/01-landing-page.png)

### 2. Klik "Sign In"

![Login Page](docs/screenshots/02-login-page.png)
```

---

**Ready to document your UI!** 📸✨
