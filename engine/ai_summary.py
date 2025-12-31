from typing import Dict, Optional
import pandas as pd


def analyze_5year_pattern(df: pd.DataFrame) -> Dict:
    """Analyze 5-year price patterns to understand market position and seasonality."""
    if df is None or df.empty:
        return {}
    
    try:
        # Get latest close and key levels
        current = df["Close"].iloc[-1]
        all_time_high = df["Close"].max()
        all_time_low = df["Close"].min()
        
        # 52-week trend
        if len(df) >= 252:
            price_1y_ago = df["Close"].iloc[-252]
            change_1y = ((current - price_1y_ago) / price_1y_ago * 100)
        else:
            change_1y = 0
        
        # Distance to extremes
        pct_from_low = ((current - all_time_low) / all_time_low * 100)
        pct_from_high = ((all_time_high - current) / all_time_high * 100)
        
        # Calculate seasonality (average returns by month)
        if "month" in df.columns and "daily_return_pct" in df.columns:
            monthly_avg = df.groupby("month")["daily_return_pct"].mean()
            best_month = monthly_avg.idxmax() if len(monthly_avg) > 0 else None
            worst_month = monthly_avg.idxmin() if len(monthly_avg) > 0 else None
        else:
            best_month = worst_month = None
        
        # Trend alignment (how many EMAs in uptrend)
        if "ema20" in df.columns and "ema50" in df.columns:
            ema_alignment = 0
            if current > df["ema20"].iloc[-1]:
                ema_alignment += 1
            if df["ema20"].iloc[-1] > df["ema50"].iloc[-1]:
                ema_alignment += 1
            if df["ema50"].iloc[-1] > df["ema200"].iloc[-1]:
                ema_alignment += 1
        else:
            ema_alignment = 0
        
        # Long-term trend (1Y+)
        if "long_term_trend" in df.columns:
            lt_trend = df["long_term_trend"].iloc[-1]
        else:
            lt_trend = 0
        
        return {
            "current": round(current, 2),
            "all_time_high": round(all_time_high, 2),
            "all_time_low": round(all_time_low, 2),
            "pct_from_low": round(pct_from_low, 1),
            "pct_from_high": round(pct_from_high, 1),
            "change_1y_pct": round(change_1y, 1),
            "ema_alignment": int(ema_alignment),  # 0-3
            "long_term_trend": int(lt_trend),      # 0-2 (0=bear, 1=neutral, 2=bull)
            "best_month": best_month,
            "worst_month": worst_month,
            "market_position": classify_market_position(current, all_time_low, all_time_high)
        }
    except Exception as e:
        return {"error": str(e)}


def classify_market_position(current, low, high):
    """Classify position in 5-year range."""
    if (current - low) < (high - low) * 0.3:
        return "Near 5-year lows (oversold territory)"
    elif (current - low) > (high - low) * 0.7:
        return "Near 5-year highs (overbought territory)"
    elif (current - low) > (high - low) * 0.5:
        return "In upper half of range (bullish)"
    else:
        return "In lower half of range (bearish)"


