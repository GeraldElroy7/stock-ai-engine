"""
Test Data Comparison: 1-Year vs 10-Year Lookback
Membandingkan kualitas signal dan backtest dengan periode data berbeda
"""

import sys
import pandas as pd
from datetime import datetime, timedelta
from backtest.simple_backtest import backtest
from engine.decision import decision_engine
from indicators.technical import add_indicators
from data.fetcher import fetch_stock_data
import config

# Test stocks - representative dari berbagai sektor
TEST_STOCKS = ["BBCA", "BBRI", "ASII", "TLKM", "UNVR", "ANTM"]

def fetch_with_period(ticker: str, period: str):
    """Fetch data dengan periode tertentu"""
    print(f"  Fetching {ticker} data ({period})...")
    
    # Temporarily modify config
    original_period = config.DATA_CONFIG["LOOKBACK_PERIOD"]
    config.DATA_CONFIG["LOOKBACK_PERIOD"] = period
    
    try:
        data = fetch_stock_data(ticker)
        config.DATA_CONFIG["LOOKBACK_PERIOD"] = original_period
        
        if data is None or data.empty:
            print(f"    ⚠️ No data for {ticker}")
            return None
            
        print(f"    ✅ Got {len(data)} days of data")
        return data
    except Exception as e:
        config.DATA_CONFIG["LOOKBACK_PERIOD"] = original_period
        print(f"    ❌ Error: {e}")
        return None

def compare_signals(ticker: str):
    """Compare signal quality dengan 1-year vs 10-year data"""
    print(f"\n{'='*60}")
    print(f"📊 Testing: {ticker}")
    print(f"{'='*60}")
    
    results = {}
    
    for period in ["1y", "10y"]:
        print(f"\n🔍 Period: {period}")
        data = fetch_with_period(ticker, period)
        
        if data is None:
            results[period] = None
            continue
        
        # Add indicators
        try:
            data_with_indicators = add_indicators(data)
            
            # Generate signal using decision engine
            signal_data = decision_engine(data_with_indicators)
            
            results[period] = {
                "data_points": len(data),
                "signal": signal_data["signal"],
                "score": signal_data.get("score", 0),
                "confidence": signal_data.get("confidence", 0),
                "components": signal_data.get("components", {}),
                "indicators": signal_data.get("indicators", {})
            }
            
            print(f"  Signal: {signal_data['signal']}")
            print(f"  Score: {signal_data.get('score', 0):.2f}")
            print(f"  Confidence: {signal_data.get('confidence', 0):.1f}%")
            
            components = signal_data.get("components", {})
            if components:
                print(f"  Components: Trend={components.get('trend', 0):.1f}, "
                      f"Momentum={components.get('momentum', 0):.1f}, "
                      f"Volume={components.get('volume', 0):.1f}")
            
        except Exception as e:
            print(f"  ❌ Signal error: {e}")
            import traceback
            traceback.print_exc()
            results[period] = None
    
    return results

