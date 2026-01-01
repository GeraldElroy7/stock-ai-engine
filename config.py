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
    "LOOKBACK_PERIOD": "10y",    # Historical data window (10 years for comprehensive analysis)
    "MAX_DATA_POINTS": 2520,     # Approximately 252 trading days * 10 years
}

# ===== SUPPORTED STOCKS =====
# Complete Indonesian Stock Exchange (IDX) Coverage - January 2026
# Format: "SYMBOL": {"is_us": False, "name": "Company Name", "sector": "Sector"}
SUPPORTED_STOCKS = {
    # === IDX-30 (Blue Chip Stocks) ===
    "BBCA": {"is_us": False, "name": "Bank Central Asia", "sector": "Banking"},
    "BBRI": {"is_us": False, "name": "Bank Rakyat Indonesia", "sector": "Banking"},
    "BMRI": {"is_us": False, "name": "Bank Mandiri", "sector": "Banking"},
    "BBNI": {"is_us": False, "name": "Bank Negara Indonesia", "sector": "Banking"},
    "ASII": {"is_us": False, "name": "Astra International", "sector": "Automotive"},
    "UNVR": {"is_us": False, "name": "Unilever Indonesia", "sector": "Consumer Goods"},
    "TLKM": {"is_us": False, "name": "Telkom Indonesia", "sector": "Telecommunications"},
    "INDF": {"is_us": False, "name": "Indofood Sukses Makmur", "sector": "Consumer Goods"},
    "ICBP": {"is_us": False, "name": "Indofood CBP", "sector": "Consumer Goods"},
    "INCO": {"is_us": False, "name": "Vale Indonesia", "sector": "Mining"},
    "ANTM": {"is_us": False, "name": "Aneka Tambang", "sector": "Mining"},
    "ADRO": {"is_us": False, "name": "Adaro Energy", "sector": "Energy"},
    "ITMG": {"is_us": False, "name": "Indo Tambangraya Megah", "sector": "Mining"},
    "PTBA": {"is_us": False, "name": "Bukit Asam", "sector": "Mining"},
    "KLBF": {"is_us": False, "name": "Kalbe Farma", "sector": "Healthcare"},
    "GGRM": {"is_us": False, "name": "Gudang Garam", "sector": "Consumer Goods"},
    "HMSP": {"is_us": False, "name": "HM Sampoerna", "sector": "Consumer Goods"},
    "CPIN": {"is_us": False, "name": "Charoen Pokphand Indonesia", "sector": "Consumer Goods"},
    "EXCL": {"is_us": False, "name": "XL Axiata", "sector": "Telecommunications"},
    "PGAS": {"is_us": False, "name": "Perusahaan Gas Negara", "sector": "Utilities"},
    "SMGR": {"is_us": False, "name": "Semen Indonesia", "sector": "Construction"},
    "TOWR": {"is_us": False, "name": "Sarana Menara Nusantara", "sector": "Telecommunications"},
    "MNCN": {"is_us": False, "name": "Media Nusantara Citra", "sector": "Media"},
    "JSMR": {"is_us": False, "name": "Jasa Marga", "sector": "Transportation"},
    "WIKA": {"is_us": False, "name": "Wijaya Karya", "sector": "Construction"},
    "PTPP": {"is_us": False, "name": "PP (Persero)", "sector": "Construction"},
    "AKRA": {"is_us": False, "name": "AKR Corporindo", "sector": "Trading"},
    "EMTK": {"is_us": False, "name": "Elang Mahkota Teknologi", "sector": "Media"},
    "SCMA": {"is_us": False, "name": "Surya Citra Media", "sector": "Media"},
    "BRPT": {"is_us": False, "name": "Barito Pacific", "sector": "Basic Materials"},
    
    # === LQ45 Additional ===
    "BSDE": {"is_us": False, "name": "Bumi Serpong Damai", "sector": "Property"},
    "CTRA": {"is_us": False, "name": "Ciputra Development", "sector": "Property"},
    "PWON": {"is_us": False, "name": "Pakuwon Jati", "sector": "Property"},
    "LPKR": {"is_us": False, "name": "Lippo Karawaci", "sector": "Property"},
    "SMRA": {"is_us": False, "name": "Summarecon Agung", "sector": "Property"},
    "MAPI": {"is_us": False, "name": "Mitra Adiperkasa", "sector": "Retail"},
    "ACES": {"is_us": False, "name": "Ace Hardware Indonesia", "sector": "Retail"},
    "ERAA": {"is_us": False, "name": "Erajaya Swasembada", "sector": "Retail"},
    "SRIL": {"is_us": False, "name": "Sri Rejeki Isman", "sector": "Textile"},
    "AMRT": {"is_us": False, "name": "Sumber Alfaria Trijaya", "sector": "Retail"},
    "MDKA": {"is_us": False, "name": "Merdeka Copper Gold", "sector": "Mining"},
    "TINS": {"is_us": False, "name": "Timah", "sector": "Mining"},
    "MEDC": {"is_us": False, "name": "Medco Energi", "sector": "Energy"},
    "BYAN": {"is_us": False, "name": "Bayan Resources", "sector": "Mining"},
    "AMMN": {"is_us": False, "name": "Amman Mineral", "sector": "Mining"},
    
    # === Banking Sector (Complete) ===
    "BBTN": {"is_us": False, "name": "Bank Tabungan Negara", "sector": "Banking"},
    "BRIS": {"is_us": False, "name": "Bank BRI Syariah", "sector": "Banking"},
    "BJBR": {"is_us": False, "name": "Bank Pembangunan Daerah Jawa Barat", "sector": "Banking"},
    "BJTM": {"is_us": False, "name": "Bank Pembangunan Daerah Jawa Timur", "sector": "Banking"},
    "NISP": {"is_us": False, "name": "Bank OCBC NISP", "sector": "Banking"},
    "PNBN": {"is_us": False, "name": "Bank Pan Indonesia", "sector": "Banking"},
    "BNLI": {"is_us": False, "name": "Bank Permata", "sector": "Banking"},
    "BNGA": {"is_us": False, "name": "Bank CIMB Niaga", "sector": "Banking"},
    "MEGA": {"is_us": False, "name": "Bank Mega", "sector": "Banking"},
    "BTPS": {"is_us": False, "name": "Bank BTPN Syariah", "sector": "Banking"},
    "MAYA": {"is_us": False, "name": "Bank Mayapada", "sector": "Banking"},
    "BACA": {"is_us": False, "name": "Bank Capital Indonesia", "sector": "Banking"},
    "BMAS": {"is_us": False, "name": "Bank Maspion Indonesia", "sector": "Banking"},
    "BNII": {"is_us": False, "name": "Bank Maybank Indonesia", "sector": "Banking"},
    
    # === Mining & Energy (Extended) ===
    "HRUM": {"is_us": False, "name": "Harum Energy", "sector": "Mining"},
    "KKGI": {"is_us": False, "name": "Resource Alam Indonesia", "sector": "Mining"},
    "DOID": {"is_us": False, "name": "Delta Dunia Makmur", "sector": "Mining"},
    "GEMS": {"is_us": False, "name": "Golden Energy Mines", "sector": "Mining"},
    "ELSA": {"is_us": False, "name": "Elnusa", "sector": "Energy"},
    "ENRG": {"is_us": False, "name": "Energi Mega Persada", "sector": "Energy"},
    "RUIS": {"is_us": False, "name": "Radiant Utama Interinsco", "sector": "Mining"},
    
    # === Consumer Goods (Extended) ===
    "KAEF": {"is_us": False, "name": "Kimia Farma", "sector": "Healthcare"},
    "MYOR": {"is_us": False, "name": "Mayora Indah", "sector": "Consumer Goods"},
    "ULTJ": {"is_us": False, "name": "Ultra Jaya Milk", "sector": "Consumer Goods"},
    "MLBI": {"is_us": False, "name": "Multi Bintang Indonesia", "sector": "Consumer Goods"},
    "SIDO": {"is_us": False, "name": "Industri Jamu Sido Muncul", "sector": "Healthcare"},
    "TSPC": {"is_us": False, "name": "Tempo Scan Pacific", "sector": "Healthcare"},
    "DVLA": {"is_us": False, "name": "Darya-Varia Laboratoria", "sector": "Healthcare"},
    "WIIM": {"is_us": False, "name": "Wismilak Inti Makmur", "sector": "Consumer Goods"},
    "ROTI": {"is_us": False, "name": "Nippon Indosari Corpindo", "sector": "Consumer Goods"},
    "GOOD": {"is_us": False, "name": "Garudafood Putra Putri Jaya", "sector": "Consumer Goods"},
    "SKBM": {"is_us": False, "name": "Sekar Bumi", "sector": "Consumer Goods"},
    
    # === Technology & Telecommunications ===
    "ISAT": {"is_us": False, "name": "Indosat Ooredoo", "sector": "Telecommunications"},
    "TBIG": {"is_us": False, "name": "Tower Bersama Infrastructure", "sector": "Telecommunications"},
    "GOTO": {"is_us": False, "name": "GoTo Gojek Tokopedia", "sector": "Technology"},
    "BUKA": {"is_us": False, "name": "Bukalapak.com", "sector": "Technology"},
    "BELI": {"is_us": False, "name": "Blibli.com", "sector": "Technology"},
    "FREN": {"is_us": False, "name": "Smartfren Telecom", "sector": "Telecommunications"},
    "LINK": {"is_us": False, "name": "Link Net", "sector": "Telecommunications"},
    
    # === Property & Construction (Extended) ===
    "ASRI": {"is_us": False, "name": "Alam Sutera Realty", "sector": "Property"},
    "APLN": {"is_us": False, "name": "Agung Podomoro Land", "sector": "Property"},
    "DMAS": {"is_us": False, "name": "Puradelta Lestari", "sector": "Property"},
    "PLIN": {"is_us": False, "name": "Plaza Indonesia Realty", "sector": "Property"},
    "BEST": {"is_us": False, "name": "Bekasi Fajar Industrial Estate", "sector": "Property"},
    "WSBP": {"is_us": False, "name": "Waskita Beton Precast", "sector": "Construction"},
    "WSKT": {"is_us": False, "name": "Waskita Karya", "sector": "Construction"},
    "ADHI": {"is_us": False, "name": "Adhi Karya", "sector": "Construction"},
    "TOTL": {"is_us": False, "name": "Total Bangun Persada", "sector": "Construction"},
    
    # === Retail & Trade ===
    "LPPF": {"is_us": False, "name": "Matahari Department Store", "sector": "Retail"},
    "RALS": {"is_us": False, "name": "Ramayana Lestari Sentosa", "sector": "Retail"},
    "CSAP": {"is_us": False, "name": "Catur Sentosa Adiprana", "sector": "Retail"},
    "HERO": {"is_us": False, "name": "Hero Supermarket", "sector": "Retail"},
    "UNTR": {"is_us": False, "name": "United Tractors", "sector": "Trading"},
    "ESSA": {"is_us": False, "name": "Surya Esa Perkasa", "sector": "Trading"},
    
    # === Transportation & Logistics ===
    "GIAA": {"is_us": False, "name": "Garuda Indonesia", "sector": "Transportation"},
    "BIRD": {"is_us": False, "name": "Blue Bird", "sector": "Transportation"},
    "WEHA": {"is_us": False, "name": "Weha Transportasi Indonesia", "sector": "Transportation"},
    "TRAM": {"is_us": False, "name": "Trada Alam Minera", "sector": "Transportation"},
    "BMTR": {"is_us": False, "name": "Global Mediacom", "sector": "Transportation"},
    "SMDR": {"is_us": False, "name": "Samudera Indonesia", "sector": "Transportation"},
}

