"""
Enhanced API Endpoints for B2C Platform
Stock AI Engine - User-Focused Information API
Author: Stock AI Engine Team
Date: January 1, 2026
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from data.fetcher import fetch_eod
from data.enhanced_fundamentals import (
    fetch_fundamental_data,
    calculate_fundamental_score,
    format_large_number,
    get_financial_statements
)
from indicators.technical import add_indicators
from engine.decision import decision_engine
from config import SUPPORTED_STOCKS, USER_INPUT_PARAMS

# Security
security = HTTPBearer()

# ===== ENUMS FOR USER INPUT =====

class TradingStyle(str, Enum):
    """Trading style options for users"""
    scalper = "scalper"
    day_trader = "day_trader"
    swing_trader = "swing_trader"
    position_trader = "position_trader"
    long_term_investor = "long_term_investor"


class RiskLevel(str, Enum):
    """Risk tolerance levels"""
    conservative = "conservative"
    moderate = "moderate"
    aggressive = "aggressive"
    very_aggressive = "very_aggressive"


class InvestmentGoal(str, Enum):
    """Investment objectives"""
    capital_preservation = "capital_preservation"
    income_generation = "income_generation"
    balanced_growth = "balanced_growth"
    capital_appreciation = "capital_appreciation"
    aggressive_growth = "aggressive_growth"


class TimeHorizon(str, Enum):
    """Investment time horizon"""
    short_term = "short_term"  # < 6 months
    medium_term = "medium_term"  # 6 months - 2 years
    long_term = "long_term"  # > 2 years


# ===== PYDANTIC MODELS =====

class UserPreferences(BaseModel):
    """User preferences untuk personalisasi analisis"""
    trading_style: TradingStyle = Field(
        default=TradingStyle.swing_trader,
        description="Gaya trading user (scalper, day_trader, swing_trader, position_trader, long_term_investor)"
    )
    risk_level: RiskLevel = Field(
        default=RiskLevel.moderate,
        description="Tingkat toleransi risiko (conservative, moderate, aggressive, very_aggressive)"
    )
    capital_size: float = Field(
        default=10000000,
        description="Ukuran modal dalam IDR (contoh: 10000000 untuk 10 juta)",
        ge=1000000
    )
    investment_goal: InvestmentGoal = Field(
        default=InvestmentGoal.balanced_growth,
        description="Tujuan investasi"
    )
    sector_preference: List[str] = Field(
        default=[],
        description="Sektor yang disukai (Banking, Technology, Mining, dll)"
    )
    exclude_sectors: List[str] = Field(
        default=[],
        description="Sektor yang dihindari"
    )
    min_confidence_level: float = Field(
        default=60.0,
        description="Minimum confidence level untuk signal (0-100)",
        ge=0,
        le=100
    )
    enable_short_signals: bool = Field(
        default=False,
        description="Aktifkan sinyal SHORT untuk market bearish"
    )
    time_horizon: TimeHorizon = Field(
        default=TimeHorizon.medium_term,
        description="Horizon waktu investasi"
    )


class StockInfoRequest(BaseModel):
    """Request untuk mendapatkan informasi lengkap saham"""
    ticker: str = Field(
        ...,
        description="Kode saham (contoh: BBCA, BBRI, TLKM)",
        example="BBCA"
    )
    user_preferences: Optional[UserPreferences] = Field(
        default=None,
        description="Preferensi user untuk personalisasi analisis"
    )
    include_fundamentals: bool = Field(
        default=True,
        description="Sertakan analisis fundamental"
    )
    include_technical: bool = Field(
        default=True,
        description="Sertakan analisis teknikal"
    )
    include_ai_summary: bool = Field(
        default=True,
        description="Sertakan AI-generated summary dan rekomendasi"
    )


class WebhookRequest(BaseModel):
    """Request untuk setup webhook notification"""
    webhook_url: str = Field(
        ...,
        description="URL endpoint untuk menerima notifications",
        example="https://your-app.com/api/webhook"
    )
    tickers: List[str] = Field(
        ...,
        description="List ticker yang di-monitor",
        example=["BBCA", "BBRI", "TLKM"]
    )
    alert_conditions: List[str] = Field(
        default=["signal_change", "price_alert"],
        description="Kondisi yang trigger notifikasi"
    )
    min_confidence: float = Field(
        default=70.0,
        description="Minimum confidence untuk trigger alert",
        ge=0,
        le=100
    )


# ===== RESPONSE MODELS =====

class ComprehensiveStockInfo(BaseModel):
    """Complete stock information response"""
    ticker: str
    company_info: Dict[str, Any]
    current_price: float
    price_change: Dict[str, Any]
    technical_analysis: Optional[Dict[str, Any]]
    fundamental_analysis: Optional[Dict[str, Any]]
    fundamental_score: Optional[Dict[str, Any]]
    trading_signal: Dict[str, Any]
    ai_recommendation: Optional[Dict[str, Any]]
    risk_assessment: Dict[str, Any]
    personalized_insights: Optional[Dict[str, Any]]
    metadata: Dict[str, Any]


# ===== HELPER FUNCTIONS =====

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token (placeholder - implement with real JWT)"""
    # For now, accept any token
    # TODO: Implement proper JWT verification
    return {"user_id": "demo_user", "email": "demo@example.com"}


