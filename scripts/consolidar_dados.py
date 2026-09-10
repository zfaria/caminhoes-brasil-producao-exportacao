"""
Consolida as series historicas anuais e mensais da ANFAVEA (Producao,
Exportacao, Emplacamento) de caminhoes em datasets tidy, prontos para Tableau.

Fonte: ANFAVEA - Associacao Nacional dos Fabricantes de Veiculos Automotores
       anfavea.com.br/site/edicoes-em-excel/
"""

import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "Producao": "anfavea_2026-09-10-PRODUCAO.csv",
    "Exportacao": "anfavea_2026-09-10-EXPORTACAO.csv",
    "Emplacamento": "anfavea_2026-09-10-EMPLACAMENTO.csv",
}

FILES_MENSAL = {
    "Producao": "anfavea_2026-09-10-PRODUCAO-MENSAL.csv",
    "Exportacao": "anfavea_2026-09-10-EXPORTACAO-MENSAL.csv",
    "Emplacamento": "anfavea_2026-09-10-EMPLACAMENTO-MENSAL.csv",
}

MESES = {
    "JAN": 1, "FEV": 2, "MAR": 3, "ABR": 4, "MAI": 5, "JUN": 6,
    "JUL": 7, "AGO": 8, "SET": 9, "OUT": 10, "NOV": 11, "DEZ": 12,
}


def ler_serie_mensal(nome_metrica: str, arquivo: str) -> pd.DataFrame:
    """Le um CSV mensal da ANFAVEA (Periodo = 'AAAA - MES') e retorna
    um DataFrame tidy: Ano, Mes, MesNome, Data, Metrica, Valor."""
    caminho = RAW_DIR / arquivo
    df = pd.read_csv(
        caminho,
        sep=";",
        skiprows=1,
        encoding="utf-8-sig",
        dtype={"Período": str},
    )
    df = df.rename(columns={"Período": "Periodo", "CAMINHÕES": "Valor"})
    partes = df["Periodo"].str.split(" - ", expand=True)
    df["Ano"] = partes[0].astype(int)
    df["MesNome"] = partes[1].str.strip()
    df["Mes"] = df["MesNome"].map(MESES)
    df["Data"] = pd.to_datetime(
        df["Ano"].astype(str) + "-" + df["Mes"].astype(str) + "-01"
    )
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
    df["Metrica"] = nome_metrica
    return df[["Data", "Ano", "Mes", "MesNome", "Metrica", "Valor"]]


def ler_serie(nome_metrica: str, arquivo: str) -> pd.DataFrame:
    """Le um CSV anual da ANFAVEA (titulo na linha 1, cabecalho na linha 2)
    e retorna um DataFrame tidy: Ano, Metrica, Valor."""
    caminho = RAW_DIR / arquivo
    df = pd.read_csv(
        caminho,
        sep=";",
        skiprows=1,          # pula a linha de titulo (ex: "Producao de Caminhoes")
        encoding="utf-8-sig",
        dtype={"Período": str},
    )
    df = df.rename(columns={"Período": "Ano", "CAMINHÕES": "Valor"})
    df["Ano"] = df["Ano"].astype(int)
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
    df["Metrica"] = nome_metrica
    return df[["Ano", "Metrica", "Valor"]]


def main():
    series = [ler_serie(nome, arq) for nome, arq in FILES.items()]

    # --- formato longo (tidy) - ideal para Tableau ---
    long_df = pd.concat(series, ignore_index=True).sort_values(["Metrica", "Ano"])

    # checagem de integridade: nenhum ano duplicado dentro da mesma metrica
    dup = long_df.duplicated(subset=["Metrica", "Ano"]).sum()
    assert dup == 0, f"{dup} linhas duplicadas encontradas"

    long_df.to_csv(OUT_DIR / "anfavea_caminhoes_longo.csv", index=False, encoding="utf-8-sig")

    # --- formato largo (uma coluna por metrica) - conveniente para analise ---
    wide_df = long_df.pivot(index="Ano", columns="Metrica", values="Valor").reset_index()
    wide_df = wide_df.sort_values("Ano").reset_index(drop=True)

    # metricas derivadas (calculadas so onde ha dado real nos dois lados)
    wide_df["Exportacao_pct_Producao"] = (
        wide_df["Exportacao"] / wide_df["Producao"] * 100
    ).round(2)
    wide_df["Emplacamento_pct_Producao"] = (
        wide_df["Emplacamento"] / wide_df["Producao"] * 100
    ).round(2)
    wide_df["Producao_var_pct_aa"] = wide_df["Producao"].pct_change().mul(100).round(2)
    wide_df["Exportacao_var_pct_aa"] = wide_df["Exportacao"].pct_change().mul(100).round(2)
    wide_df["Emplacamento_var_pct_aa"] = wide_df["Emplacamento"].pct_change().mul(100).round(2)

    wide_df.to_csv(OUT_DIR / "anfavea_caminhoes_consolidado.csv", index=False, encoding="utf-8-sig")

    print("Anos cobertos por metrica (serie anual):")
    for nome in FILES:
        sub = long_df[long_df["Metrica"] == nome]["Ano"]
        print(f"  {nome}: {sub.min()}-{sub.max()} ({sub.nunique()} anos)")

    # --- series mensais ---
    mensal = pd.concat(
        [ler_serie_mensal(nome, arq) for nome, arq in FILES_MENSAL.items()],
        ignore_index=True,
    ).sort_values(["Metrica", "Data"])

    dup_m = mensal.duplicated(subset=["Metrica", "Data"]).sum()
    assert dup_m == 0, f"{dup_m} linhas mensais duplicadas encontradas"

    # 2026 ainda nao fechou o ano nas series anuais (ultimo ano anual = 2025);
    # marca meses de anos incompletos para nao distorcer medias de sazonalidade
    ultimo_ano_completo = int(long_df["Ano"].max())
    mensal["AnoCompleto"] = mensal["Ano"] <= ultimo_ano_completo

    mensal.to_csv(OUT_DIR / "anfavea_caminhoes_mensal_longo.csv", index=False, encoding="utf-8-sig")

    mensal_wide = mensal.pivot_table(
        index=["Data", "Ano", "Mes", "MesNome", "AnoCompleto"],
        columns="Metrica",
        values="Valor",
    ).reset_index().sort_values("Data")
    mensal_wide.to_csv(OUT_DIR / "anfavea_caminhoes_mensal_consolidado.csv", index=False, encoding="utf-8-sig")

    print("\nPeriodo coberto por metrica (serie mensal):")
    for nome in FILES_MENSAL:
        sub = mensal[mensal["Metrica"] == nome]["Data"]
        print(f"  {nome}: {sub.min().strftime('%Y-%m')} a {sub.max().strftime('%Y-%m')} ({sub.nunique()} meses)")

    print(f"\nArquivos gerados em {OUT_DIR}:")
    print("  anfavea_caminhoes_longo.csv               (anual, tidy: Ano, Metrica, Valor)")
    print("  anfavea_caminhoes_consolidado.csv         (anual, largo + metricas derivadas)")
    print("  anfavea_caminhoes_mensal_longo.csv        (mensal, tidy: Data, Metrica, Valor)")
    print("  anfavea_caminhoes_mensal_consolidado.csv  (mensal, largo)")


if __name__ == "__main__":
    main()
