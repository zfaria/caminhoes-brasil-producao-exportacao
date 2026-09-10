# Roteiro de construção — Tableau Story: Caminhões do Brasil

Este guia descreve, tela a tela, como montar a Story no Tableau Desktop a partir de quatro
arquivos em [`data/processed/`](../data/processed/):

- `anfavea_caminhoes_consolidado.csv` — uma linha por ano, com métricas derivadas
- `anfavea_caminhoes_longo.csv` — formato tidy anual (`Ano`, `Metrica`, `Valor`), melhor para
  gráficos com as três séries juntas
- `anfavea_caminhoes_mensal_consolidado.csv` — uma linha por mês (`Data`, `Ano`, `Mes`, `MesNome`,
  `AnoCompleto`, + uma coluna por métrica)
- `anfavea_caminhoes_mensal_longo.csv` — formato tidy mensal, para gráficos de sazonalidade

Cada Story Point abaixo tem um **título que já conta parte da história** — não é só o nome da
métrica — seguindo a mesma sequência do README: abertura → desenvolvimento → insight central →
fechamento.

## Conexão dos dados

1. Conectar aos quatro CSVs de `data/processed/` (extract, não live, já que os arquivos não mudam
   com frequência).
2. Em `anfavea_caminhoes_consolidado.csv`, confirmar que `Ano` está como **Data/Discreta** (ano) e
   as demais colunas numéricas como medida contínua.
3. Criar um campo calculado auxiliar `Década` = `STR(INT(([Ano])/10)*10) + "s"` para permitir
   filtros/agrupamentos rápidos por década nas folhas de contexto histórico, se necessário.

## Story Point 1 — "Cada caminhão desse gráfico foi montado por alguém"

**Abertura.** Não é um gráfico ainda — é uma folha de texto/imagem com o gancho pessoal (o mesmo
parágrafo de abertura do README, resumido) e um único número grande: total de caminhões
produzidos no Brasil desde 1957 (soma de `Producao`). Objetivo: estabelecer por que a leitura
importa antes de mostrar qualquer curva.

- Folha: texto formatado (Tableau permite objeto de texto solto no dashboard) + um BAN (big
  number) com `SUM(Producao)` de toda a série.

## Story Point 2 — "Quase 70 anos em uma única curva"

**Desenvolvimento (visão geral).** Gráfico de linha, `Ano` no eixo X, `Producao` no eixo Y,
usando `anfavea_caminhoes_longo.csv` com as três métricas (`Producao`, `Exportacao`,
`Emplacamento`) como linhas separadas (cor = `Metrica`). Isso já deixa visualmente claro que
Produção e Emplacamento andam quase coladas, enquanto Exportação é uma linha mais baixa e mais
estável.

- Anotações fixas no gráfico (Tableau: clique direito no ponto → Annotate → Point) nos 5 pontos de
  inflexão da tabela do README: 1980-82, 2008-09, 2011-12, 2014-16, 2022-23. Texto curto por
  anotação, ex.: "PROCONVE P7 (Euro 5): -40% em 2012".

## Story Point 3 — "Duas vezes em onze anos, a mesma queda de 40%"

**Desenvolvimento (o padrão regulatório).** Gráfico de barras, `Ano` no eixo X (filtrado para
2009-2016 e 2020-2025, ou os dois períodos lado a lado com um parâmetro de seleção), `Producao`
no eixo Y, com destaque de cor nos anos 2011/2012 e 2022/2023 (campo calculado booleano
`[Ano]=2011 OR [Ano]=2012 OR [Ano]=2022 OR [Ano]=2023`).

- Rótulo de dados com `Producao_var_pct_aa` nos anos de queda, para reforçar o "-40,3%" e "-37,9%"
  lado a lado.
- Título já é a conclusão: essa tela existe para o espectador comparar os dois ciclos visualmente
  antes de ler a explicação.

## Story Point 4 — "O ano também tem seu próprio ciclo"

**Desenvolvimento (sazonalidade).** Usar `anfavea_caminhoes_mensal_consolidado.csv`, filtrado por
`AnoCompleto = TRUE` (exclui 2026, ano em curso). Campo calculado `Indice_Sazonal`:

```
SUM([Producao]) / WINDOW_AVG(SUM([Producao]))
```

com Table Calculation computada "ao longo de" `Mes`, particionada por `Ano` (Compute using: Mes,
restart every Ano) — reproduz o mesmo índice do script `eda_sazonalidade.py` (valor do mês ÷ média
dos 12 meses do ano).

- Gráfico de linha ou barras: `MesNome` no eixo X (ordenado Jan→Dez, não alfabético — ajustar em
  "Sort"), `Indice_Sazonal` no eixo Y, uma linha de referência em 1.0.
- Repetir para `Emplacamento` e, em aba/gráfico separado, para `Exportacao` — mas filtrando
  `Ano >= 2001` neste último (ver nota sobre ruído nos anos 1960-80 no README principal).
- Anotação nos meses de Janeiro e Dezembro: "recesso coletivo de fim de ano — vale sazonal em 72%
  dos anos" e em Agosto-Outubro: "pico do ano — renovação de frota + escoamento de safra".

## Story Point 5 — "Quem puxa o ciclo não é quem exporta"

**Insight central.** Dividir em dois gráficos na mesma tela (dashboard com dois objetos):

1. Gráfico de dispersão (scatter): `Producao_var_pct_aa` no eixo X, `Exportacao_var_pct_aa` no
   eixo Y, um ponto por ano — a nuvem de pontos sem padrão linear é a prova visual da correlação
   ≈ 0. Adicionar linha de tendência do Tableau (Analytics → Trend Line) para reforçar que ela é
   praticamente horizontal/sem inclinação.
2. Segundo gráfico: barras de `Exportacao_pct_Producao` por `Ano`, com os anos 2015-2017
   destacados — mostrando que a participação da exportação sobe justamente nos anos de crise
   doméstica, mesmo sem a exportação crescer em volume.

- Texto de apoio na tela com os dois coeficientes de correlação (0,923 vs. 0,003), citados
  diretamente do resultado de [`analysis/eda_caminhoes.py`](../analysis/eda_caminhoes.py).

## Story Point 6 — "O que os dados confirmam de quem já viveu isso por dentro"

**Fechamento.** Volta a ser uma tela de texto/imagem — sem gráfico novo, só a curva completa do
Story Point 2 ao fundo, mais leve — com o parágrafo de fechamento do README conectando o padrão
identificado (dependência do mercado interno + antecipação regulatória como gatilho, e o ritmo
sazonal previsível dentro de cada ano) à experiência prática de chão de fábrica.

## Publicação

1. Salvar como `.twbx` (packaged workbook, para incluir o extract dos dados).
2. Publicar no [Tableau Public](https://public.tableau.com/) (conta gratuita).
3. Colar o link público de volta na seção "Dashboard (Tableau Story)" do README principal.
