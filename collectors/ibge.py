import requests, pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

IBGE_BASE = "https://servicodados.ibge.gov.br/api/v3/agregados"

series_ibge = {

   "ipca_variacao":    {"tab": 1737, "var": 63,   "freq": "M"},
    "ipca_acum_12m":    {"tab": 1737, "var": 2266, "freq": "M"},
    "inpc_variacao":    {"tab": 7060, "var": 63,   "freq": "M"},
    "pib_variacao_trim":{"tab": 5932, "var": 6561, "freq": "Q"},
    "desemprego_pnad":  {"tab": 6381, "var": 4099, "freq": "Q"},  

}

def _periodo(freq, n=12):
    h = datetime.today()
    if freq == "M":
        meses = [(h - relativedelta(months=i)).strftime("%Y%m") for i in range(n, 0, -1)]
        return f"{meses[0]}-{meses[-1]}"
    trimestre_atual = (h.month - 1) // 3 + 1
    return f"{h.year-2}01-{h.year}0{trimestre_atual}"



def collect() -> pd.DataFrame:
    frames = []
    for nome, cfg in series_ibge.items():
        periodo = _periodo(cfg["freq"])
        url = (f"{IBGE_BASE}/{cfg['tab']}/periodos/{periodo}"
               f"/variaveis/{cfg['var']}?localidades=N1[all]&formato=json")
        r = requests.get(url, timeout=20); r.raise_for_status()
        serie = r.json()[0]["resultados"][0]["series"][0]["serie"]
        rows = [{"periodo":k, "valor":v,
                 "indicador":nome, "frequencia":cfg["freq"], "fonte":"IBGE"}
                for k,v in serie.items() if v != "..."]
        frames.append(pd.DataFrame(rows))
        print(f"✓ IBGE {nome}: {len(rows)} períodos")
    df = pd.concat(frames, ignore_index=True)
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    return df.dropna(subset=["valor"])


if __name__ == "__main__":
    df = collect()
    print("Linhas:", len(df))
    print(df["indicador"].value_counts())



            