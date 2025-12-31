import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.fetcher import fetch_eod
from indicators.technical import add_indicators
from engine.decision import decision_engine
from backtest.simple_backtest import backtest
from backtest.report import summarize
import pandas as pd


DEFAULT_IHSG = [
    "BBCA","BBRI","BMRI","BBNI","ASII","TLKM","ANTM","INCO","MDKA",
    "ADRO","PGAS","PTBA","BRIS","GOTO","ARTO","UNVR","ICBP","INDF",
    "KLBF","CPIN","SMGR","INTP","ASSA","BUKA","SIDO","HEAL","MTEL","MEDC"
]


def prepare_backtest(df, warmup=50):
    """Runs decision_engine on rolling historical slices and returns df with signal and metadata columns."""
    records = []

    for i in range(len(df)):
        if i < warmup:
            records.append({"signal": None, "score": None, "confidence": None, "reasons": None, "meta": None})
        else:
            temp_df = df.iloc[:i+1]
            decision = decision_engine(temp_df)
            records.append(decision)

    df = df.copy()
    df["signal"] = [r["signal"] for r in records]
    df["signal_score"] = [r.get("score") for r in records]
    df["signal_confidence"] = [r.get("confidence") for r in records]
    df["signal_reasons"] = [json.dumps(r.get("reasons")) if r.get("reasons") is not None else None for r in records]
    df["signal_meta"] = [json.dumps(r.get("meta")) if r.get("meta") is not None else None for r in records]
    return df


def run_for_symbol(symbol, save_trades=False):
    print(f"\n{'='*70}")
    print(f"ANALYZING: {symbol}")
    print(f"{'='*70}")
    
    df = fetch_eod(symbol)
    if df is None or df.empty:
        print(f"❌ No data for {symbol}, skipping.")
        return None

    df = add_indicators(df)
    df = prepare_backtest(df)

    trades = backtest(df)
    report = summarize(trades)

    # ===== INSTITUTIONAL-READY OUTPUT =====
    print(f"\n📊 BACKTEST REPORT: {symbol}")
    print(f"{'─'*70}")
    
    if report.get("total_trades") == 0:
        print("⚠️  No trades generated")
        return None
    
    # Basic metrics
    print(f"Total Trades:         {report.get('total_trades')}")
    print(f"Wins / Losses:        {report.get('wins')} / {report.get('losses')}")
    print(f"Win Rate:             {report.get('win_rate')}%")
    print(f"Avg Return per Trade: {report.get('avg_return_pct')}%")
    
    # Risk metrics
    print(f"\n📈 RISK METRICS:")
    print(f"Max Gain:             {report.get('max_gain_pct')}%")
    print(f"Max Loss:             {report.get('max_loss_pct')}%")
    print(f"Max Drawdown:         {report.get('max_drawdown_pct')}%")
    print(f"Sharpe Ratio:         {report.get('sharpe_ratio')}")
    
    # Robustness metrics
    print(f"\n🛡️  ROBUSTNESS METRICS:")
    print(f"Recovery Factor:      {report.get('recovery_factor')}")
    print(f"Profit Factor:        {report.get('profit_factor')}")
    print(f"Max Consecutive Loss: {report.get('max_consecutive_losses')}")
    print(f"Expectancy:           {report.get('expectancy')}%")
    print(f"Total Profit:         {report.get('total_profit_pct')}%")
    
    # Institutional readiness
    institution_ready = report.get('institution_ready')
    status_icon = "✅" if institution_ready else "🔄"
    print(f"\n{status_icon} INSTITUTIONAL READY: {institution_ready}")
    
    # Sample trades
    if trades:
        print(f"\n📋 FIRST 3 TRADES:")
        for i, t in enumerate(trades[:3], 1):
            print(f"  Trade {i}: Entry={t['entry_price']:.0f} → Exit={t['exit_price']:.0f} | Return={t['return_pct']}%")

    # Save trades to CSV if requested
    if save_trades:
        from pathlib import Path
        import csv
        # Create results directory if it doesn't exist
        results_dir = Path(__file__).parent.parent / "results"
        results_dir.mkdir(exist_ok=True)
        
        out_csv = results_dir / f"trades_{symbol}.csv"
        keys = trades[0].keys() if trades else []
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(keys))
            if keys:
                writer.writeheader()
                writer.writerows(trades)
        print(f"\n💾 Trades exported to: results/trades_{symbol}.csv")

    return {"symbol": symbol, "trades": trades, "report": report}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("symbols", nargs="*", help="Symbols to test (overrides defaults)")
    p.add_argument("--all", action="store_true", help="Run through full IHSG default list")
    p.add_argument("--save", action="store_true", help="Save trades to CSV per symbol")
    args = p.parse_args()

    if args.all:
        symbols = DEFAULT_IHSG
    elif args.symbols:
        symbols = args.symbols
    else:
        symbols = ["BBCA"]  # conservative default

    results = []
    for s in symbols:
        res = run_for_symbol(s, save_trades=args.save)
        if res:
            results.append(res)

    # Aggregate summary
    if results:
        print(f"\n{'='*70}")
        print("📊 PORTFOLIO BACKTEST SUMMARY")
        print(f"{'='*70}")
        
        total_trades = sum(len(r["trades"]) for r in results)
        total_wins = sum(r["report"].get("wins", 0) for r in results)
        total_losses = sum(r["report"].get("losses", 0) for r in results)
        
        avg_win_rate = sum(r["report"].get("win_rate", 0) for r in results) / len(results)
        avg_sharpe = sum(r["report"].get("sharpe_ratio", 0) for r in results) / len(results)
        avg_recovery = sum(r["report"].get("recovery_factor", 0) for r in results) / len(results)
        
        portfolio_return = sum(r["report"].get("total_profit_pct", 0) for r in results)
        
        print(f"\nSymbols Tested:       {len(results)}")
        print(f"Total Trades:         {total_trades}")
        print(f"Portfolio Win/Loss:   {total_wins} / {total_losses}")
        print(f"\nAverage Win Rate:     {round(avg_win_rate, 2)}%")
        print(f"Avg Sharpe Ratio:     {round(avg_sharpe, 2)}")
        print(f"Avg Recovery Factor:  {round(avg_recovery, 2)}")
        print(f"Total Return Pct:     {round(portfolio_return, 2)}%")
        
        # Overall readiness
        ready_count = sum(1 for r in results if r["report"].get("institution_ready"))
        print(f"\n✅ SYMBOLS READY FOR INSTITUTION: {ready_count}/{len(results)}")
        
        if ready_count > 0:
            ready_symbols = [r["symbol"] for r in results if r["report"].get("institution_ready")]
            print(f"   {', '.join(ready_symbols)}")
        
        print(f"{'='*70}")