def compare_backtest(ticker: str):
    """Compare backtest performance"""
    print(f"\n🧪 Backtesting {ticker}")
    print(f"{'-'*60}")
    
    results = {}
    
    for period in ["1y", "10y"]:
        print(f"\n📈 Backtest Period: {period}")
        data = fetch_with_period(ticker, period)
        
        if data is None or len(data) < 100:
            results[period] = None
            continue
        
        try:
            # Add signals to data
            from engine.decision import decision_engine
            from indicators.technical import add_indicators
            
            # Make copy to avoid modifying original
            test_data = data.copy()
            test_data = add_indicators(test_data)
            
            # Generate signals for each row
            signals = []
            for i in range(len(test_data)):
                if i < 50:  # warmup period
                    signals.append({"signal": None, "score": None, "confidence": None})
                else:
                    slice_df = test_data.iloc[:i+1]
                    result = decision_engine(slice_df)
                    signals.append(result)
            
            # Add signals to dataframe
            test_data["signal"] = [s["signal"] for s in signals]
            test_data["score"] = [s["score"] for s in signals]
            test_data["confidence"] = [s["confidence"] for s in signals]
            
            # Run backtest
            backtest_result = backtest(test_data, initial_capital=10_000_000)
            
            if backtest_result and len(backtest_result) > 0:
                total_trades = len(backtest_result)
                winning_trades = sum(1 for t in backtest_result if t.get("pnl", 0) > 0)
                total_pnl = sum(t.get("pnl", 0) for t in backtest_result)
                
                results[period] = {
                    "total_trades": total_trades,
                    "win_rate": (winning_trades / total_trades * 100) if total_trades > 0 else 0,
                    "total_return": (total_pnl / 10_000_000 * 100) if total_pnl else 0,
                    "sharpe_ratio": 0,  # Simplified for now
                    "max_drawdown": 0,
                    "avg_trade_return": (total_pnl / total_trades / 10_000_000 * 100) if total_trades > 0 else 0
                }
                
                print(f"  Total Trades: {total_trades}")
                print(f"  Win Rate: {results[period]['win_rate']:.1f}%")
                print(f"  Total Return: {results[period]['total_return']:.2f}%")
                print(f"  Avg Trade Return: {results[period]['avg_trade_return']:.2f}%")
            else:
                results[period] = None
                print(f"  ⚠️ No trades generated")
                
        except Exception as e:
            print(f"  ❌ Backtest error: {e}")
            import traceback
            traceback.print_exc()
            results[period] = None
    
    return results

def print_comparison_summary(all_results):
    """Print comprehensive comparison summary"""
    print(f"\n\n{'='*80}")
    print(f"📊 COMPARISON SUMMARY: 1-Year vs 10-Year Data")
    print(f"{'='*80}\n")
    
    # Signal comparison
    print("🎯 SIGNAL COMPARISON")
    print(f"{'-'*80}")
    print(f"{'Stock':<10} {'Period':<10} {'Signal':<8} {'Score':<8} {'Confidence':<12} {'Data Points':<12}")
    print(f"{'-'*80}")
    
    for ticker, results in all_results["signals"].items():
        for period, data in results.items():
            if data:
                print(f"{ticker:<10} {period:<10} {data['signal']:<8} "
                      f"{data['score']:<8.2f} {data['confidence']:<12.1f} {data['data_points']:<12}")
    
    # Backtest comparison
    print(f"\n\n📈 BACKTEST PERFORMANCE COMPARISON")
    print(f"{'-'*80}")
    print(f"{'Stock':<10} {'Period':<10} {'Trades':<8} {'Win Rate':<12} {'Return %':<12} {'Sharpe':<10}")
    print(f"{'-'*80}")
    
    for ticker, results in all_results["backtests"].items():
        for period, data in results.items():
            if data:
                print(f"{ticker:<10} {period:<10} {data['total_trades']:<8} "
                      f"{data['win_rate']:<12.1f} {data['total_return']:<12.2f} {data['sharpe_ratio']:<10.2f}")
    
    # Statistical summary
    print(f"\n\n📊 STATISTICAL SUMMARY")
    print(f"{'-'*80}")
    
    # Average metrics
    metrics_1y = {"trades": [], "win_rate": [], "return": [], "sharpe": []}
    metrics_10y = {"trades": [], "win_rate": [], "return": [], "sharpe": []}
    
    for ticker, results in all_results["backtests"].items():
        if results.get("1y"):
            metrics_1y["trades"].append(results["1y"]["total_trades"])
            metrics_1y["win_rate"].append(results["1y"]["win_rate"])
            metrics_1y["return"].append(results["1y"]["total_return"])
            metrics_1y["sharpe"].append(results["1y"]["sharpe_ratio"])
        
        if results.get("10y"):
            metrics_10y["trades"].append(results["10y"]["total_trades"])
            metrics_10y["win_rate"].append(results["10y"]["win_rate"])
            metrics_10y["return"].append(results["10y"]["total_return"])
            metrics_10y["sharpe"].append(results["10y"]["sharpe_ratio"])
    
    if metrics_1y["trades"]:
        print(f"\n1-YEAR DATA AVERAGES:")
        print(f"  Avg Trades: {sum(metrics_1y['trades'])/len(metrics_1y['trades']):.1f}")
        print(f"  Avg Win Rate: {sum(metrics_1y['win_rate'])/len(metrics_1y['win_rate']):.1f}%")
        print(f"  Avg Return: {sum(metrics_1y['return'])/len(metrics_1y['return']):.2f}%")
        print(f"  Avg Sharpe: {sum(metrics_1y['sharpe'])/len(metrics_1y['sharpe']):.2f}")
    
    if metrics_10y["trades"]:
        print(f"\n10-YEAR DATA AVERAGES:")
        print(f"  Avg Trades: {sum(metrics_10y['trades'])/len(metrics_10y['trades']):.1f}")
        print(f"  Avg Win Rate: {sum(metrics_10y['win_rate'])/len(metrics_10y['win_rate']):.1f}%")
        print(f"  Avg Return: {sum(metrics_10y['return'])/len(metrics_10y['return']):.2f}%")
        print(f"  Avg Sharpe: {sum(metrics_10y['sharpe'])/len(metrics_10y['sharpe']):.2f}")
    
    # Recommendation
    print(f"\n\n✨ RECOMMENDATION")
    print(f"{'-'*80}")
    
    if metrics_10y["trades"] and metrics_1y["trades"]:
        win_rate_improvement = (sum(metrics_10y['win_rate'])/len(metrics_10y['win_rate'])) - (sum(metrics_1y['win_rate'])/len(metrics_1y['win_rate']))
        return_improvement = (sum(metrics_10y['return'])/len(metrics_10y['return'])) - (sum(metrics_1y['return'])/len(metrics_1y['return']))
        
        if win_rate_improvement > 5 or return_improvement > 10:
            print("✅ 10-YEAR DATA SHOWS SIGNIFICANT IMPROVEMENT")
            print(f"   - Win Rate: +{win_rate_improvement:.1f}%")
            print(f"   - Return: +{return_improvement:.2f}%")
            print("\n   Recommendation: USE 10-YEAR DATA for better signal quality")
        elif win_rate_improvement < -5 or return_improvement < -10:
            print("⚠️ 1-YEAR DATA PERFORMS BETTER")
            print(f"   - Win Rate: {win_rate_improvement:.1f}%")
            print(f"   - Return: {return_improvement:.2f}%")
            print("\n   Recommendation: KEEP 1-YEAR DATA or investigate 10-year data quality")
        else:
            print("➡️ SIMILAR PERFORMANCE")
            print(f"   - Win Rate Diff: {win_rate_improvement:.1f}%")
            print(f"   - Return Diff: {return_improvement:.2f}%")
            print("\n   Recommendation: 10-YEAR DATA provides more context without sacrificing performance")
    
    print(f"\n{'='*80}\n")

