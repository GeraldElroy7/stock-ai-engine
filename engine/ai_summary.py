from typing import Dict, Optional


def summarize_analysis(tech_report: Optional[Dict], fund_report: Optional[Dict], mode: str = "both") -> Dict:
    """Create a short AI-style summary from technical and/or fundamental reports.

    This is a deterministic templated summarizer. Later we can plug in an LLM.
    """
    parts = []
    if mode in ("technical", "both") and tech_report:
        tt = tech_report
        parts.append(f"Technical: signal={tt.get('signal', 'N/A')}, score={tt.get('score', 'N/A')}, confidence={tt.get('confidence', 'N/A')}")
    if mode in ("fundamental", "both") and fund_report:
        fr = fund_report
        pe = fr.get('pe_ratio')
        roe = fr.get('roe_pct')
        parts.append(f"Fundamental: PE={pe if pe is not None else 'N/A'}, ROE={roe if roe is not None else 'N/A'}")

    # Simple rule-based recommendation
    recommendation = "HOLD"
    try:
        if tech_report and tech_report.get('signal') == 'BUY':
            recommendation = 'BUY'
        if tech_report and tech_report.get('signal') == 'SELL':
            recommendation = 'SELL'
        # fundamentals can influence
        if fund_report and fund_report.get('pe_ratio') is not None and fund_report.get('pe_ratio') < 8:
            if recommendation == 'HOLD':
                recommendation = 'BUY (value)'
    except Exception:
        pass

    summary = {
        "summary_text": " | ".join(parts) + f" -> Recommendation: {recommendation}",
        "recommendation": recommendation
    }
    return summary
