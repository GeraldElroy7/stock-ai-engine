# 🚀 Stock AI Engine - React Website Implementation Guide

**Date**: January 1, 2026  
**Status**: 🟢 IN PROGRESS  
**Frontend Location**: `/Users/zelda/stock-ai-frontend`

---

## 📊 Executive Summary

Building a **modern web3-style** React website with:
- ✅ Dark mode default (elegant deep navy blue)
- ✅ Light mode toggle
- ✅ Premium, expensive UI look
- ✅ Full API integration with backend
- ✅ 6 pages (Landing, Auth, Dashboard, Analysis, Settings, Pricing)
- ✅ Responsive design (mobile + desktop)

---

## 🎯 Business Justification

**Why React Website NOW?**

1. **Backend Score**: 95/100 ⭐⭐⭐⭐⭐ (Production Ready)
2. **Frontend Score**: 0/100 ❌ (BLOCKER)
3. **Overall Score**: 47.5/100 ⚠️

**After Frontend Launch**: 95/100 ⭐⭐⭐⭐⭐ MARKET READY!

**Impact**:
- Unblocks user acquisition (retail investors need UI)
- Unblocks monetization (payment needs frontend)
- Unblocks growth (SEO, marketing, investor demo)
- Time to market: 2 weeks max

---

## 📦 Tech Stack

### Core
- ⚡ **Vite** 5.4+ - Lightning fast dev server
- ⚛️ **React** 18 - Modern React with hooks
- 🎨 **TailwindCSS** 3.4+ - Utility-first CSS
- 🎭 **Framer Motion** - Smooth animations
- 📊 **Recharts** - Beautiful stock charts
- 🔗 **Axios** - HTTP client for API calls
- 🚦 **React Router** 6 - Client-side routing
- 🎯 **Lucide React** - Modern icons

### Dev Tools
- 📝 **PostCSS** + Autoprefixer
- 🔥 **Hot Module Replacement** (HMR)
- 📱 **Responsive Design** utilities

---

## 🎨 Design System

### Color Palette

**Dark Mode** (Default):
```css
Background: #0a0e27  /* Deep navy */
Surface:    #111827  /* Dark gray */
Border:     #1f2937  /* Darker gray */
Primary:    #3b82f6  /* Elegant blue */
Secondary:  #8b5cf6  /* Purple accent */
Text:       #e2e8f0  /* Soft white */
Muted:      #94a3b8  /* Light gray */
```

**Light Mode**:
```css
Background: #ffffff  /* White */
Surface:    #f8fafc  /* Light gray */
Border:     #e2e8f0  /* Border gray */
Primary:    #2563eb  /* Darker blue */
Secondary:  #7c3aed  /* Darker purple */
Text:       #1e293b  /* Dark slate */
Muted:      #64748b  /* Gray */
```

### Design Features
- 🔮 **Glass Morphism**: Frosted glass effects
- ✨ **Gradient Animations**: Smooth background transitions
- 🎯 **Card Hover Effects**: Scale + shadow on hover
- 🌊 **Smooth Scrollbar**: Custom styled scrollbar
- 📱 **Responsive**: Mobile-first design

---

## 📁 Project Structure

```
stock-ai-frontend/
├── public/
│   └── vite.svg
├── src/
│   ├── assets/
│   │   └── logo.svg
│   ├── components/
│   │   ├── shared/
│   │   │   ├── Navbar.jsx         # Navigation with theme toggle
│   │   │   ├── Footer.jsx         # Footer links
│   │   │   ├── Button.jsx         # Reusable button
│   │   │   ├── Card.jsx           # Glass card component
│   │   │   ├── Input.jsx          # Form input
│   │   │   └── Loading.jsx        # Loading spinner
│   │   ├── dashboard/
│   │   │   ├── StockSearchBar.jsx
│   │   │   ├── WatchlistCard.jsx
│   │   │   ├── QuickStats.jsx
│   │   │   └── RecentAnalyses.jsx
│   │   └── analysis/
│   │       ├── CompanyInfoCard.jsx
│   │       ├── TechnicalChart.jsx
│   │       ├── FundamentalMetrics.jsx
│   │       ├── AIRecommendation.jsx
│   │       ├── RiskAssessment.jsx
│   │       └── PersonalizationForm.jsx
│   ├── pages/
│   │   ├── LandingPage.jsx        # Public homepage
│   │   ├── LoginPage.jsx          # Login form
│   │   ├── RegisterPage.jsx       # Register form
│   │   ├── DashboardPage.jsx      # Protected dashboard
│   │   ├── StockAnalysisPage.jsx  # Main analysis page
│   │   ├── SettingsPage.jsx       # User settings
│   │   └── PricingPage.jsx        # Pricing plans
│   ├── context/
│   │   ├── ThemeContext.jsx       # Dark/Light mode
│   │   └── AuthContext.jsx        # User authentication
│   ├── services/
│   │   └── api.js                 # API integration
│   ├── utils/
│   │   ├── formatters.js          # Number/date formatters
│   │   └── validators.js          # Form validation
│   ├── App.jsx                    # Main app component
│   ├── main.jsx                   # React entry point
│   └── index.css                  # Tailwind + custom CSS
├── tailwind.config.js             # Tailwind configuration
├── postcss.config.js              # PostCSS configuration
├── vite.config.js                 # Vite configuration
└── package.json                   # Dependencies
```

