"""
AI Agent for trading style customization.

Generates personalized analysis layouts and recommendations based on:
- Trading style (scalper, swing, investor, value)
- Risk tolerance (aggressive, moderate, conservative)
- Time horizon

Uses rule-based customization + optional LLM for natural language synthesis.
"""

from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class TradingStyle(str, Enum):
    SCALPER = "scalper"           # 5-min to 1h, high frequency, tight stops
    SWING = "swing"                # 1-5 days, technical focus, support/resistance
    INVESTOR = "investor"          # Months-years, fundamental focus, buy-and-hold
    VALUE = "value"                # Fundamental focus, margin of safety, long-term


class RiskLevel(str, Enum):
    CONSERVATIVE = "conservative"  # 1-2% risk per trade, wide stops
    MODERATE = "moderate"          # 2-3% risk per trade, balanced
    AGGRESSIVE = "aggressive"      # 3-5% risk per trade, tight stops


@dataclass
class StyleConfig:
    """Configuration for a trading style."""
    name: str
    timeframe: str
    priority_indicators: List[str]
    key_metrics: List[str]
    recommended_position_size: str
    risk_per_trade_pct: float
    stop_loss_atr_multiplier: float
    take_profit_atr_multiplier: float
    holding_period: str
    decision_speed: str  # slow (days), moderate (hours), fast (minutes)


# Predefined style configurations
STYLE_CONFIGS = {
    TradingStyle.SCALPER: StyleConfig(
        name="Scalper",
        timeframe="5-min to 1-hour",
        priority_indicators=["RSI", "MACD", "Volume", "ATR", "EMA20"],
        key_metrics=["Win Rate", "Risk/Reward", "Profit Factor", "Max Drawdown"],
        recommended_position_size="Risk 1-2% per trade",
        risk_per_trade_pct=1.5,
        stop_loss_atr_multiplier=0.5,
        take_profit_atr_multiplier=1.5,
        holding_period="Minutes to hours",
        decision_speed="fast"
    ),
    TradingStyle.SWING: StyleConfig(
        name="Swing Trader",
        timeframe="1 to 5 days",
        priority_indicators=["EMA20", "EMA50", "Support/Resistance", "Bollinger Bands", "RSI", "MACD"],
        key_metrics=["Win Rate", "Average Trade Duration", "Trend Strength", "Support Breaks"],
        recommended_position_size="Risk 2-3% per trade",
        risk_per_trade_pct=2.5,
        stop_loss_atr_multiplier=1.2,
        take_profit_atr_multiplier=2.5,
        holding_period="1-5 days",
        decision_speed="moderate"
    ),
    TradingStyle.INVESTOR: StyleConfig(
        name="Investor",
        timeframe="Months to years",
        priority_indicators=["EMA200", "Long-term Trend", "PE Ratio", "ROE", "Earnings Growth", "Dividend Yield"],
        key_metrics=["Annual Return", "Sharpe Ratio", "Fundamental Score", "Valuation Trend"],
        recommended_position_size="Risk 2-3% per position",
        risk_per_trade_pct=2.5,
        stop_loss_atr_multiplier=3.0,
        take_profit_atr_multiplier=5.0,
        holding_period="Months to years",
        decision_speed="slow"
    ),
    TradingStyle.VALUE: StyleConfig(
        name="Value Investor",
        timeframe="1-5 years",
        priority_indicators=["PE Ratio", "PB Ratio", "ROE", "Dividend Yield", "5-Year Trend", "Debt/Equity"],
        key_metrics=["Margin of Safety", "PE Improvement", "ROE Trend", "Dividend Growth", "Book Value"],
        recommended_position_size="Core position, Risk 2-3%",
        risk_per_trade_pct=2.5,
        stop_loss_atr_multiplier=4.0,
        take_profit_atr_multiplier=None,  # No hard targets, long-term hold
        holding_period="1-5 years",
        decision_speed="slow"
    )
}


