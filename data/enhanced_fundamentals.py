"""
Enhanced Fundamental Data Fetcher
Mengambil data fundamental lengkap untuk analisis mendalam
Author: Stock AI Engine Team
Date: January 1, 2026
"""

import yfinance as yf
import pandas as pd
from typing import Dict, Optional, Any
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

def fetch_fundamental_data(ticker: str) -> Optional[Dict[str, Any]]:
    """
    Fetch comprehensive fundamental data dari yfinance
    
    Args:
        ticker: Stock symbol (e.g., "BBCA" for IDX stocks)
    
    Returns:
        Dict dengan data fundamental lengkap atau None jika gagal
    """
    try:
        # Add .JK suffix for Indonesian stocks
        symbol = f"{ticker}.JK" if not ticker.endswith('.JK') else ticker
        
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # Check if data is valid
        if not info or info.get("regularMarketPrice") is None:
            print(f"⚠️ No fundamental data available for {ticker}")
            return None
        
        # Extract comprehensive fundamental metrics
        fundamentals = {
            # === COMPANY INFO ===
            "company_info": {
                "ticker": ticker,
                "company_name": info.get("longName", info.get("shortName", "N/A")),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "website": info.get("website", "N/A"),
                "description": info.get("longBusinessSummary", "N/A")[:500] + "..." if info.get("longBusinessSummary") else "N/A",
                "employees": info.get("fullTimeEmployees", 0),
                "country": info.get("country", "Indonesia"),
                "city": info.get("city", "N/A"),
            },
            
            # === MARKET DATA ===
            "market_data": {
                "market_cap": info.get("marketCap", 0),
                "enterprise_value": info.get("enterpriseValue", 0),
                "shares_outstanding": info.get("sharesOutstanding", 0),
                "float_shares": info.get("floatShares", 0),
                "shares_short": info.get("sharesShort", 0),
                "short_ratio": info.get("shortRatio", 0),
                "held_percent_insiders": info.get("heldPercentInsiders", 0),
                "held_percent_institutions": info.get("heldPercentInstitutions", 0),
            },
            
            # === VALUATION RATIOS ===
            "valuation": {
                "pe_ratio": info.get("trailingPE", None),
                "forward_pe": info.get("forwardPE", None),
                "peg_ratio": info.get("pegRatio", None),
                "pb_ratio": info.get("priceToBook", None),
                "ps_ratio": info.get("priceToSalesTrailing12Months", None),
                "ev_to_revenue": info.get("enterpriseToRevenue", None),
                "ev_to_ebitda": info.get("enterpriseToEbitda", None),
            },
            
            # === PROFITABILITY METRICS ===
            "profitability": {
                "profit_margin": info.get("profitMargins", None),
                "operating_margin": info.get("operatingMargins", None),
                "gross_margin": info.get("grossMargins", None),
                "ebitda_margin": info.get("ebitdaMargins", None),
                "roe": info.get("returnOnEquity", None),
                "roa": info.get("returnOnAssets", None),
            },
            
            # === FINANCIAL HEALTH ===
            "financial_health": {
                "total_revenue": info.get("totalRevenue", 0),
                "revenue_per_share": info.get("revenuePerShare", None),
                "revenue_growth": info.get("revenueGrowth", None),
                "earnings_growth": info.get("earningsGrowth", None),
                "quarterly_revenue_growth": info.get("quarterlyRevenueGrowth", None),
                "quarterly_earnings_growth": info.get("quarterlyEarningsGrowth", None),
                "total_debt": info.get("totalDebt", 0),
                "total_cash": info.get("totalCash", 0),
                "debt_to_equity": info.get("debtToEquity", None),
                "current_ratio": info.get("currentRatio", None),
                "quick_ratio": info.get("quickRatio", None),
                "free_cashflow": info.get("freeCashflow", 0),
                "operating_cashflow": info.get("operatingCashflow", 0),
            },
            
            # === PER SHARE DATA ===
            "per_share": {
                "eps_trailing": info.get("trailingEps", None),
                "eps_forward": info.get("forwardEps", None),
                "book_value": info.get("bookValue", None),
                "revenue_per_share": info.get("revenuePerShare", None),
                "cashflow_per_share": info.get("operatingCashflow", 0) / info.get("sharesOutstanding", 1) if info.get("sharesOutstanding") else None,
            },
            
            # === DIVIDEND INFO ===
            "dividend": {
                "dividend_rate": info.get("dividendRate", None),
                "dividend_yield": info.get("dividendYield", None),
                "payout_ratio": info.get("payoutRatio", None),
                "ex_dividend_date": datetime.fromtimestamp(info.get("exDividendDate", 0)).strftime("%Y-%m-%d") if info.get("exDividendDate") else None,
                "five_year_avg_dividend_yield": info.get("fiveYearAvgDividendYield", None),
            },
            
            # === PRICE INFO ===
            "price_info": {
                "current_price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
                "previous_close": info.get("previousClose", 0),
                "open": info.get("open", 0),
                "day_low": info.get("dayLow", 0),
                "day_high": info.get("dayHigh", 0),
                "fifty_day_average": info.get("fiftyDayAverage", None),
                "two_hundred_day_average": info.get("twoHundredDayAverage", None),
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh", None),
                "fifty_two_week_low": info.get("fiftyTwoWeekLow", None),
                "fifty_two_week_change": info.get("52WeekChange", None),
            },
            
            # === TRADING INFO ===
            "trading": {
                "volume": info.get("volume", 0),
                "avg_volume": info.get("averageVolume", 0),
                "avg_volume_10days": info.get("averageVolume10days", 0),
                "beta": info.get("beta", None),
                "bid": info.get("bid", 0),
                "ask": info.get("ask", 0),
                "bid_size": info.get("bidSize", 0),
                "ask_size": info.get("askSize", 0),
            },
            
            # === ANALYST RECOMMENDATIONS ===
            "analyst": {
                "recommendation": info.get("recommendationKey", "N/A"),
                "recommendation_mean": info.get("recommendationMean", None),
                "target_mean_price": info.get("targetMeanPrice", None),
                "target_median_price": info.get("targetMedianPrice", None),
                "target_high_price": info.get("targetHighPrice", None),
                "target_low_price": info.get("targetLowPrice", None),
                "number_of_analyst_opinions": info.get("numberOfAnalystOpinions", 0),
            },
            
            # === METADATA ===
            "metadata": {
                "data_source": "yfinance",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "currency": info.get("currency", "IDR"),
                "exchange": info.get("exchange", "JKT"),
            }
        }
        
        return fundamentals
        
    except Exception as e:
        print(f"❌ Error fetching fundamentals for {ticker}: {str(e)}")
        return None