---

## 🔧 Setup Instructions

### 1. Project Already Created ✅
```bash
cd /Users/zelda/stock-ai-frontend
```

### 2. Dependencies Already Installed ✅
```bash
# Core dependencies
npm install react react-dom
npm install react-router-dom
npm install axios
npm install lucide-react

# UI & Animation
npm install -D tailwindcss postcss autoprefixer
npm install framer-motion
npm install recharts
```

### 3. Configuration Files Created ✅
- `tailwind.config.js` ✅
- `postcss.config.js` ✅
- `src/index.css` ✅

---

## 📄 Pages Overview

### 1. 🏠 Landing Page (Public)

**Route**: `/`

**Sections**:
- Hero: Gradient background, main value proposition
- Features: 4 key features (AI Analysis, 100+ Metrics, Personalization, Real-time)
- Pricing: Free vs Premium comparison
- CTA: "Try Demo" or "Sign Up Free"

**Components**:
```jsx
<LandingPage>
  <Navbar />
  <HeroSection />
  <FeaturesSection />
  <PricingSection />
  <Footer />
</LandingPage>
```

---

### 2. 🔐 Auth Pages (Public)

**Routes**: `/login`, `/register`

**Login Page**:
- Email & password inputs
- "Try Demo" button (auto-fills demo@example.com / demo123)
- Link to register

**Register Page**:
- Full name, email, password inputs
- Terms & conditions checkbox
- Link to login

**API Calls**:
```javascript
// Login
POST /api/v2/auth/login
Body: { email, password }
Response: { access_token, refresh_token, user }

// Register
POST /api/v2/auth/register
Body: { email, password, full_name }
Response: { user_id, email, message }
```

---

### 3. 📊 Dashboard Page (Protected)

**Route**: `/dashboard`