# ===== EASY EXTEND GUIDE =====
EXTEND_GUIDE = """
To add more IHSG stocks, just add to SUPPORTED_STOCKS dict:

SUPPORTED_STOCKS.update({
    "SYMBOL": {"is_us": False, "name": "Full Company Name", "sector": "Sector"},
    ...
})
"""

# ===== DATA CONFIGURATION =====
DATA_CONFIG = {
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
        "sell_threshold": -1.5,
        "indicators": ["RSI", "MACD", "Volume"],
        "timeframes": ["5min", "15min", "1h"],
        "holding_period": "minutes to hours",
        "risk_level": "high"
    },
    "day_trader": {
        "description": "Intraday trades (1hr-4hr charts)",
        "buy_threshold": 7.0,
        "sell_threshold": -1.0,
        "indicators": ["EMA", "MACD", "RSI", "Bollinger Bands"],
        "timeframes": ["1h", "4h"],
        "holding_period": "hours to 1 day",
        "risk_level": "medium-high"
    },
    "swing_trader": {
        "description": "Medium-term trends (daily charts)",
        "buy_threshold": 6.5,
        "sell_threshold": -0.75,
        "indicators": ["EMA200", "MACD", "RSI"],
        "timeframes": ["1d", "1w"],
        "holding_period": "days to weeks",
        "risk_level": "medium"
    },
    "position_trader": {
        "description": "Long-term positions (weekly/monthly charts)",
        "buy_threshold": 6.0,
        "sell_threshold": -0.5,
        "indicators": ["EMA200", "RSI"],
        "timeframes": ["1w", "1M"],
        "holding_period": "weeks to months",
        "risk_level": "low-medium"
    },
    "long_term_investor": {
        "description": "Multi-month/year positions (fundamentals-focused)",
        "buy_threshold": 5.0,
        "sell_threshold": -0.3,
        "indicators": ["EMA200", "Fundamentals"],
        "timeframes": ["1M"],
        "holding_period": "months to years",
        "risk_level": "low"
    }
}