def calculate_risk_assessment(
    technical: Dict[str, Any],
    fundamentals: Optional[Dict[str, Any]],
    user_prefs: Optional[UserPreferences]
) -> Dict[str, Any]:
    """Calculate risk assessment berdasarkan data teknikal dan fundamental"""
    
    risk_score = 50  # Neutral starting point
    risk_factors = []
    
    # Technical volatility
    if technical and "indicators" in technical:
        indicators = technical["indicators"]
        atr = indicators.get("atr")
        volatility = indicators.get("volatility", 0)
        
        if volatility > 0.03:  # High volatility
            risk_score += 15
            risk_factors.append("High price volatility detected")
        elif volatility < 0.01:  # Low volatility
            risk_score -= 10
            risk_factors.append("Low volatility - stable price action")
    
    # Fundamental health
    if fundamentals:
        health = fundamentals.get("financial_health", {})
        debt_to_equity = health.get("debt_to_equity")
        
        if debt_to_equity and debt_to_equity > 2.0:
            risk_score += 10
            risk_factors.append(f"High debt-to-equity ratio: {debt_to_equity:.2f}")
        elif debt_to_equity and debt_to_equity < 0.5:
            risk_score -= 10
            risk_factors.append("Low debt levels")
    
    # User risk tolerance
    if user_prefs:
        if user_prefs.risk_level == RiskLevel.conservative:
            risk_threshold = 40
        elif user_prefs.risk_level == RiskLevel.moderate:
            risk_threshold = 60
        elif user_prefs.risk_level == RiskLevel.aggressive:
            risk_threshold = 80
        else:  # very_aggressive
            risk_threshold = 100
    else:
        risk_threshold = 60
    
    # Determine risk level
    if risk_score <= 30:
        risk_level = "LOW"
        risk_color = "green"
    elif risk_score <= 50:
        risk_level = "MODERATE"
        risk_color = "yellow"
    elif risk_score <= 70:
        risk_level = "HIGH"
        risk_color = "orange"
    else:
        risk_level = "VERY HIGH"
        risk_color = "red"
    
    suitable = risk_score <= risk_threshold
    
    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_color": risk_color,
        "suitable_for_user": suitable,
        "risk_factors": risk_factors,
        "recommendation": "Sesuai dengan profil risiko Anda" if suitable else "Melebihi toleransi risiko Anda"
    }


