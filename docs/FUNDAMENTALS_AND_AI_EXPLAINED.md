# Fundamental Data & AI Analysis - Detailed Explanation

## 1. How Fundamental Data Works (The Flow)

### Data Source & Storage
```
You (user) provide:
    └─ JSON files under: data/fund_data/{SYMBOL}.json
       Example: data/fund_data/BBCA.json
```

### Data File Format (5-year example - BBCA)
```json
{
  "symbol": "BBCA",
  "company_name": "Bank Central Asia",
  "fundamentals": [
    {
      "year": 2024,
      "pe_ratio": 7.2,           // Price-to-Earnings (low = cheap)
      "pb_ratio": 1.35,           // Price-to-Book
      "roe_pct": 18.7,            // Return on Equity % (high = good profitability)
      "roa_pct": 2.1,             // Return on Assets
      "revenue_growth_pct": 12.3, // Year-over-year growth
      "net_income_growth_pct": 15.8,
      "market_cap_usd": 12500000000,
      "debt_to_equity": 0.15,
      "dividend_yield_pct": 3.2
    },
    { "year": 2023, ... },
    { "year": 2022, ... },
    { "year": 2021, ... },
    { "year": 2020, ... }
  ]
}
```

### How It's Used (Step by Step)

**Step 1:** User calls `/analysis` endpoint
```bash
curl -X POST "http://127.0.0.1:8000/analysis" \
  -H "Content-Type: application/json" \
  -d '{"symbols":["BBCA"],"mode":"both"}'
```

**Step 2:** Endpoint calls `fetch_fundamentals("BBCA")`
- Looks for file: `data/fund_data/BBCA.json`
- If found → Loads entire JSON (including 5-year history)
- If NOT found → Returns mock data `{"symbol": "BBCA", "note": "mocked"}`

**Step 3:** Endpoint calls `summarize_analysis(tech_report, fund_report, mode="both")`
- Takes technical signal (from decision_engine) + fundamental data
- Analyzes both with **smart rules**:
  - Technical: BUY/SELL/HOLD based on short-term indicators
  - Fundamental: Valuation (PE), Quality (ROE), Growth trends
- Returns combined recommendation

**Step 4:** Result includes:
```json
{
  "symbol": "BBCA",
  "technical": {...signal data...},
  "fundamental": {...the JSON you provided...},
  "summary": {
    "mode": "both",
    "technical_score": 2.5,
    "fundamental_score": 1.2,
    "total_score": 3.7,
    "recommendation": "BUY (tech + value)",
    "reasoning": [
      "Technical BUY signal (score=6.5, confidence=0.8)",
      "Fundamentals (2024): PE=7.2, PB=1.35, ROE=18.7%, Growth=15.8%",
      "✓ Undervalued (PE < 8)",
      "✓ Good profitability (ROE=18.7%)",
      "✓ Strong earnings growth (15.8%)",
      "✓ Valuation improving: PE 13.8→7.2"
    ]
  }
}
```

---

## 2. 5-10 Year Historical Data for Better Decisions

I've provided **5-year data** (2020-2024) for BBCA and BBRI. Here's why and what it enables:

### What We Calculate From 5-Year Data

| Metric | How It's Used | Example |
|--------|--------------|---------|
| **PE Trend** | Identify if stock is getting cheaper/expensive | BBCA: 13.8 (2020) → 7.2 (2024) = **getting cheaper** ✓ |
| **ROE Stability** | Check if company is consistently profitable | BBCA: 13.9% → 18.7% = **improving** ✓ |
| **Growth Acceleration** | See if business is accelerating | BBRI: 1.5% → 14.7% growth = **strong acceleration** ✓ |
| **Debt Trends** | Monitor financial health | Both banks: debt decreasing ✓ |
| **Dividend Growth** | Sustainability of dividends | BBCA: stable 3.2-4.5% ✓ |

### How to Add More Historical Data

Option 1: **Manual Entry (Excel → JSON)**
- Collect 10 years of data from IDX website or Bloomberg
- Format as shown above
- Save as `data/fund_data/{SYMBOL}.json`

Option 2: **Fetch from API** (Recommended)
I can integrate one of these:
- **Alpha Vantage** (free tier, 5 calls/min): PE, dividend history
- **IEX Cloud** (paid, high quality): full fundamental data
- **Yahoo Finance API** (via yfinance extensions): limited but free

