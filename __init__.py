# Enterprise-grade Stock AI Engine
# Technical Analysis & Trading Decision System
# Ready for institutional integration

__version__ = "1.0.0"
__author__ = "StockAI Engine"
__description__ = "Indicator-based decision engine for institutional trading"

from .engine.decision import decision_engine
from .backtest.simple_backtest import backtest
from .backtest.report import summarize
from .data.fetcher import fetch_eod
from .indicators.technical import add_indicators

__all__ = [
    "decision_engine",
    "backtest",
    "summarize",
    "fetch_eod",
    "add_indicators"
]