def get_financial_statements(ticker: str) -> Optional[Dict[str, pd.DataFrame]]:
    """
    Fetch financial statements (Income Statement, Balance Sheet, Cash Flow)
    
    Args:
        ticker: Stock symbol
    
    Returns:
        Dict dengan DataFrames untuk setiap statement atau None jika gagal
    """
    try:
        symbol = f"{ticker}.JK" if not ticker.endswith('.JK') else ticker
        stock = yf.Ticker(symbol)
        
        statements = {
            "income_statement": stock.financials,
            "balance_sheet": stock.balance_sheet,
            "cash_flow": stock.cashflow,
            "quarterly_financials": stock.quarterly_financials,
            "quarterly_balance_sheet": stock.quarterly_balance_sheet,
            "quarterly_cashflow": stock.quarterly_cashflow,
        }
        
        # Check if we got valid data
        if statements["income_statement"] is None or statements["income_statement"].empty:
            return None
        
        return statements
        
    except Exception as e:
        print(f"❌ Error fetching statements for {ticker}: {str(e)}")
        return None


def format_large_number(num: float, currency: str = "IDR") -> str:
    """Format large numbers untuk display yang user-friendly"""
    if num is None:
        return "N/A"
    
    if num >= 1_000_000_000_000:  # Triliun
        return f"{currency} {num/1_000_000_000_000:.2f}T"
    elif num >= 1_000_000_000:  # Miliar
        return f"{currency} {num/1_000_000_000:.2f}B"
    elif num >= 1_000_000:  # Juta
        return f"{currency} {num/1_000_000:.2f}M"
    elif num >= 1_000:  # Ribu
        return f"{currency} {num/1_000:.2f}K"
    else:
        return f"{currency} {num:.2f}"