# ===== USER INPUT PARAMETERS =====
# These parameters allow personalization of signals and recommendations
USER_INPUT_PARAMS = {
    "trading_style": {
        "type": "select",
        "options": ["scalper", "day_trader", "swing_trader", "position_trader", "long_term_investor"],
        "default": "swing_trader",
        "description": "Your preferred trading approach and timeframe"
    },
    "risk_level": {
        "type": "select",
        "options": ["conservative", "moderate", "aggressive", "very_aggressive"],
        "default": "moderate",
        "description": "How much risk you're willing to take",
        "mapping": {
            "conservative": {
                "max_position_size_pct": 2.0,
                "stop_loss_multiplier": 1.5,
                "min_confidence": 0.70,
                "max_concurrent_positions": 5
            },
            "moderate": {
                "max_position_size_pct": 5.0,
                "stop_loss_multiplier": 2.0,
                "min_confidence": 0.60,
                "max_concurrent_positions": 10
            },
            "aggressive": {
                "max_position_size_pct": 8.0,
                "stop_loss_multiplier": 2.5,
                "min_confidence": 0.50,
                "max_concurrent_positions": 15
            },
            "very_aggressive": {
                "max_position_size_pct": 10.0,
                "stop_loss_multiplier": 3.0,
                "min_confidence": 0.40,
                "max_concurrent_positions": 20
            }
        }
    },
    "capital_size": {
        "type": "number",
        "min": 1_000_000,
        "max": 100_000_000_000,
        "default": 10_000_000,
        "description": "Total trading capital in IDR",
        "currency": "IDR"
    },
    "investment_goal": {
        "type": "select",
        "options": ["income", "growth", "balanced", "speculation"],
        "default": "balanced",
        "description": "Primary investment objective",
        "preferences": {
            "income": {
                "prefer_dividends": True,
                "sectors": ["Banking", "Utilities", "Consumer Goods"],
                "min_dividend_yield": 3.0
            },
            "growth": {
                "prefer_growth_stocks": True,
                "sectors": ["Technology", "Mining", "Energy"],
                "min_revenue_growth": 15.0
            },
            "balanced": {
                "prefer_balanced": True,
                "sectors": ["All"],
                "min_dividend_yield": 2.0,
                "min_revenue_growth": 10.0
            },
            "speculation": {
                "prefer_volatile": True,
                "sectors": ["Technology", "Mining", "Retail"],
                "min_volatility": 20.0
            }
        }
    },
    "sector_preference": {
        "type": "multi-select",
        "options": [
            "Banking", "Mining", "Energy", "Consumer Goods", "Healthcare",
            "Technology", "Telecommunications", "Property", "Construction",
            "Retail", "Transportation", "Media", "Utilities", "Trading"
        ],
        "default": ["All"],
        "description": "Sectors you want to focus on"
    },
    "exclude_sectors": {
        "type": "multi-select",
        "options": [
            "Banking", "Mining", "Energy", "Consumer Goods", "Healthcare",
            "Technology", "Telecommunications", "Property", "Construction",
            "Retail", "Transportation", "Media", "Utilities", "Trading"
        ],
        "default": [],
        "description": "Sectors to avoid (e.g., ethical reasons)"
    },
    "min_confidence_level": {
        "type": "number",
        "min": 0.0,
        "max": 1.0,
        "default": 0.60,
        "description": "Minimum confidence score to show signals (0-1)",
        "step": 0.05
    },
    "enable_short_signals": {
        "type": "boolean",
        "default": True,
        "description": "Allow SHORT signals (profit from downtrends)"
    },
    "max_stocks_to_monitor": {
        "type": "number",
        "min": 1,
        "max": 200,
        "default": 50,
        "description": "Maximum number of stocks to analyze"
    },
    "notification_preferences": {
        "type": "multi-select",
        "options": ["email", "sms", "push", "webhook"],
        "default": ["email"],
        "description": "How to receive signal alerts"
    },
    "alert_conditions": {
        "type": "multi-select",
        "options": [
            "buy_signal", "sell_signal", "short_signal",
            "price_target_reached", "stop_loss_triggered",
            "high_confidence_signal", "portfolio_threshold"
        ],
        "default": ["buy_signal", "sell_signal"],
        "description": "When to send alerts"
    },
    "time_horizon": {
        "type": "select",
        "options": ["intraday", "short_term", "medium_term", "long_term"],
        "default": "medium_term",
        "description": "Expected holding period for positions",
        "mapping": {
            "intraday": {"days": 0, "lookback": "1mo"},
            "short_term": {"days": 7, "lookback": "3mo"},
            "medium_term": {"days": 30, "lookback": "1y"},
            "long_term": {"days": 365, "lookback": "10y"}
        }
    },
    "fundamental_weight": {
        "type": "number",
        "min": 0.0,
        "max": 1.0,
        "default": 0.3,
        "description": "Weight for fundamental analysis (0=technical only, 1=fundamental only)",
        "step": 0.1
    },
    "technical_weight": {
        "type": "number",
        "min": 0.0,
        "max": 1.0,
        "default": 0.7,
        "description": "Weight for technical analysis (0=none, 1=full)",
        "step": 0.1
    },
    "rebalance_frequency": {
        "type": "select",
        "options": ["daily", "weekly", "monthly", "quarterly"],
        "default": "monthly",
        "description": "How often to review and rebalance portfolio"
    },
    "tax_optimization": {
        "type": "boolean",
        "default": False,
        "description": "Consider tax implications (hold >1 year for tax benefits)"
    },
    "dividend_reinvestment": {
        "type": "boolean",
        "default": True,
        "description": "Automatically reinvest dividends"
    },
    "broker_name": {
        "type": "select",
        "options": [
            "Mandiri Sekuritas", "Mirae Asset Sekuritas", "Indo Premier Sekuritas",
            "BCA Sekuritas", "Trimegah Sekuritas", "Other"
        ],
        "default": "Other",
        "description": "Your broker (for commission calculation)"
    },
    "commission_rate": {
        "type": "number",
        "min": 0.0,
        "max": 1.0,
        "default": 0.15,
        "description": "Broker commission rate (%)",
        "step": 0.01
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