def summarize_analysis(tech_report: Optional[Dict], fund_report: Optional[Dict], mode: str = "both", 
                      tech_data: Optional[pd.DataFrame] = None) -> Dict:
    """
    Create a smart AI-style summary with 5-year pattern recognition.
    
    Analyzes:
    - Technical: short-term trend + 5-year patterns (support/resistance, seasonality)
    - Fundamental: long-term value & growth (PE, ROE, growth rates, 5-year trends)
    - Patterns: Market position, seasonal strength, EMA alignment
    
    Returns comprehensive recommendation with reasoning.
    """
    recommendation = "HOLD"
    reasoning = []
    
    # Get 5-year pattern analysis if data available
    pattern_analysis = {}
    if tech_data is not None:
        pattern_analysis = analyze_5year_pattern(tech_data)
    
    # ===== TECHNICAL ANALYSIS =====
    tech_score = 0
    if mode in ("technical", "both") and tech_report:
        tt = tech_report
        sig = tt.get('signal', 'HOLD')
        score = tt.get('score', 0)
        conf = tt.get('confidence', 0.5)
        
        # Map signal to score component
        if sig == 'BUY':
            tech_score = 3
            reasoning.append(f"Technical BUY signal (score={score:.2f}, confidence={conf:.1%})")
        elif sig == 'SELL':
            tech_score = -2
            reasoning.append(f"Technical SELL signal (score={score:.2f})")
        elif sig == 'SHORT':
            tech_score = -3
            reasoning.append(f"Technical SHORT signal (score={score:.2f}) - strong bearish")
        else:
            tech_score = 0
            reasoning.append(f"Technical HOLD (score={score:.2f})")
        
        # Add 5-year pattern insights
        if pattern_analysis:
            pos = pattern_analysis.get("market_position", "")
            if "oversold" in pos.lower():
                tech_score += 0.5
                reasoning.append(f"📍 {pos} - potential recovery zone")
            elif "overbought" in pos.lower():
                tech_score -= 0.3
                reasoning.append(f"📍 {pos} - watch for pullbacks")
            
            # Seasonality hint
            if pattern_analysis.get("best_month"):
                reasoning.append(f"📅 Seasonal: Typically strong in Q{(pattern_analysis['best_month']-1)//3+1}")
            
            # 1-year trend
            change_1y = pattern_analysis.get("change_1y_pct", 0)
            if change_1y > 15:
                reasoning.append(f"📈 Strong 1-year trend: +{change_1y}%")
            elif change_1y < -15:
                reasoning.append(f"📉 Weak 1-year trend: {change_1y}%")

    # ===== FUNDAMENTAL ANALYSIS =====
    fund_score = 0
    if mode in ("fundamental", "both") and fund_report:
        fr = fund_report
        
        # Get latest year data (usually year 2024/2025)
        latest = None
        if isinstance(fr, dict) and 'fundamentals' in fr:
            latest = fr['fundamentals'][0] if fr['fundamentals'] else None
        
        if latest:
            pe = latest.get('pe_ratio')
            pb = latest.get('pb_ratio')
            roe = latest.get('roe_pct')
            growth = latest.get('net_income_growth_pct')
            
            reasoning.append(f"Fundamentals (2024-Q2 2025): PE={pe}, PB={pb}, ROE={roe}%, Growth={growth}%")
            
            # Value check (PE < 8 = undervalued)
            if pe and pe < 8:
                fund_score += 1.5
                reasoning.append("✓ Undervalued (PE < 8)")
            elif pe and pe < 10:
                fund_score += 0.5
                reasoning.append("✓ Fairly valued (PE 8-10)")
            elif pe and pe > 12:
                fund_score -= 0.5
                reasoning.append("⚠ Overvalued (PE > 12)")
            
            # Quality check (ROE > 15% = good)
            if roe and roe > 15:
                fund_score += 1
                reasoning.append(f"✓ Good profitability (ROE={roe}%)")
            elif roe and roe < 10:
                fund_score -= 0.5
                reasoning.append(f"⚠ Weak profitability (ROE={roe}%)")
            
            # Growth check
            if growth and growth > 10:
                fund_score += 1
                reasoning.append(f"✓ Strong earnings growth ({growth}%)")
            elif growth and growth < 0:
                fund_score -= 1
                reasoning.append(f"⚠ Declining earnings ({growth}%)")
            
            # Trend check (5-year improvement)
            if isinstance(fr, dict) and 'fundamentals' in fr and len(fr['fundamentals']) >= 5:
                pe_5yr = fr['fundamentals'][-1].get('pe_ratio')  # 2020
                if pe and pe_5yr and pe < pe_5yr:
                    fund_score += 0.5
                    reasoning.append(f"✓ Valuation improving: PE {pe_5yr:.1f}→{pe:.1f}")
                elif pe and pe_5yr and pe > pe_5yr:
                    fund_score -= 0.3
                    reasoning.append(f"⚠ Valuation deteriorating: PE {pe_5yr:.1f}→{pe:.1f}")

    # ===== COMBINED RECOMMENDATION =====
    total_score = tech_score + fund_score
    
    if mode == "technical":
        if tech_score >= 2.5:
            recommendation = "BUY (technical)"
        elif tech_score <= -2:
            recommendation = "SELL (technical)"
        else:
            recommendation = "HOLD (technical)"
    elif mode == "fundamental":
        if fund_score >= 2:
            recommendation = "BUY (value)"
        elif fund_score <= -1:
            recommendation = "SELL (weak fundamentals)"
        else:
            recommendation = "HOLD (fundamentals)"
    else:  # mode == "both"
        if tech_score >= 2.5 and fund_score >= 1:
            recommendation = "STRONG BUY (tech + value)"
        elif tech_score >= 2.5:
            recommendation = "BUY (technical strength)"
        elif fund_score >= 2:
            recommendation = "BUY (value play)"
        elif tech_score <= -2 and fund_score <= -1:
            recommendation = "STRONG SELL"
        elif tech_score <= -2:
            recommendation = "SELL (technical weakness)"
        elif fund_score <= -1:
            recommendation = "SELL (weak fundamentals)"
        else:
            recommendation = "HOLD"

    summary = {
        "mode": mode,
        "technical_score": round(tech_score, 2),
        "fundamental_score": round(fund_score, 2),
        "total_score": round(total_score, 2),
        "recommendation": recommendation,
        "reasoning": reasoning,
        "pattern_analysis": pattern_analysis  # New: 5-year patterns
    }
    return summary


