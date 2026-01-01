# 🚀 Stock AI Engine Frontend Setup Guide

> React 18 + Vite Frontend for Stock AI Analysis Platform

---

## Quick Start (Backend + Frontend)

### Prerequisites
- Python 3.11+ with venv
- Node.js 18+ (npm/yarn)
- macOS/Linux/WSL

### 1️⃣ Start Backend (Terminal 1)
```bash
cd /Users/zelda/stock-ai-engine
source venv/bin/activate
python -m uvicorn app_b2c:app --reload --port 8000
```

✅ **Backend running**: http://127.0.0.1:8000  
📖 **API Docs**: http://127.0.0.1:8000/docs (Swagger)

---

### 2️⃣ Start Frontend (Terminal 2)
```bash
cd /Users/zelda/stock-ai-frontend
npm install  # one-time only
npm run dev
```

✅ **Frontend running**: http://localhost:5173  
🎨 **Default**: Light mode (white background)  
🌙 **Toggle**: Dark mode via navbar sun/moon icon

---

## How to Use

### Via Web UI (Recommended)
1. **Open** http://localhost:5173
2. **Click** "Sign In" → Choose **"Try Demo Account"**
3. **Demo Credentials**:
   - Email: `demo@example.com`
   - Password: `demo123`
4. **Explore**:
   - Dashboard: View featured stocks
   - Search: Find specific stocks (BBCA, BBRI, ASII, etc.)
   - Analyze: Click any stock → See price history, metrics, AI recommendation
   - Settings: Change theme, manage profile

### Via API + Swagger
1. **Open** http://127.0.0.1:8000/docs
2. **Register** (if needed):
   ```bash
   curl -X POST http://127.0.0.1:8000/api/v2/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "email":"demo@example.com",
       "password":"demo123",
       "full_name":"Demo User"
     }'
   ```
3. **Login** to get token:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/v2/auth/login \
     -H "Content-Type: application/json" \
     -d '{
       "email":"demo@example.com",
       "password":"demo123"
     }'
   ```
4. **Copy** `access_token` from response
5. **In Swagger**:
   - Click **"Authorize"** button (top right)
   - Paste: `Bearer <your_token_here>`
   - Click **Authorize** → **Close**
6. **Try** endpoints like:
   - **POST /api/v2/stock/info** (requires JSON body with ticker, trading_style, etc.)
   - **GET /api/v2/stocks/search?q=BBCA** (search stocks)

---

## Frontend Features

### 🎨 Design System
- **Light Mode**: White background (#fff), dark text (#0f172a)
- **Dark Mode**: Navy background (#0a0e27), light text (#e2e8f0)
- **Responsive**: Mobile-first, works on all devices
- **Smooth**: Framer Motion animations, Recharts graphs

### 📄 Pages
| Page | Purpose |
|------|---------|
| Landing | Hero, features, CTA |
| Login | Sign in or try demo |
| Register | Create new account |
| Dashboard | View portfolio, search stocks, watch list |
| Analysis | Detailed stock info, AI recommendation, charts, personalization |
| Settings | Profile, theme toggle, logout |

### 🔧 Components
- **Shared**: Button, Card, Input, Alert, Badge, Navbar, Footer, Spinner
- **Analysis**: Charts (Recharts), metrics display, recommendation cards
- **Forms**: Personalization (investment horizon, risk tolerance)

### 🔐 Authentication
- **JWT-based**: Secure token storage in localStorage
- **Auto-refresh**: Token refresh on 401 (if backend implements)
- **Protected routes**: Dashboard/Analysis require login

---

## Development Tips

### Troubleshooting

**Problem**: Frontend can't reach backend
- **Solution**: Ensure backend is running on port 8000 and CORS is enabled
- **Check**: http://127.0.0.1:8000/docs loads

**Problem**: Light mode not showing white background
- **Solution**: Clear browser cache (`Cmd+Shift+Delete`) and refresh
- **Or**: Toggle dark mode ON, then toggle back OFF

**Problem**: npm install fails
- **Solution**: Delete `node_modules` and `package-lock.json`, then reinstall:
  ```bash
  rm -rf node_modules package-lock.json
  npm install
  ```

### Build for Production
```bash
npm run build
npm run preview
```
Outputs to `dist/` folder (ready for Vercel/Netlify).

---

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Frontend** | React | 18.2 |
| **Build** | Vite | 7.2 |
| **Styling** | Tailwind CSS | 3.4 |
| **Animation** | Framer Motion | 12.2 |
| **Charts** | Recharts | 3.6 |
| **HTTP** | Axios | 1.13 |
| **Routing** | React Router | 7.1 |
| **Icons** | Lucide React | 0.56 |

---

## File Structure
```
stock-ai-frontend/
├── src/
│   ├── components/
│   │   ├── shared/     (Button, Card, Input, Alert, Badge, Navbar, Footer, Spinner)
│   │   ├── pages/      (Landing, Login, Register, Dashboard, Analysis, Settings)
│   │   └── analysis/   (Charts, metrics, recommendation components)
│   ├── context/        (ThemeContext, AuthContext)
│   ├── hooks/          (useAuth, useTheme, useLocalStorage)
│   ├── services/       (api.js - Axios setup)
│   ├── utils/          (formatters.js - formatting utilities)
│   ├── App.jsx         (Main app + routing)
│   ├── main.jsx        (Entry point)
│   └── index.css       (Tailwind + custom styles)
├── tailwind.config.js  (Tailwind config with custom colors)
├── postcss.config.js   (PostCSS setup)
├── vite.config.js      (Vite config)
└── package.json        (Dependencies)
```

---

## Next Steps

1. **Integrate Real Data**: Connect Analysis page to backend `/api/v2/stock/info` endpoint
2. **Watchlist**: Persist user's favorite stocks to database
3. **Email Alerts**: Notify on price changes
4. **Mobile App**: React Native version
5. **Deploy**: Push to Vercel (frontend) + Railway/Heroku (backend)

---

## Support

- 📖 **API Docs**: http://127.0.0.1:8000/docs (Swagger)
- 🐛 **Issues**: Check GitHub repository
- 💬 **Questions**: Review code comments and component props

---

**Happy analyzing! 📊**