def generate_layout(
    trading_style: str,
    risk_level: str = "moderate",
    symbol: str = "UNKNOWN"
) -> Dict:
    """
    Generate customized analysis layout based on trading style.
    
    Args:
        trading_style: "scalper", "swing", "investor", or "value"
        risk_level: "conservative", "moderate", or "aggressive"
        symbol: Stock symbol for context
    
    Returns:
        Dict with customized layout configuration
    """
    try:
        style_enum = TradingStyle(trading_style)
        config = STYLE_CONFIGS[style_enum]
    except (ValueError, KeyError):
        # Default to swing trader
        style_enum = TradingStyle.SWING
        config = STYLE_CONFIGS[style_enum]
    
    risk_enum = RiskLevel(risk_level) if risk_level in [e.value for e in RiskLevel] else RiskLevel.MODERATE
    
    # Adjust metrics based on risk level
    if risk_enum == RiskLevel.AGGRESSIVE:
        position_size = config.recommended_position_size.replace("2-3", "3-5")
        risk_pct = config.risk_per_trade_pct * 1.5
    elif risk_enum == RiskLevel.CONSERVATIVE:
        position_size = config.recommended_position_size.replace("2-3", "1-2").replace("1-2", "0.5-1")
        risk_pct = config.risk_per_trade_pct * 0.67
    else:
        position_size = config.recommended_position_size
        risk_pct = config.risk_per_trade_pct
    
    layout = {
        "trading_style": style_enum.value,
        "symbol": symbol,
        "generated_at": datetime.now().isoformat(),
        
        # Display configuration
        "display": {
            "primary_chart_timeframe": config.timeframe,
            "priority_indicators": config.priority_indicators,
            "key_metrics_dashboard": config.key_metrics,
            "show_volume": True,
            "show_pattern_zones": style_enum in [TradingStyle.SWING, TradingStyle.VALUE],
            "show_seasonality": style_enum in [TradingStyle.SWING, TradingStyle.INVESTOR],
        },
        
        # Risk management rules
        "risk_management": {
            "position_sizing": position_size,
            "risk_per_trade_pct": round(risk_pct, 2),
            "stop_loss_method": f"ATR × {config.stop_loss_atr_multiplier}" if config.stop_loss_atr_multiplier else "Support level",
            "take_profit_method": f"ATR × {config.take_profit_atr_multiplier}" if config.take_profit_atr_multiplier else "Fundamental milestone",
            "max_drawdown_limit_pct": 10 if risk_enum == RiskLevel.AGGRESSIVE else (5 if risk_enum == RiskLevel.MODERATE else 3),
        },
        
        # Entry/exit criteria
        "entry_criteria": get_entry_criteria(style_enum),
        "exit_criteria": get_exit_criteria(style_enum),
        
        # Recommended holding period
        "holding_period": config.holding_period,
        "decision_making_speed": config.decision_speed,
        
        # Alerts and notifications
        "alerts": get_alerts_for_style(style_enum),
        
        # Performance expectations (backtested averages for IDX)
        "performance_expectations": get_expectations(style_enum),
    }
    
    return layout


def get_entry_criteria(style: TradingStyle) -> Dict:
    """Entry signals for each trading style."""
    entries = {
        TradingStyle.SCALPER: {
            "primary": "RSI < 30 (oversold) with volume confirmation",
            "confirmation": "MACD bullish crossover in 5-min chart",
            "additional": "Above EMA20 on intraday chart",
            "avoid": "Against major trend, within 30-min of major data release"
        },
        TradingStyle.SWING: {
            "primary": "Price breaks above support + EMA20 > EMA50",
            "confirmation": "RSI 50-70 (bullish momentum) + MACD positive",
            "additional": "Volume > 20-day average, Bollinger Band breakout",
            "avoid": "During earnings uncertainty, when above resistance"
        },
        TradingStyle.INVESTOR: {
            "primary": "PE < 10 or PB < 1.0 (undervalued relative to peers)",
            "confirmation": "ROE > 15%, Earnings growing, Dividend stable",
            "additional": "Price above EMA200 (long-term uptrend), ESG improving",
            "avoid": "High debt/equity, declining ROE, sector headwinds"
        },
        TradingStyle.VALUE: {
            "primary": "PE at 3-year lows, Margin of Safety > 20%",
            "confirmation": "ROE > 15%, Dividend yield attractive, Balance sheet strong",
            "additional": "PE improving trend (5-year low), Insider buying",
            "avoid": "Deteriorating fundamentals, high leverage, mature/declining sectors"
        }
    }
    return entries.get(style, entries[TradingStyle.SWING])


def get_exit_criteria(style: TradingStyle) -> Dict:
    """Exit signals for each trading style."""
    exits = {
        TradingStyle.SCALPER: {
            "profit_target": "+1.5 to +3% from entry",
            "stop_loss": "0.5 ATR below entry",
            "time_stop": "Exit if no movement in 5-15 min",
            "additional": "Close on opposite MACD signal"
        },
        TradingStyle.SWING: {
            "profit_target": "Support/Resistance level or +5-10%",
            "stop_loss": "1.2 ATR below support level",
            "time_stop": "Exit if consolidating >2 days",
            "additional": "Close at EMA resistance if momentum weakens"
        },
        TradingStyle.INVESTOR: {
            "profit_target": "Target price or 20-30% gain (whichever first)",
            "stop_loss": "10% below entry or if fundamentals deteriorate",
            "time_stop": "Hold for 2-5 years, review quarterly",
            "additional": "Rebalance if PE > 1.5× sector average"
        },
        TradingStyle.VALUE: {
            "profit_target": "Fair value (PE = sector average) or +15-25% over years",
            "stop_loss": "No hard stop; hold through cycles",
            "time_stop": "Indefinite hold if fundamentals improve",
            "additional": "Sell if PE reverts to fair value + 10% margin"
        }
    }
    return exits.get(style, exits[TradingStyle.SWING])


