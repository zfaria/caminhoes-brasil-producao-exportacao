"""
Analise de sazonalidade mensal da producao/exportacao/emplacamento de
caminhoes (ANFAVEA). Usa indice sazonal: Valor do mes / media dos 12 meses
do mesmo ano - isola o padrao de mes dentro do ano, sem efeito de tendencia
de longo prazo (uma serie que cresce 4000% entre 1957 e 2025 nao pode ser
comparada em nivel absoluto entre decadas).
"""

import pandas as pd
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "processed" / "anfavea_caminhoes_mensal_consolidado.csv"

df = pd.read_csv(DATA, parse_dates=["Data"])
df_completo = df[df["AnoCompleto"]].copy()  # exclui 2026 (ano ainda em curso)

MESES_ORDEM = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]

for metrica in ["Producao", "Exportacao", "Emplacamento"]:
    print("=" * 70)
    print(f"SAZONALIDADE - {metrica} (indice: mes / media do ano, 1965-2025 quando aplicavel)")
    print("=" * 70)
    sub = df_completo[["Ano", "Mes", "MesNome", metrica]].dropna(subset=[metrica]).copy()
    media_ano = sub.groupby("Ano")[metrica].transform("mean")
    sub["indice"] = sub[metrica] / media_ano
    resumo = (
        sub.groupby("MesNome")["indice"]
        .agg(["mean", "std", "count"])
        .reindex(MESES_ORDEM)
        .round(3)
    )
    resumo.columns = ["indice_medio", "desvio_padrao", "n_anos"]
    print(resumo.to_string())
    print(f"\nMes historicamente mais forte: {resumo['indice_medio'].idxmax()} "
          f"(indice {resumo['indice_medio'].max():.3f})")
    print(f"Mes historicamente mais fraco: {resumo['indice_medio'].idxmin()} "
          f"(indice {resumo['indice_medio'].min():.3f})")
    print()

print("=" * 70)
print("SAZONALIDADE - Exportacao, ULTIMOS 25 ANOS (2001-2025) - serie mais recente,")
print("menos distorcida por volumes proximos de zero no inicio da serie (anos 1960-80)")
print("=" * 70)
sub = df_completo[(df_completo["Ano"] >= 2001)][["Ano", "Mes", "MesNome", "Exportacao"]].dropna()
media_ano = sub.groupby("Ano")["Exportacao"].transform("mean")
sub["indice"] = sub["Exportacao"] / media_ano
resumo = sub.groupby("MesNome")["indice"].agg(["mean", "std", "count"]).reindex(MESES_ORDEM).round(3)
resumo.columns = ["indice_medio", "desvio_padrao", "n_anos"]
print(resumo.to_string())
print(f"\nMes historicamente mais forte: {resumo['indice_medio'].idxmax()} (indice {resumo['indice_medio'].max():.3f})")
print(f"Mes historicamente mais fraco: {resumo['indice_medio'].idxmin()} (indice {resumo['indice_medio'].min():.3f})")

print("\n" + "=" * 70)
print("QUEDA DEZEMBRO -> JANEIRO (recesso coletivo de fim de ano) - Producao")
print("=" * 70)
prod = df_completo[["Ano", "Mes", "Producao"]].dropna()
dez = prod[prod["Mes"] == 12].set_index("Ano")["Producao"]
jan = prod[prod["Mes"] == 1].set_index("Ano")["Producao"]
jan_seguinte = jan.reindex(dez.index + 1)
jan_seguinte.index = dez.index
queda_pct = ((jan_seguinte - dez) / dez * 100).dropna()
print(f"Media da variacao Dezembro -> Janeiro seguinte, {queda_pct.index.min()}-{queda_pct.index.max()}: "
      f"{queda_pct.mean():.1f}% (desvio padrao {queda_pct.std():.1f} p.p., n={len(queda_pct)} anos)")
print(f"Anos em que Janeiro foi MAIOR que o Dezembro anterior: {(queda_pct > 0).sum()} de {len(queda_pct)}")

print("\n" + "=" * 70)
print("MENOR MES DO ANO - contagem de vezes que cada mes foi o mais fraco do ano (Producao)")
print("=" * 70)
menor_mes_por_ano = prod.loc[prod.groupby("Ano")["Producao"].idxmin()]
contagem = menor_mes_por_ano["Mes"].value_counts().sort_index()
nomes_mes = dict(zip(range(1, 13), MESES_ORDEM))
for mes, cnt in contagem.items():
    print(f"  {nomes_mes[mes]}: {cnt} anos")
