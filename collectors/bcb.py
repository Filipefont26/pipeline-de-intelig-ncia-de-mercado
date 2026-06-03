   
import requests, pandas as pd
from datetime import datetime, timedelta

BCB_BASE = "https://api.bcb.gov.br/dados/serie/bcdata.sgs"

SERIES = {
    "selic_diaria": 11,
    "ipca_mensal":  13522,  
    "usd_brl":      1,
    "igpm_mensal":  189,
}

def fetch_bcb_series(series_id: int, days: int = 365) -> pd.DataFrame:
    start = (datetime.today() - timedelta(days=days)).strftime("%d/%m/%Y")
    end   = datetime.today().strftime("%d/%m/%Y")
    url   = f"{BCB_BASE}.{series_id}/dados"
    resp  = requests.get(url, params={
        "formato": "json", "dataInicial": start, "dataFinal": end
    }, timeout=15)
    resp.raise_for_status()
    df = pd.DataFrame(resp.json())        
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["data"]  = pd.to_datetime(df["data"], dayfirst=True)
    df["serie"] = series_id
    return df.dropna()

def collect(days: int = 365) -> pd.DataFrame:   
    frames = []
    for name, sid in SERIES.items():
        df = fetch_bcb_series(sid, days=days)
        df["indicador"] = name
        df["fonte"]     = "BCB"
        frames.append(df)
        print(f"✓ BCB {name}: {len(df)} registros")
    return pd.concat(frames, ignore_index=True)

if __name__ == "__main__":
    df = collect(days=30)
    print("Linhas:", len(df))
    print(df.head(10))