def generate_ai_recommendation(
    ticker: str,
    technical: Dict[str, Any],
    fundamentals: Optional[Dict[str, Any]],
    fundamental_score: Optional[Dict[str, Any]],
    user_prefs: Optional[UserPreferences]
) -> Dict[str, Any]:
    """Generate AI-powered recommendation"""
    
    # Extract key data
    signal = technical.get("signal", "HOLD")
    confidence = technical.get("confidence", 50)
    score = technical.get("score", 0)
    
    # Build recommendation text
    recommendation_parts = []
    
    # Main signal
    if signal == "BUY" and confidence >= 70:
        recommendation_parts.append(f"✅ **STRONG BUY** signal dengan confidence {confidence:.1f}%.")
    elif signal == "BUY":
        recommendation_parts.append(f"📈 **BUY** signal dengan confidence {confidence:.1f}%.")
    elif signal == "SELL" and confidence >= 70:
        recommendation_parts.append(f"❌ **STRONG SELL** signal dengan confidence {confidence:.1f}%.")
    elif signal == "SELL":
        recommendation_parts.append(f"📉 **SELL** signal dengan confidence {confidence:.1f}%.")
    elif signal == "SHORT":
        recommendation_parts.append(f"⚠️ **SHORT** signal - market bearish dengan confidence {confidence:.1f}%.")
    else:
        recommendation_parts.append(f"⏸️ **HOLD** - tunggu konfirmasi lebih lanjut.")
    
    # Fundamental insight
    if fundamental_score:
        fund_rating = fundamental_score.get("rating", "N/A")
        fund_pct = fundamental_score.get("percentage", 0)
        
        if fund_rating in ["EXCELLENT", "GOOD"]:
            recommendation_parts.append(f"Fundamental rating: **{fund_rating}** ({fund_pct:.0f}/100) - perusahaan solid.")
        elif fund_rating == "FAIR":
            recommendation_parts.append(f"Fundamental rating: **{fund_rating}** - perlu evaluasi lebih lanjut.")
        else:
            recommendation_parts.append(f"⚠️ Fundamental rating: **{fund_rating}** - waspadai risiko fundamental.")
    
    # User-specific advice
    if user_prefs:
        if user_prefs.trading_style == TradingStyle.scalper:
            recommendation_parts.append("Untuk scalping: perhatikan volume dan spread yang tight.")
        elif user_prefs.trading_style == TradingStyle.swing_trader:
            recommendation_parts.append("Untuk swing trading: tunggu konfirmasi breakout atau breakdown.")
        elif user_prefs.trading_style == TradingStyle.long_term_investor:
            recommendation_parts.append("Untuk investor jangka panjang: fokus pada fundamental dan dividend yield.")
    
    # Action items
    action_items = []
    if signal == "BUY":
        action_items.append("Monitor entry point di support level")
        action_items.append("Set stop loss di bawah support terdekat")
        action_items.append("Target profit di resistance level berikutnya")
    elif signal == "SELL":
        action_items.append("Pertimbangkan take profit jika ada posisi")
        action_items.append("Hindari new entry untuk saat ini")
        action_items.append("Monitor untuk potential reversal")
    else:  # HOLD
        action_items.append("Tunggu signal lebih jelas")
        action_items.append("Monitor pergerakan harga dan volume")
        action_items.append("Siapkan strategi untuk skenario bullish & bearish")
    
    return {
        "summary": " ".join(recommendation_parts),
        "action_items": action_items,
        "confidence_level": confidence,
        "signal": signal,
        "generated_at": datetime.now().isoformat()
    }


def generate_personalized_insights(
    ticker: str,
    company_info: Dict[str, Any],
    technical: Dict[str, Any],
    fundamentals: Optional[Dict[str, Any]],
    user_prefs: Optional[UserPreferences]
) -> Optional[Dict[str, Any]]:
    """Generate personalized insights based on user preferences"""
    
    if not user_prefs:
        return None
    
    insights = []
    
    # Sector preference match
    sector = company_info.get("sector", "N/A")
    if sector in user_prefs.sector_preference:
        insights.append(f"✅ Saham ini dari sektor preferensi Anda: {sector}")
    elif sector in user_prefs.exclude_sectors:
        insights.append(f"⚠️ Saham ini dari sektor yang Anda hindari: {sector}")
    
    # Capital size consideration
    if fundamentals:
        price = fundamentals.get("price_info", {}).get("current_price", 0)
        if price > 0:
            shares_can_buy = int(user_prefs.capital_size / price)
            position_value = shares_can_buy * price
            insights.append(f"Dengan modal Rp {user_prefs.capital_size:,.0f}, Anda bisa beli {shares_can_buy:,} lembar saham (Rp {position_value:,.0f})")
    
    # Risk level match
    confidence = technical.get("confidence", 0)
    if confidence < user_prefs.min_confidence_level:
        insights.append(f"⚠️ Confidence {confidence:.1f}% di bawah minimum Anda ({user_prefs.min_confidence_level:.0f}%)")
    else:
        insights.append(f"✅ Confidence {confidence:.1f}% memenuhi kriteria minimum Anda")
    
    # Investment goal alignment
    if fundamentals and user_prefs.investment_goal == InvestmentGoal.income_generation:
        div_yield = fundamentals.get("dividend", {}).get("dividend_yield")
        if div_yield:
            insights.append(f"Dividend yield: {div_yield*100:.2f}% - {'cocok' if div_yield > 0.03 else 'rendah'} untuk income generation")
    
    # Time horizon
    if user_prefs.time_horizon == TimeHorizon.short_term:
        insights.append("⏱️ Untuk trading jangka pendek: monitor daily price action dan volume")
    elif user_prefs.time_horizon == TimeHorizon.long_term:
        insights.append("📅 Untuk investasi jangka panjang: fokus pada pertumbuhan fundamental dan dividend")
    
    return {
        "insights": insights,
        "personalized": True,
        "user_trading_style": user_prefs.trading_style,
        "user_risk_level": user_prefs.risk_level
    }


