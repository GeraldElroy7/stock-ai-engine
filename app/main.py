from data.fetcher import fetch_eod
from indicators.technical import add_indicators
from engine.decision import decision_engine


def run(ticker):
    df = fetch_eod(ticker)
    df = add_indicators(df)
    return decision_engine(df)

if __name__ == "__main__":
    print("=== STOCK AI ENGINE ===")
    print("Ketik ticker (contoh: BBCA)")
    print("Ketik 'exit' untuk keluar\n")

    while True:
        ticker = input("Ticker > ").upper().strip()

        if ticker == "EXIT":
            print("Engine stopped.")
            break

        try:
            result = run(ticker)
            print(result)
            print("-" * 40)
        except Exception as e:
            print("Error:", e)