def main():
    """Main testing function"""
    print("\n" + "="*80)
    print("🧪 STOCK AI ENGINE - DATA PERIOD COMPARISON TEST")
    print("="*80)
    print(f"\nTesting {len(TEST_STOCKS)} stocks: {', '.join(TEST_STOCKS)}")
    print(f"Comparing: 1-year vs 10-year historical data")
    print(f"Metrics: Signal quality, Win rate, Return, Sharpe ratio\n")
    
    all_results = {
        "signals": {},
        "backtests": {}
    }
    
    # Test each stock
    for ticker in TEST_STOCKS:
        # Signal comparison
        signal_results = compare_signals(ticker)
        all_results["signals"][ticker] = signal_results
        
        # Backtest comparison
        backtest_results = compare_backtest(ticker)
        all_results["backtests"][ticker] = backtest_results
        
        print(f"\n{'='*60}\n")
    
    # Print comprehensive summary
    print_comparison_summary(all_results)
    
    # Save results to file
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results/data_comparison_{timestamp}.txt"
        
        import os
        os.makedirs("results", exist_ok=True)
        
        with open(filename, "w") as f:
            # Redirect print to file
            original_stdout = sys.stdout
            sys.stdout = f
            print_comparison_summary(all_results)
            sys.stdout = original_stdout
        
        print(f"📁 Results saved to: {filename}")
    except Exception as e:
        print(f"⚠️ Could not save results: {e}")
    
    print("\n✅ Testing complete!")

if __name__ == "__main__":
    main()