# ===== API ROUTES =====

def setup_b2c_routes(app: FastAPI):
    """Setup B2C-focused API routes"""
    
    @app.post("/api/v2/stock/info", response_model=ComprehensiveStockInfo)
    async def get_comprehensive_stock_info(
        request: StockInfoRequest,
        # user: dict = Depends(verify_token)  # Uncomment when auth is ready
    ):
        """
        **Get Complete Stock Information** 🎯
        
        Endpoint ini memberikan informasi LENGKAP tentang saham yang user minta:
        - Company profile & info
        - Real-time price data
        - Technical analysis dengan 10-year data
        - Fundamental analysis lengkap
        - AI-generated recommendation
        - Risk assessment
        - Personalized insights berdasarkan user preferences
        
        **Example Request:**
        ```json
        {
          "ticker": "BBCA",
          "user_preferences": {
            "trading_style": "swing_trader",
            "risk_level": "moderate",
            "capital_size": 50000000,
            "investment_goal": "balanced_growth",
            "min_confidence_level": 70.0
          },
          "include_fundamentals": true,
          "include_technical": true,
          "include_ai_summary": true
        }
        ```
        
        **Returns:** Complete stock information dengan semua data yang dibutuhkan user
        """
        try:
            ticker = request.ticker.upper()
            
            # Validate ticker
            if ticker not in SUPPORTED_STOCKS:
                raise HTTPException(
                    status_code=404,
                    detail=f"Ticker {ticker} tidak ditemukan. Gunakan /api/v2/stocks/list untuk melihat ticker yang tersedia."
                )
            
            stock_config = SUPPORTED_STOCKS[ticker]
            
            # Initialize response data
            response_data = {
                "ticker": ticker,
                "company_info": {
                    "name": stock_config.get("name", "N/A"),
                    "sector": stock_config.get("sector", "N/A"),
                    "is_us": stock_config.get("is_us", False)
                },
                "current_price": 0,
                "price_change": {},
                "technical_analysis": None,
                "fundamental_analysis": None,
                "fundamental_score": None,
                "trading_signal": {},
                "ai_recommendation": None,
                "risk_assessment": {},
                "personalized_insights": None,
                "metadata": {
                    "data_source": "yfinance + Stock AI Engine",
                    "generated_at": datetime.now().isoformat(),
                    "lookback_period": "10 years"
                }
            }
            
            # Fetch technical analysis
            if request.include_technical:
                print(f"📊 Fetching technical data for {ticker}...")
                df = fetch_eod(ticker, use_5y=False, is_us=stock_config.get("is_us", False))
                
                if df is not None and not df.empty:
                    df_with_indicators = add_indicators(df)
                    technical_decision = decision_engine(df_with_indicators)
                    
                    response_data["technical_analysis"] = technical_decision
                    response_data["trading_signal"] = {
                        "signal": technical_decision.get("signal", "HOLD"),
                        "score": technical_decision.get("score", 0),
                        "confidence": technical_decision.get("confidence", 50),
                        "reasons": technical_decision.get("reasons", [])
                    }
                    
                    # Current price from technical data
                    if len(df) > 0:
                        current_price = float(df['Close'].iloc[-1])
                        prev_close = float(df['Close'].iloc[-2]) if len(df) > 1 else current_price
                        
                        response_data["current_price"] = current_price
                        response_data["price_change"] = {
                            "amount": current_price - prev_close,
                            "percentage": ((current_price - prev_close) / prev_close * 100) if prev_close > 0 else 0,
                            "previous_close": prev_close
                        }
            
            # Fetch fundamental analysis
            if request.include_fundamentals:
                print(f"📈 Fetching fundamental data for {ticker}...")
                fundamentals = fetch_fundamental_data(ticker)
                
                if fundamentals:
                    response_data["fundamental_analysis"] = fundamentals
                    
                    # Calculate fundamental score
                    fund_score = calculate_fundamental_score(fundamentals)
                    response_data["fundamental_score"] = fund_score
                    
                    # Update price if not from technical
                    if response_data["current_price"] == 0:
                        price_info = fundamentals.get("price_info", {})
                        response_data["current_price"] = price_info.get("current_price", 0)
                        response_data["price_change"] = {
                            "amount": price_info.get("current_price", 0) - price_info.get("previous_close", 0),
                            "percentage": ((price_info.get("current_price", 0) - price_info.get("previous_close", 0)) / price_info.get("previous_close", 1) * 100) if price_info.get("previous_close", 0) > 0 else 0,
                            "previous_close": price_info.get("previous_close", 0)
                        }
            
            # Calculate risk assessment
            if response_data["technical_analysis"]:
                response_data["risk_assessment"] = calculate_risk_assessment(
                    response_data["technical_analysis"],
                    response_data["fundamental_analysis"],
                    request.user_preferences
                )
            
            # Generate AI recommendation
            if request.include_ai_summary and response_data["technical_analysis"]:
                response_data["ai_recommendation"] = generate_ai_recommendation(
                    ticker,
                    response_data["technical_analysis"],
                    response_data["fundamental_analysis"],
                    response_data["fundamental_score"],
                    request.user_preferences
                )
            
            # Generate personalized insights
            if request.user_preferences and response_data["technical_analysis"]:
                response_data["personalized_insights"] = generate_personalized_insights(
                    ticker,
                    response_data["company_info"],
                    response_data["technical_analysis"],
                    response_data["fundamental_analysis"],
                    request.user_preferences
                )
            
            return response_data
            
        except HTTPException:
            raise
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=500,
                detail=f"Error processing request: {str(e)}"
            )
    
    
    @app.get("/api/v2/stocks/list")
    async def get_supported_stocks():
        """
        **Get List of Supported Stocks** 📋
        
        Returns list of all supported stocks dengan info lengkap
        
        **Returns:** List of 120+ Indonesian stocks
        """
        stocks_list = []
        for ticker, info in SUPPORTED_STOCKS.items():
            stocks_list.append({
                "ticker": ticker,
                "name": info.get("name", "N/A"),
                "sector": info.get("sector", "N/A"),
                "is_us": info.get("is_us", False)
            })
        
        return {
            "total": len(stocks_list),
            "stocks": stocks_list,
            "sectors": list(set([s["sector"] for s in stocks_list]))
        }
    
    
    @app.get("/api/v2/user/parameters")
    async def get_user_input_parameters():
        """
        **Get Available User Input Parameters** ⚙️
        
        Returns semua parameter yang bisa diinput oleh user untuk personalisasi analisis.
        Berguna untuk UI form generation.
        
        **Returns:** Complete list of user input parameters dengan options dan descriptions
        """
        return {
            "parameters": USER_INPUT_PARAMS,
            "trading_styles": [style.value for style in TradingStyle],
            "risk_levels": [level.value for level in RiskLevel],
            "investment_goals": [goal.value for goal in InvestmentGoal],
            "time_horizons": [horizon.value for horizon in TimeHorizon],
            "description": "Use these parameters to personalize your stock analysis and recommendations"
        }
    
    
    @app.post("/api/v2/webhook/register")
    async def register_webhook(
        request: WebhookRequest,
        # user: dict = Depends(verify_token)  # Uncomment when auth is ready
    ):
        """
        **Register Webhook for Signal Alerts** 🔔
        
        Setup webhook untuk receive real-time notifications ketika ada signal changes
        atau price alerts untuk ticker yang di-monitor.
        
        **Example Request:**
        ```json
        {
          "webhook_url": "https://your-app.com/api/webhook",
          "tickers": ["BBCA", "BBRI", "TLKM"],
          "alert_conditions": ["signal_change", "price_alert"],
          "min_confidence": 70.0
        }
        ```
        
        **Webhook Payload Format:**
        ```json
        {
          "ticker": "BBCA",
          "event": "signal_change",
          "old_signal": "HOLD",
          "new_signal": "BUY",
          "confidence": 78.5,
          "timestamp": "2026-01-01T10:30:00"
        }
        ```
        """
        # TODO: Implement webhook registration in database
        # For now, return success response
        
        return {
            "status": "success",
            "message": "Webhook registered successfully",
            "webhook_id": f"wh_{datetime.now().timestamp()}",
            "webhook_url": request.webhook_url,
            "monitored_tickers": request.tickers,
            "alert_conditions": request.alert_conditions,
            "min_confidence": request.min_confidence,
            "created_at": datetime.now().isoformat(),
            "note": "Webhook implementation in progress - notifications will be sent to your endpoint when conditions are met"
        }
    
    
    return app


if __name__ == "__main__":
    print("B2C API Endpoints Module")
    print("Import this module in main.py to activate B2C routes")
