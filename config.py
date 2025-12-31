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
}

# ===== SUPPORTED STOCKS =====
# IHSG Stocks - Easily extensible to 100+ stocks
# Format: "SYMBOL": {"is_us": False, "name": "Company Name", "sector": "Sector"}
SUPPORTED_STOCKS = {
    # === BLUE CHIPS (Top 10) ===
    "BBCA": {"is_us": False, "name": "Bank Central Asia", "sector": "Banking"},
    "BBRI": {"is_us": False, "name": "Bank Rakyat Indonesia", "sector": "Banking"},
    "BMRI": {"is_us": False, "name": "Bank Mandiri", "sector": "Banking"},
    "ASII": {"is_us": False, "name": "Astra International", "sector": "Automotive"},
    "UNVR": {"is_us": False, "name": "Unilever Indonesia", "sector": "Consumer Goods"},
    "INCO": {"is_us": False, "name": "Vale Indonesia", "sector": "Mining"},
    "ANTM": {"is_us": False, "name": "Antam", "sector": "Mining"},
    "ITMG": {"is_us": False, "name": "Indo Tambangraya Megah", "sector": "Mining"},
    "TINS": {"is_us": False, "name": "Timah", "sector": "Mining"},
    "NICL": {"is_us": False, "name": "Nickel Indonesia", "sector": "Mining"},
    
    # === FINANCE & BANKING ===
    "MEDC": {"is_us": False, "name": "Medco Energi", "sector": "Finance"},
    "MDKA": {"is_us": False, "name": "Merdeka Copper Gold", "sector": "Mining"},
    "ASSO": {"is_us": False, "name": "Asosiasi Asuransi Indonesia", "sector": "Insurance"},
    "AKRA": {"is_us": False, "name": "AKR Corporindo", "sector": "Trading"},
    
    # === AGRICULTURE & CONSUMER ===
    "AGRO": {"is_us": False, "name": "Bank Pertanian", "sector": "Banking"},
    "INDF": {"is_us": False, "name": "Indofood", "sector": "Consumer Goods"},
    
    # === UTILITIES & ENERGY ===
    "PGAS": {"is_us": False, "name": "Perusahaan Gas Negara", "sector": "Utilities"},
    "ADRO": {"is_us": False, "name": "Adaro Energy", "sector": "Energy"},
    
    # === PROPERTY & CONSTRUCTION ===
    "CTRA": {"is_us": False, "name": "Citraland", "sector": "Property"},
    "MNCN": {"is_us": False, "name": "MNC Investama", "sector": "Media"},
    "PTPP": {"is_us": False, "name": "Pembangunan Perumahan", "sector": "Construction"},
    "WIKA": {"is_us": False, "name": "Wijaya Karya", "sector": "Construction"},
    
    # === TECH & DIGITAL ===
    "GOTO": {"is_us": False, "name": "GoTo Gojek Tokopedia", "sector": "Technology"},
    "ASRI": {"is_us": False, "name": "Astra Sedaya Finance", "sector": "Finance"},
    
    # === TELECOMMUNICATIONS ===
    "TLKM": {"is_us": False, "name": "Telkom", "sector": "Telecom"},
    
    # === TRANSPORTATION & LOGISTICS ===
    "BRPT": {"is_us": False, "name": "Bhakti Pertiwi", "sector": "Transportation"},
    
    # === HEALTHCARE ===
    "ARNA": {"is_us": False, "name": "Arwana Citramulia", "sector": "Healthcare"},
    
    # === SUPPORTING TIER (Add more as needed) ===
    "JPRS": {"is_us": False, "name": "Jasa Marga", "sector": "Transportation"},
    
    # === US STOCKS ===
    "COIN": {"is_us": True, "name": "Coinbase Global", "sector": "Crypto"},
    "TSLA": {"is_us": True, "name": "Tesla", "sector": "Automotive"},
    "AAPL": {"is_us": True, "name": "Apple", "sector": "Technology"},
    "MSFT": {"is_us": True, "name": "Microsoft", "sector": "Technology"},
    "GOOGL": {"is_us": True, "name": "Alphabet (Google)", "sector": "Technology"},
    "AMZN": {"is_us": True, "name": "Amazon", "sector": "E-Commerce"},
}

# ===== EASY EXTEND GUIDE =====
"""
To add more IHSG stocks, just add to SUPPORTED_STOCKS dict:

SUPPORTED_STOCKS.update({
    "SYMBOL": {"is_us": False, "name": "Full Company Name", "sector": "Sector"},
    ...
})

Atau gunakan endpoint POST /admin/add-stock untuk menambah di runtime
"""
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
