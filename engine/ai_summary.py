from typing import Dict, Optional


def summarize_analysis(tech_report: Optional[Dict], fund_report: Optional[Dict], mode: str = "both") -> Dict:
    """Create a smart AI-style summary from technical and/or fundamental reports.

    Analyzes:
    - Technical: short-term trend from indicators (EMA, RSI, MACD, Bollinger Bands)
    - Fundamental: long-term value & growth (PE, ROE, growth rates, 5-year trends)
    
    Returns recommendation based on both angles.
    """
    recommendation = "HOLD"
    reasoning = []

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

    # ===== FUNDAMENTAL ANALYSIS =====
    fund_score = 0
    if mode in ("fundamental", "both") and fund_report:
        fr = fund_report
        
        # Get latest year data (usually year 2024)
        latest = None
        if isinstance(fr, dict) and 'fundamentals' in fr:
            latest = fr['fundamentals'][0] if fr['fundamentals'] else None
        
        if latest:
            pe = latest.get('pe_ratio')
            pb = latest.get('pb_ratio')
            roe = latest.get('roe_pct')
            growth = latest.get('net_income_growth_pct')
            
            reasoning.append(f"Fundamentals (2024): PE={pe}, PB={pb}, ROE={roe}%, Growth={growth}%")
            
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
        "reasoning": reasoning
    }
    return summary

