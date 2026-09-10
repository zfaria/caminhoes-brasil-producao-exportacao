"""
Consolida as series historicas anuais da ANFAVEA (Producao, Exportacao,
Emplacamento) de caminhoes em um unico dataset tidy, pronto para Tableau.

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

    print("Anos cobertos por metrica:")
    for nome in FILES:
        sub = long_df[long_df["Metrica"] == nome]["Ano"]
        print(f"  {nome}: {sub.min()}-{sub.max()} ({sub.nunique()} anos)")

    print(f"\nArquivos gerados em {OUT_DIR}:")
    print("  anfavea_caminhoes_longo.csv        (formato tidy: Ano, Metrica, Valor)")
    print("  anfavea_caminhoes_consolidado.csv  (formato largo + metricas derivadas)")


if __name__ == "__main__":
    main()
