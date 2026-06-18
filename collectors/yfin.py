import yfinance as yf
import pandas as pd


TICKERS = {
    "IBOV": "^BVSP","PETR4": "PETR4.SA", "VALE3": "VALE3.SA", "ITUB4": "ITUB4.SA","SP500": "^GSPC", 
}

def collect(period : str = "1y") -> pd.DataFrame:
    frames = []
    for nome, ticker in TICKERS.items():
        df = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        if df.empty: continue
        df = df.reset_index()
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        df["ativo"] = nome
        df["ticker"] = ticker
        df["retorno_d"] = df["Close"].pct_change().round(6)
        frames.append(df[["Date", "Open", "High", "Low", "Close", "Volume", "ativo", "ticker", "retorno_d"]])
        print(f"✓ YFinance {nome}: {len(df)} pregões")

    return pd.concat(frames, ignore_index=True)
if __name__ == "__main__":
    df = collect()
    print("Linhas:", len(df))
    print(df["ativo"].value_counts())
      