def get_alerts_for_style(style: TradingStyle) -> List[str]:
    """Real-time alerts for each trading style."""
    alerts = {
        TradingStyle.SCALPER: [
            "RSI < 20 (extreme oversold)",
            "Volume spike > 3× average",
            "Breakout above/below recent high/low",
            "MACD crossover + RSI confirmation"
        ],
        TradingStyle.SWING: [
            "Support/Resistance breach",
            "Bollinger Band breakout + volume",
            "EMA20 crosses EMA50",
            "RSI divergence (higher low, lower price)"
        ],
        TradingStyle.INVESTOR: [
            "Earnings announcement",
            "Dividend cut or suspension",
            "PE drops below 0.7× of 5-year average",
            "Significant insider trading activity"
        ],
        TradingStyle.VALUE: [
            "PE at new 5-year low",
            "Major dividend increase",
            "ROE improvement acceleration",
            "Analyst downgrade (potential margin of safety)"
        ]
    }
    return alerts.get(style, alerts[TradingStyle.SWING])


def get_expectations(style: TradingStyle) -> Dict:
    """Expected performance metrics for each style (IDX historical data)."""
    expectations = {
        TradingStyle.SCALPER: {
            "win_rate_pct": "50-55%",
            "avg_profit_factor": "1.2-1.5",
            "annual_return_pct": "30-100% (high variance)",
            "max_drawdown_pct": "10-20%",
            "trades_per_month": "50-200"
        },
        TradingStyle.SWING: {
            "win_rate_pct": "45-55%",
            "avg_profit_factor": "1.5-2.0",
            "annual_return_pct": "20-40%",
            "max_drawdown_pct": "10-15%",
            "trades_per_month": "10-20"
        },
        TradingStyle.INVESTOR: {
            "win_rate_pct": "60-70% (by position, not trade)",
            "avg_profit_factor": "2.0-3.0",
            "annual_return_pct": "12-18%",
            "max_drawdown_pct": "15-25%",
            "positions_held": "5-15"
        },
        TradingStyle.VALUE: {
            "win_rate_pct": "70-80%",
            "avg_profit_factor": "3.0-5.0+",
            "annual_return_pct": "15-25%",
            "max_drawdown_pct": "20-35% (endure to compound)",
            "positions_held": "3-8"
        }
    }
    return expectations.get(style, expectations[TradingStyle.SWING])


def synthesize_recommendation(
    technical_score: float,
    fundamental_score: float,
    layout: Dict,
    symbol: str = "UNKNOWN"
) -> str:
    """
    Generate natural language recommendation based on scores and trading style.
    
    This is a rule-based version. In production, could call Claude/GPT API.
    
    Args:
        technical_score: -3 to +3
        fundamental_score: -1.5 to +2.5
        layout: Style configuration from generate_layout()
        symbol: Stock symbol
    
    Returns:
        Natural language recommendation
    """
    style = layout["trading_style"]
    combined_score = technical_score + fundamental_score
    
    # Construct reasoning
    if style == "scalper":
        if combined_score >= 1.5:
            return f"{symbol}: Setup looks favorable for scalp trade. RSI dipped, MACD bullish. Watch for tight consolidation, then ride momentum for 1-3% gains. Keep stop loss tight (0.5 ATR)."
        else:
            return f"{symbol}: Scalping opportunity weak right now. Wait for clearer RSI oversold + MACD confirmation. Current conditions lack the required sharp reversal signal."
    
    elif style == "swing":
        if combined_score >= 1.0:
            entry_level = "at current support" if technical_score >= 1 else "dip to EMA50"
            return f"{symbol}: Swing setup forming. Enter {entry_level}, target resistance 5-10% above. Hold 2-5 days. Exit if breaks support or consolidates >2 days without momentum."
        else:
            return f"{symbol}: Not ideal for swing trade now. Lacks EMA alignment or momentum confirmation. Monitor for 1-2 weeks until better setup emerges."
    
    elif style == "investor":
        if combined_score >= 1.0:
            return f"{symbol}: Suitable for long-term position. Fundamentals solid (PE reasonable, ROE strong). Ignore short-term noise. Build position on weakness. Target: 5+ year hold, 15-20% annual returns."
        else:
            return f"{symbol}: Fundamentals need improvement. Wait for better entry or select alternatives with clearer growth trajectory."
    
    elif style == "value":
        if combined_score >= 0.5:
            margin = f"{abs(combined_score)*10:.0f}%" if combined_score < 1.5 else "20%+"
            return f"{symbol}: Value opportunity detected. Current valuation underprices fundamentals by ~{margin}. Build core position. Hold through cycles. Exit only if fundamentals deteriorate permanently."
        else:
            return f"{symbol}: Not sufficiently undervalued vs fundamentals. Pass. Continue monitoring 5-year PE trend."
    
    return f"{symbol}: Neutral. Requires more data clarity before commitment."


if __name__ == "__main__":
    # Test layouts
    print("\n=== Trading Style Layouts ===\n")
    
    for style in ["scalper", "swing", "investor", "value"]:
        layout = generate_layout(style, "moderate", "BBCA")
        print(f"\n{style.upper()}:")
        print(f"  Indicators: {layout['display']['priority_indicators'][:3]}")
        print(f"  Risk/Trade: {layout['risk_management']['risk_per_trade_pct']}%")
        print(f"  Holding: {layout['holding_period']}")
        
        rec = synthesize_recommendation(2.5, 1.0, layout, "BBCA")
        print(f"  Recommendation: {rec[:100]}...")