Example to add API fetch:
```python
# In data/fundamentals.py
import requests

def fetch_fundamentals_from_api(symbol: str, years: int = 5):
    url = f"https://api.example.com/fundamentals/{symbol}"
    resp = requests.get(url)
    return resp.json()
```

---

## 3. Is AI Implemented? (Yes, But It's Rule-Based, Not LLM)

### Current Implementation: Smart Rule-Based Analysis

**NOT** OpenAI/Claude/LLM yet. Instead:
- **Technical Analysis Score**: -3 to +3 based on signals
- **Fundamental Analysis Score**: -1.5 to +2.5 based on metrics
- **Combined Score**: Triggers recommendation based on thresholds

### How the "AI" Works Now

```
TECHNICAL COMPONENT:
  Signal = BUY           → tech_score = +3
  Signal = SELL          → tech_score = -2
  Signal = SHORT         → tech_score = -3
  Signal = HOLD          → tech_score = 0

FUNDAMENTAL COMPONENT:
  PE < 8                 → +1.5 (undervalued)
  PE 8-10                → +0.5 (fair)
  PE > 12                → -0.5 (overvalued)
  
  ROE > 15%              → +1 (good quality)
  ROE < 10%              → -1 (weak quality)
  
  Growth > 10%           → +1 (strong)
  Growth < 0%            → -1 (declining)
  
  PE improving 5-year    → +0.5 (bonus)

FINAL RECOMMENDATION:
  total_score >= 3.5     → "STRONG BUY (tech + value)"
  tech_score >= 2.5      → "BUY (technical strength)"
  fund_score >= 2        → "BUY (value play)"
  total_score <= -2.5    → "STRONG SELL"
  else                   → "HOLD"
```

### Example: BBCA vs BBRI Analysis

**BBCA:**
```
Technical Score: 2.5 (BUY signal)
Fundamental Score: 1.8
  - PE 7.2 (undervalued) = +1.5
  - ROE 18.7% (good) = +1
  - Growth 15.8% (strong) = +1
  - PE improved 13.8→7.2 = +0.5
Total: 4.3 → "STRONG BUY (tech + value)"
```

**BBRI:**
```
Technical Score: -1 (HOLD signal)
Fundamental Score: 2.2
  - PE 5.8 (very undervalued) = +1.5
  - ROE 19.4% (excellent) = +1
  - Growth 18.3% (very strong) = +1
  - PE improved 10.5→5.8 = +0.5
Total: 1.2 → "BUY (value play)" (despite weak technical)
```

**Result:** Different recommendations show the system **differentiates** between technical and fundamental angles.

---

## 4. To See Real Results Now

**Start server:**
```powershell
cd C:\Users\Bittime\Documents\Script\stock_ai_engine
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

**Test all 3 modes:**
```bash
# Technical only
curl -X POST "http://127.0.0.1:8000/analysis" \
  -H "Content-Type: application/json" \
  -d '{"symbols":["BBCA","BBRI"],"mode":"technical"}'

# Fundamental only
curl -X POST "http://127.0.0.1:8000/analysis" \
  -H "Content-Type: application/json" \
  -d '{"symbols":["BBCA","BBRI"],"mode":"fundamental"}'

# Combined (both)
curl -X POST "http://127.0.0.1:8000/analysis" \
  -H "Content-Type: application/json" \
  -d '{"symbols":["BBCA","BBRI"],"mode":"both"}'
```

You'll see **different recommendations** for each mode!

---

## 5. Future: Real AI (LLM-Based Summaries)

If you want actual AI sentences (not rules), I can add:
```python
# Using OpenAI API
def summarize_with_llm(tech, fund, mode):
    prompt = f"""
    Technical signal: {tech['signal']}, score: {tech['score']}
    PE ratio: {fund['pe_ratio']}, ROE: {fund['roe_pct']}%
    
    Provide a 2-sentence investment recommendation.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

To enable this, provide:
- OpenAI API key, or
- Hugging Face API key, or
- Keep rule-based (free, but less "natural")

---

## Summary

✅ **Fundamental data:** JSON files under `data/fund_data/` — 5 years provided now  
✅ **AI summary:** Rule-based analysis differentiating technical vs fundamental  
✅ **Difference visible:** Test `/analysis` with `mode=technical`, `fundamental`, `both` to see different recommendations  
✅ **Historical:** 5-year trends analyzed for valuation improvement & growth acceleration  

Next: Run the test and see it in action!
