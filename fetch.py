import yfinance as yf

def fetch_eod(ticker):
    df = yf.download(f"{ticker}.JK", period="6mo")

    # 🔥 FLATTEN CLOSE COLUMN
    if isinstance(df["Close"], type(df)):
        df["Close"] = df["Close"].iloc[:, 0]


    return df