def calculate_fundamental_score(fundamentals: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate fundamental score berdasarkan metrics penting
    
    Returns:
        Dict dengan score dan interpretation
    """
    if not fundamentals:
        return {"score": 0, "rating": "N/A", "strengths": [], "weaknesses": []}
    
    score = 0
    max_score = 100
    strengths = []
    weaknesses = []
    
    # === VALUATION (20 points) ===
    valuation = fundamentals.get("valuation", {})
    pe = valuation.get("pe_ratio")
    pb = valuation.get("pb_ratio")
    
    if pe and 0 < pe < 15:
        score += 10
        strengths.append(f"PE Ratio attractive ({pe:.2f})")
    elif pe and pe > 25:
        weaknesses.append(f"PE Ratio tinggi ({pe:.2f})")
    
    if pb and 0 < pb < 2:
        score += 10
        strengths.append(f"PB Ratio good ({pb:.2f})")
    elif pb and pb > 3:
        weaknesses.append(f"PB Ratio tinggi ({pb:.2f})")
    
    # === PROFITABILITY (30 points) ===
    profitability = fundamentals.get("profitability", {})
    roe = profitability.get("roe")
    profit_margin = profitability.get("profit_margin")
    
    if roe and roe > 0.15:
        score += 15
        strengths.append(f"ROE excellent ({roe*100:.1f}%)")
    elif roe and roe < 0.05:
        weaknesses.append(f"ROE rendah ({roe*100:.1f}%)")
    
    if profit_margin and profit_margin > 0.10:
        score += 15
        strengths.append(f"Profit margin strong ({profit_margin*100:.1f}%)")
    elif profit_margin and profit_margin < 0.05:
        weaknesses.append(f"Profit margin lemah ({profit_margin*100:.1f}%)")
    
    # === FINANCIAL HEALTH (25 points) ===
    health = fundamentals.get("financial_health", {})
    debt_to_equity = health.get("debt_to_equity")
    current_ratio = health.get("current_ratio")
    revenue_growth = health.get("revenue_growth")
    
    if debt_to_equity is not None and debt_to_equity < 1.0:
        score += 10
        strengths.append(f"Debt manageable (D/E: {debt_to_equity:.2f})")
    elif debt_to_equity and debt_to_equity > 2.0:
        weaknesses.append(f"Debt tinggi (D/E: {debt_to_equity:.2f})")
    
    if current_ratio and current_ratio > 1.5:
        score += 8
        strengths.append(f"Liquidity strong (CR: {current_ratio:.2f})")
    elif current_ratio and current_ratio < 1.0:
        weaknesses.append(f"Liquidity concerns (CR: {current_ratio:.2f})")
    
    if revenue_growth and revenue_growth > 0.10:
        score += 7
        strengths.append(f"Revenue growing ({revenue_growth*100:.1f}%)")
    elif revenue_growth and revenue_growth < 0:
        weaknesses.append(f"Revenue declining ({revenue_growth*100:.1f}%)")
    
    # === DIVIDEND (15 points) ===
    dividend = fundamentals.get("dividend", {})
    dividend_yield = dividend.get("dividend_yield")
    payout_ratio = dividend.get("payout_ratio")
    
    if dividend_yield and dividend_yield > 0.03:
        score += 10
        strengths.append(f"Dividend yield good ({dividend_yield*100:.1f}%)")
    
    if payout_ratio and 0.3 < payout_ratio < 0.7:
        score += 5
        strengths.append(f"Payout sustainable ({payout_ratio*100:.1f}%)")
    
    # === MOMENTUM (10 points) ===
    price_info = fundamentals.get("price_info", {})
    current = price_info.get("current_price", 0)
    ma_50 = price_info.get("fifty_day_average")
    ma_200 = price_info.get("two_hundred_day_average")
    
    if ma_50 and ma_200 and current > ma_50 > ma_200:
        score += 10
        strengths.append("Price momentum positive (above MAs)")
    elif ma_200 and current < ma_200:
        weaknesses.append("Price below 200-day MA")
    
    # Determine rating
    if score >= 80:
        rating = "EXCELLENT"
    elif score >= 60:
        rating = "GOOD"
    elif score >= 40:
        rating = "FAIR"
    elif score >= 20:
        rating = "WEAK"
    else:
        rating = "POOR"
    
    return {
        "score": score,
        "max_score": max_score,
        "percentage": (score / max_score) * 100,
        "rating": rating,
        "strengths": strengths[:5],  # Top 5
        "weaknesses": weaknesses[:5],  # Top 5
    }


if __name__ == "__main__":
    # Test the module
    print("Testing Enhanced Fundamentals Fetcher...\n")
    
    test_tickers = ["BBCA", "BBRI", "TLKM"]
    
    for ticker in test_tickers:
        print(f"\n{'='*60}")
        print(f"Testing: {ticker}")
        print(f"{'='*60}")
        
        fundamentals = fetch_fundamental_data(ticker)
        if fundamentals:
            print(f"✅ Company: {fundamentals['company_info']['company_name']}")
            print(f"✅ Sector: {fundamentals['company_info']['sector']}")
            print(f"✅ Market Cap: {format_large_number(fundamentals['market_data']['market_cap'])}")
            
            score_data = calculate_fundamental_score(fundamentals)
            print(f"\n📊 Fundamental Score: {score_data['score']}/{score_data['max_score']} ({score_data['percentage']:.1f}%)")
            print(f"📈 Rating: {score_data['rating']}")
            
            if score_data['strengths']:
                print(f"\n💪 Strengths:")
                for s in score_data['strengths']:
                    print(f"  - {s}")
            
            if score_data['weaknesses']:
                print(f"\n⚠️ Weaknesses:")
                for w in score_data['weaknesses']:
                    print(f"  - {w}")
        else:
            print(f"❌ Failed to fetch data for {ticker}")
