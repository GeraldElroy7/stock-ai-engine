# Frontend Repository Setup Guide

## 📍 Frontend Location

**Frontend folder:** `/Users/zelda/stock-ai-frontend` (Outside main repo)

**Alasan:** Frontend dan Backend adalah 2 project terpisah:
- Backend: Python/FastAPI
- Frontend: React/Node.js

---

## 🚀 Setup Frontend Repository

### Option 1: Create New Repository (Recommended)

#### Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `stock-ai-frontend`
   - **Description:** React 18 Frontend for Stock AI Engine
   - **Visibility:** Public
   - **Initialize:** No (already have files)
3. Click **Create repository**

#### Step 2: Connect Local to GitHub

```bash
cd /Users/zelda/stock-ai-frontend

# Set remote
git remote add origin https://github.com/GeraldElroy7/stock-ai-frontend.git
git branch -M main
git push -u origin main
```

**✅ Done!** Frontend is now on GitHub

---

### Option 2: Add Frontend to Backend Repository

If you want everything in one place:

```bash
# Copy frontend into backend repo
cp -r /Users/zelda/stock-ai-frontend \
  /Users/zelda/stock-ai-engine/packages/frontend

# Add to git
cd /Users/zelda/stock-ai-engine
git add packages/frontend/
git commit -m "feat: add React frontend to monorepo"
git push origin main
```

---

## 📊 Current Frontend Status

```
Frontend Folder: /Users/zelda/stock-ai-frontend
Git Status:      ✅ Initialized locally
GitHub Status:   ❌ Need to create repo

Last Commit:
  - 63d2c5a feat: React 18 frontend with Vite
  - Files: 39 files, 6.6 KB

Fixed Issues:
  ✅ Auth endpoint: /api/v2/auth/login
  ✅ Register endpoint: /api/v2/auth/register
  ✅ User data parsing for demo account
```

---

## 🔗 Project Structure

```
Home Directory:
├── /Users/zelda/stock-ai-engine/        ← Backend (Python)
│   ├── app_b2c.py
│   ├── api/
│   ├── engine/
│   ├── data/
│   └── requirements.txt
│
└── /Users/zelda/stock-ai-frontend/      ← Frontend (React)
    ├── src/
    ├── package.json
    ├── vite.config.js
    └── tailwind.config.js
```

---

## ✅ Frontend Features

- ✅ Landing page with hero section
- ✅ Login & Register pages with JWT auth
- ✅ Dashboard with stock search
- ✅ Stock analysis page with charts
- ✅ AI recommendations display
- ✅ Settings page
- ✅ Light/Dark mode toggle
- ✅ Responsive design
- ✅ Framer Motion animations
- ✅ Recharts integration

---

## 🚀 Running Frontend & Backend Together

### Terminal 1: Backend
```bash
cd /Users/zelda/stock-ai-engine
source venv/bin/activate
python -m uvicorn app_b2c:app --reload --port 8000
```

### Terminal 2: Frontend
```bash
cd /Users/zelda/stock-ai-frontend
npm run dev
```

**Open:** http://localhost:5174

---

## 📝 Frontend Components

### Pages
- `Landing.jsx` - Homepage with features
- `Login.jsx` - Login form
- `Register.jsx` - Registration form
- `Dashboard.jsx` - Main dashboard
- `Analysis.jsx` - Stock analysis page
- `Settings.jsx` - User settings

### Components
- `Navbar.jsx` - Top navigation
- `Button.jsx` - Reusable button
- `Input.jsx` - Reusable input field
- `Card.jsx` - Card component
- `Alert.jsx` - Alert message
- `Footer.jsx` - Footer

### Context & Hooks
- `AuthContext.jsx` - Authentication state
- `ThemeContext.jsx` - Light/Dark mode
- `useAuth.js` - Auth hook
- `useTheme.js` - Theme hook

### Services
- `api.js` - API utilities
- `stockService.js` - Stock-related API calls

---

## 🔧 Frontend Technologies

- **React 18** - UI library
- **Vite** - Build tool
- **React Router** - Navigation
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Recharts** - Data visualization
- **Axios/Fetch** - HTTP requests

---

## 🐛 Known Issues Fixed

1. **Wrong API endpoint** ✅
   - Was: `/api/auth/login`
   - Now: `/api/v2/auth/login`

2. **User response parsing** ✅
   - Was: Expect `data.user` from backend
   - Now: Extract user from email

3. **Register endpoint** ✅
   - Was: `/api/auth/register`
   - Now: `/api/v2/auth/register`

---

## 📚 Related Documentation

- [PANDUAN_LENGKAP_MACOS.md](../PANDUAN_LENGKAP_MACOS.md) - Complete setup guide
- [QUICK_CHECKLIST.md](../QUICK_CHECKLIST.md) - Quick start
- [SETUP_FRONTEND.md](../SETUP_FRONTEND.md) - Frontend setup details

---

## 🎯 Next Steps

1. **Create GitHub repository** for frontend (see Option 1 above)
2. **Push frontend to GitHub**
3. **Update README.md** with links to both repos
4. **Add GitHub repo links** to documentation

---

**Frontend is ready to deploy!** 🚀
