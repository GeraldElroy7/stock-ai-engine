"""
Enterprise Configuration
For institutional integration and API deployment
"""

# ===== SIGNAL THRESHOLDS =====
# Optimized based on historical analysis across 312 data points
# Thresholds set at 75th/25th percentiles for better signal distribution
SIGNAL_CONFIG = {
    "BUY_THRESHOLD": 4.0,       # Score >= 4.0 = BUY signal (top 25% of signals)
    "SELL_THRESHOLD": -0.5,     # Score <= -0.5 = SELL signal (bottom 25% of signals)
    "SHORT_THRESHOLD": -7.0,    # Score <= -7.0 = SHORT signal (extreme downtrend, profit from decline)
    # Score ranges: SHORT <-7 | SELL -7 to -0.5 | HOLD -0.5 to 4.0 | BUY >4.0
}

# ===== RISK MANAGEMENT =====
RISK_CONFIG = {
    "MAX_POSITION_SIZE_PCT": 5.0,           # Max 5% per trade
    "STOP_LOSS_MULTIPLIER": 2.0,            # Stop = entry - (2 * ATR)
    "TAKE_PROFIT_MULTIPLIER": 3.0,          # TP = entry + (3 * ATR)
    "RISK_REWARD_RATIO_MIN": 1.0,           # Minimum 1:1 R:R
    "MAX_CONCURRENT_POSITIONS": 10,          # Max 10 open positions
    "MAX_DAILY_LOSS_PCT": 2.0,              # Stop trading if -2% in a day
}

# ===== BACKTEST VALIDATION =====
BACKTEST_THRESHOLDS = {
    "MIN_WIN_RATE": 0.55,           # Minimum 55% win rate
    "MIN_RECOVERY_FACTOR": 2.0,     # Profit / Max Drawdown >= 2
    "MIN_SHARPE_RATIO": 0.5,        # Risk-adjusted return
    "MAX_CONSECUTIVE_LOSSES": 5,    # Psychological limit
    "MIN_TRADES_FOR_VALIDATION": 20, # Need 20+ trades to validate
    "SHORT_SIGNAL_ENABLED": True,    # Enable SHORT signal generation
    "SHORT_WIN_RATE_TARGET": 0.50    # SHORT signals can have lower win rate (larger moves)
}

# ===== INSTITUTIONAL REQUIREMENTS =====
INSTITUTIONAL_CONFIG = {
    "INCLUDE_TRANSACTION_COSTS": True,      # Account for fees/slippage
    "TRANSACTION_COST_PCT": 0.05,           # 0.05% per trade
    "MIN_LIQUIDITY_VOLUME_USD": 100_000,    # Only liquid stocks
    "EXCLUDE_HALTED_STOCKS": True,
    "LOG_ALL_SIGNALS": True,                # Audit trail
}

# ===== DATA SOURCES =====
DATA_CONFIG = {
    "PRIMARY_SOURCE": "yfinance",
    "FALLBACK_SOURCE": "None",  # Add fallback if needed
    "LOOKBACK_PERIOD": "1y",    # Historical data window (upgraded from 6mo for better accuracy)
    "TIMEZONE": "Asia/Jakarta",
    "MARKET": "Indonesia (IDX)",
    "DATA_POINTS_TARGET": 250,   # Approximately 250 trading days per year
}

# ===== INDICATOR SETTINGS =====
INDICATOR_CONFIG = {
    "EMA_FAST": 20,
    "EMA_MEDIUM": 50,
    "EMA_SLOW": 200,
    "RSI_PERIOD": 14,
    "RSI_OVERBOUGHT": 70,
    "RSI_OVERSOLD": 30,
    "MACD_FAST": 12,
    "MACD_SLOW": 26,
    "MACD_SIGNAL": 9,
    "BB_PERIOD": 20,
    "BB_STDDEV": 2.0,
    "ATR_PERIOD": 14,
    "VOLUME_MA_PERIOD": 20,
}

# ===== TRADING STYLES (for future UI personalization) =====
TRADING_STYLES = {
    "scalper": {
        "description": "High-frequency, small profits (5min-1hr charts)",
        "buy_threshold": 8.0,
        "indicators": ["RSI", "MACD", "Volume"],
        "timeframes": ["5min", "15min", "1h"]
    },
    "day_trader": {
        "description": "Intraday trades (1hr-4hr charts)",
        "buy_threshold": 7.0,
        "indicators": ["EMA", "MACD", "RSI", "Bollinger Bands"],
        "timeframes": ["1h", "4h"]
    },
    "swing_trader": {
        "description": "Medium-term trends (daily charts)",
        "buy_threshold": 6.5,
        "indicators": ["EMA200", "MACD", "RSI"],
        "timeframes": ["1d", "1w"]
    },
    "long_term_investor": {
        "description": "Multi-week/month positions",
        "buy_threshold": 6.0,
        "indicators": ["EMA200", "RSI"],
        "timeframes": ["1w", "1M"]
    }
}

# ===== REPORTING =====
REPORT_CONFIG = {
    "INCLUDE_SHARPE_RATIO": True,
    "INCLUDE_DRAWDOWN": True,
    "INCLUDE_PROFIT_FACTOR": True,
    "INCLUDE_EXPECTANCY": True,
    "FORMAT": "json",  # Can also be "csv", "pdf"
    "SEND_ALERTS": False,  # Email alerts on new signals
}

# ===== API / DEPLOYMENT =====
API_CONFIG = {
    "ENABLE_REST_API": True,
    "ENABLE_WEBSOCKET": True,
    "PORT": 8000,
    "HOST": "0.0.0.0",
    "RATE_LIMIT_PER_MINUTE": 60,
    "REQUIRE_API_KEY": True,
}

# ===== REVENUE SHARING MODEL =====
REVENUE_CONFIG = {
    "MODEL": "profit_sharing",  # "profit_sharing", "per_transaction", "subscription"
    "REVENUE_SHARE_PCT": 15.0,   # Platform takes 15% of profits
    "MIN_ACCOUNT_SIZE": 1_000_000,  # Minimum $1M to use system
    "PROFIT_SHARE_CALC": "monthly",  # Calculate monthly
}
