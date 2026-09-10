"""
Analise exploratoria da serie consolidada de caminhoes (ANFAVEA).
Identifica picos, quedas e pontos de inflexao reais na serie -
sem inventar causas: so aponta o que o numero mostra.
"""

import pandas as pd
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "processed" / "anfavea_caminhoes_consolidado.csv"

df = pd.read_csv(DATA)

print("=" * 70)
print("RESUMO GERAL (1957-2025)")
print("=" * 70)
print(df[["Producao", "Exportacao", "Emplacamento"]].describe().round(1))

print("\n" + "=" * 70)
print("MAIORES QUEDAS ANO A ANO - PRODUCAO (top 10)")
print("=" * 70)
quedas_prod = df.nsmallest(10, "Producao_var_pct_aa")[["Ano", "Producao", "Producao_var_pct_aa"]]
print(quedas_prod.to_string(index=False))

print("\n" + "=" * 70)
print("MAIORES ALTAS ANO A ANO - PRODUCAO (top 10)")
print("=" * 70)
altas_prod = df.nlargest(10, "Producao_var_pct_aa")[["Ano", "Producao", "Producao_var_pct_aa"]]
print(altas_prod.to_string(index=False))

print("\n" + "=" * 70)
print("PICOS LOCAIS DE PRODUCAO (ano > ano anterior E > ano seguinte)")
print("=" * 70)
prod = df["Producao"].values
anos = df["Ano"].values
for i in range(1, len(prod) - 1):
    if prod[i] > prod[i - 1] and prod[i] > prod[i + 1]:
        print(f"  Pico em {anos[i]}: {prod[i]:,.0f} unidades "
              f"(vindo de {prod[i-1]:,.0f} em {anos[i-1]}, "
              f"caindo para {prod[i+1]:,.0f} em {anos[i+1]})")

print("\n" + "=" * 70)
print("VALES LOCAIS DE PRODUCAO (ano < ano anterior E < ano seguinte)")
print("=" * 70)
for i in range(1, len(prod) - 1):
    if prod[i] < prod[i - 1] and prod[i] < prod[i + 1]:
        print(f"  Vale em {anos[i]}: {prod[i]:,.0f} unidades "
              f"(vindo de {prod[i-1]:,.0f} em {anos[i-1]}, "
              f"subindo para {prod[i+1]:,.0f} em {anos[i+1]})")

print("\n" + "=" * 70)
print("PARTICIPACAO DA EXPORTACAO NA PRODUCAO - EXTREMOS")
print("=" * 70)
print("Maior dependencia de mercado externo:")
print(df.nlargest(5, "Exportacao_pct_Producao")[["Ano", "Producao", "Exportacao", "Exportacao_pct_Producao"]].to_string(index=False))
print("\nMenor dependencia de mercado externo (entre anos com exportacao registrada):")
print(df.dropna(subset=["Exportacao_pct_Producao"]).nsmallest(5, "Exportacao_pct_Producao")[["Ano", "Producao", "Exportacao", "Exportacao_pct_Producao"]].to_string(index=False))

print("\n" + "=" * 70)
print("CORRELACAO Producao x Exportacao x Emplacamento (niveis, 1965-2025)")
print("=" * 70)
print(df[df["Ano"] >= 1965][["Producao", "Exportacao", "Emplacamento"]].corr().round(3))

print("\n" + "=" * 70)
print("CORRELACAO das VARIACOES ANUAIS (%) - Producao x Exportacao x Emplacamento")
print("=" * 70)
print(df[["Producao_var_pct_aa", "Exportacao_var_pct_aa", "Emplacamento_var_pct_aa"]].corr().round(3))

print("\n" + "=" * 70)
print("MESMA CORRELACAO, POR JANELA DE ANOS (a serie completa e distorcida pelas")
print("decadas de 1960-70, quando a base de exportacao era proxima de zero e")
print("qualquer oscilacao minima virava uma variacao percentual absurda - ex.:")
print("1970 teve +2950% de 'alta', de 4 para 122 unidades)")
print("=" * 70)
cols = ["Producao_var_pct_aa", "Exportacao_var_pct_aa", "Emplacamento_var_pct_aa"]
janelas = [
    ("serie completa", df),
    ("1980-2025", df[df["Ano"] >= 1980]),
    ("2000-2025", df[df["Ano"] >= 2000]),
    ("2010-2025", df[df["Ano"] >= 2010]),
]
for nome, sub in janelas:
    d = sub[cols].dropna()
    c = d.corr()
    print(f"{nome:16s} (n={len(d):2d})  Producao x Emplacamento: {c.loc[cols[0], cols[2]]:.3f}"
          f"   Producao x Exportacao: {c.loc[cols[0], cols[1]]:.3f}")

print("\n" + "=" * 70)
print("ULTIMA DECADA (2016-2025)")
print("=" * 70)
print(df[df["Ano"] >= 2016][["Ano", "Producao", "Exportacao", "Emplacamento", "Exportacao_pct_Producao"]].to_string(index=False))