**Sections**:
- Stock Search Bar (autocomplete from 120+ stocks)
- Watchlist (user's favorite stocks)
- Quick Stats (portfolio summary)
- Recent Analyses (history)

**API Calls**:
```javascript
// Get all stocks
GET /api/v2/stocks/list?sector=ALL
Response: { stocks: [ { ticker, name, sector, description } ] }
```

---

### 4. 📈 Stock Analysis Page (Protected) ⭐ MAIN PAGE

**Route**: `/analysis/:ticker`

**Sections**:
1. **Company Info Card**
   - Company name, ticker, sector
   - Current price, change %
   - Market cap

2. **Technical Chart**
   - Price history (Recharts LineChart)
   - Volume bars
   - EMA lines (10, 20, 50)
   - RSI, MACD indicators

3. **Fundamental Metrics**
   - 100+ metrics organized by category:
     - Valuation (PE, PB, PS)
     - Profitability (ROE, Profit Margin)
     - Financial Health (Debt/Equity, Current Ratio)
     - Dividend (Yield, Payout Ratio)
   - Fundamental Score: 0-100 with rating

4. **AI Recommendation Card**
   - Signal: BUY/SELL/HOLD/SHORT
   - Confidence: 0-100%
   - Entry price, Target price, Stop loss
   - Action items (3-5 bullet points)

5. **Risk Assessment**
   - Risk score: 0-100
   - Suitability for user's risk profile
   - Risk factors list

6. **Personalization Form**
   - Trading style selector
   - Risk level selector
   - Capital size input
   - Investment goal dropdown
   - Sector preferences

**API Call**:
```javascript
POST /api/v2/stock/info
Headers: { Authorization: Bearer ${token} }
Body: {
  ticker: "BBCA",
  trading_style: "swing_trader",
  risk_level: "moderate",
  capital_size: 100000000,
  investment_goal: "balanced"
}
Response: { 
  company_info: {...},
  technical_analysis: {...},
  fundamental_analysis: {...},
  ai_recommendation: {...},
  risk_assessment: {...},
  personalized_insights: {...}
}
```

---

### 5. ⚙️ Settings Page (Protected)

**Route**: `/settings`

**Sections**:
- Profile Management (name, email)
- Dark/Light Mode Toggle
- API Key Management (for premium users)
- Subscription Status
- Change Password

---

### 6. 💳 Pricing Page (Public)

**Route**: `/pricing`

**Tiers**:
```
FREE:
  ✅ 10 stocks access
  ✅ Basic signals
  ✅ 1-year data
  ✅ Limited analyses (10/month)
  Price: Rp 0

PREMIUM:
  ✅ 120+ stocks access
  ✅ AI recommendations
  ✅ 10-year data
  ✅ Unlimited analyses
  ✅ Webhook alerts
  ✅ Premium support
  Price: Rp 149k/month
```

---

## 🔌 API Integration

### Base Configuration

```javascript
// src/services/api.js
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

### API Methods

```javascript
// Authentication
export const login = (email, password) => 
  api.post('/api/v2/auth/login', { email, password });

export const register = (email, password, full_name) =>
  api.post('/api/v2/auth/register', { email, password, full_name });

// Stock Data
export const getStocksList = (sector = 'ALL') =>
  api.get(`/api/v2/stocks/list?sector=${sector}`);

export const getStockInfo = (ticker, preferences) =>
  api.post('/api/v2/stock/info', { ticker, ...preferences });

// User
export const getUserParameters = () =>
  api.get('/api/v2/user/parameters');
```

---

## 🎭 Theme Context (Dark/Light Mode)

```javascript
// src/context/ThemeContext.jsx
import { createContext, useState, useEffect } from 'react';

export const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('dark'); // default dark

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    setTheme(savedTheme);
    document.documentElement.classList.toggle('dark', savedTheme === 'dark');
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
```

---

## 🔐 Auth Context

```javascript
// src/context/AuthContext.jsx
import { createContext, useState, useEffect } from 'react';
import { login as apiLogin, register as apiRegister } from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const userData = localStorage.getItem('user');
    if (token && userData) {
      setUser(JSON.parse(userData));
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    const response = await apiLogin(email, password);
    const { access_token, user } = response.data;
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('user', JSON.stringify(user));
    setUser(user);
    return user;
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
```

---

## 🚀 Running the App

### Development
```bash
cd /Users/zelda/stock-ai-frontend
npm run dev
```

Access: http://localhost:5173

### Build for Production
```bash
npm run build
```

Output: `/Users/zelda/stock-ai-frontend/dist`

### Deploy to Vercel (Free)
```bash
npm install -g vercel
vercel login
vercel --prod
```

---

## ✅ Implementation Checklist

### Phase 1: Setup (DONE ✅)
- [x] Create Vite project
- [x] Install dependencies
- [x] Configure Tailwind
- [x] Setup custom CSS

### Phase 2: Core Components (NEXT)
- [ ] Create shared components (Navbar, Footer, Button, Card, Input)
- [ ] Create Theme Context
- [ ] Create Auth Context
- [ ] Setup React Router

### Phase 3: Pages (IN PROGRESS)
- [ ] Landing Page
- [ ] Login/Register Pages
- [ ] Dashboard Page
- [ ] Stock Analysis Page (MAIN)
- [ ] Settings Page
- [ ] Pricing Page

### Phase 4: API Integration
- [ ] Setup axios interceptors
- [ ] Create API service methods
- [ ] Test all endpoints

### Phase 5: Polish
- [ ] Add loading states
- [ ] Add error handling
- [ ] Optimize performance
- [ ] Mobile responsiveness testing

### Phase 6: Deploy
- [ ] Build for production
- [ ] Deploy to Vercel
- [ ] Connect to backend API (CORS)
- [ ] Test live site

---

## 📊 Progress Tracking

**Overall**: 15% Complete

| Component | Status | Progress |
|-----------|--------|----------|
| Project Setup | ✅ Done | 100% |
| Tailwind Config | ✅ Done | 100% |
| Dependencies | ✅ Done | 100% |
| Shared Components | 🟡 In Progress | 0% |
| Theme Context | 🟡 To Do | 0% |
| Auth Context | 🟡 To Do | 0% |
| Landing Page | 🟡 To Do | 0% |
| Auth Pages | 🟡 To Do | 0% |
| Dashboard | 🟡 To Do | 0% |
| Stock Analysis | 🟡 To Do | 0% |
| Settings | 🟡 To Do | 0% |
| Pricing | 🟡 To Do | 0% |
| API Integration | 🟡 To Do | 0% |
| Deployment | 🟡 To Do | 0% |

---

## 🎯 Next Steps

1. **Continue Building Components** (IMMEDIATE)
   - Create all shared components
   - Build page layouts
   - Integrate with API

2. **Test with Backend** (AFTER BUILD)
   - Start backend: `python -m uvicorn app_b2c:app --reload --port 8000`
   - Test login with demo account
   - Test stock analysis with BBCA

3. **Polish & Deploy** (FINAL)
   - Mobile testing
   - Performance optimization
   - Deploy to Vercel

---

## 💡 Tips for Development

1. **Start Backend First**:
   ```bash
   cd /Users/zelda/stock-ai-engine
   python -m uvicorn app_b2c:app --reload --port 8000
   ```

2. **Use Demo Account**:
   - Email: demo@example.com
   - Password: demo123

3. **Test with BBCA Stock**:
   - Ticker: BBCA
   - Sector: BANKING
   - Has good data for testing

4. **Dark Mode First**:
   - Build in dark mode
   - Test light mode after

---

## 📞 Support

**Documentation**:
- Backend API: http://127.0.0.1:8000/docs
- React Docs: https://react.dev
- Tailwind Docs: https://tailwindcss.com

**Continuation Instructions**:
To continue building, run:
```bash
cd /Users/zelda/stock-ai-frontend
npm run dev
```

Then start creating components in `src/components/` and pages in `src/pages/`.

---

**Status**: 🟢 Frontend Development In Progress  
**Started**: January 1, 2026  
**ETA**: 2 weeks to production ready

**Next Session**: Continue building React components and pages!
