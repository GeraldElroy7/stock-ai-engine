import pandas as pd
import numpy as np


def summarize(trades, initial_capital=100_000_000):
    """
    Generate comprehensive backtest report with institutional-grade metrics.
    
    Metrics include:
    - Win rate, avg return, max gain/loss (basic)
    - Sharpe ratio, max drawdown (risk-adjusted)
    - Recovery factor, profit factor (robustness)
    - Consecutive losses (psychological limit)
    - Expectancy (edge verification)
    
    Args:
        trades: List of trade dictionaries with entry/exit prices and returns
        initial_capital: Starting capital for drawdown calculation
    
    Returns:
        dict with comprehensive performance metrics
    """
    if len(trades) == 0:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "avg_return_pct": 0,
            "max_gain_pct": 0,
            "max_loss_pct": 0,
            "sharpe_ratio": 0,
            "max_drawdown_pct": 0,
            "recovery_factor": 0,
            "profit_factor": 0,
            "consecutive_losses": 0,
            "expectancy": 0,
            "message": "No trades generated"
        }
    
    df = pd.DataFrame(trades)
    returns = df["return_pct"].values
    
    # ===== BASIC METRICS =====
    total_trades = len(df)
    wins = (returns > 0).sum()
    losses = (returns < 0).sum()
    win_rate = wins / total_trades if total_trades > 0 else 0
    
    avg_return = returns.mean()
    max_gain = returns.max()
    max_loss = returns.min()
    
    # ===== SHARPE RATIO (Risk-adjusted return) =====
    # Assuming risk-free rate = 0 for simplicity
    if len(returns) > 1:
        sharpe_ratio = (avg_return / returns.std()) if returns.std() > 0 else 0
    else:
        sharpe_ratio = 0
    
    # ===== MAX DRAWDOWN =====
    cumulative_pnl = [0]
    running_pnl = 0
    for ret in returns:
        running_pnl += ret
        cumulative_pnl.append(running_pnl)
    
    cumulative_pnl = np.array(cumulative_pnl)
    running_max = np.maximum.accumulate(cumulative_pnl)
    drawdown = cumulative_pnl - running_max
    max_drawdown = drawdown.min() if len(drawdown) > 0 else 0
    max_drawdown_pct = (max_drawdown / running_max[-1] * 100) if running_max[-1] != 0 else 0
    
    # ===== RECOVERY FACTOR =====
    total_profit = returns.sum()
    recovery_factor = total_profit / abs(max_drawdown) if max_drawdown != 0 else 0
    
    # ===== PROFIT FACTOR =====
    gross_profit = returns[returns > 0].sum() if len(returns[returns > 0]) > 0 else 0
    gross_loss = abs(returns[returns < 0].sum()) if len(returns[returns < 0]) > 0 else 0
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
    
    # ===== CONSECUTIVE LOSSES =====
    consecutive_losses = 0
    max_consecutive_losses = 0
    for ret in returns:
        if ret < 0:
            consecutive_losses += 1
            max_consecutive_losses = max(max_consecutive_losses, consecutive_losses)
        else:
            consecutive_losses = 0
    
    # ===== EXPECTANCY (Edge verification) =====
    avg_win = returns[returns > 0].mean() if len(returns[returns > 0]) > 0 else 0
    avg_loss = returns[returns < 0].mean() if len(returns[returns < 0]) > 0 else 0
    expectancy = (win_rate * avg_win) + ((1 - win_rate) * avg_loss)
    
    return {
        "total_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "win_rate": round(win_rate * 100, 2),
        "avg_return_pct": round(avg_return, 2),
        "max_gain_pct": round(max_gain, 2),
        "max_loss_pct": round(max_loss, 2),
        
        # Risk-adjusted metrics
        "sharpe_ratio": round(sharpe_ratio, 2),
        "max_drawdown_pct": round(max_drawdown_pct, 2),
        "recovery_factor": round(recovery_factor, 2),
        "profit_factor": round(profit_factor, 2),
        
        # Robustness metrics
        "max_consecutive_losses": max_consecutive_losses,
        "expectancy": round(expectancy, 2),
        "total_profit_pct": round(total_profit, 2),
        
        # Institutional note
        "institution_ready": win_rate >= 0.55 and recovery_factor >= 2.0
    }

