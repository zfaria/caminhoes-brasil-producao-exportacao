# Roteiro de construção — Tableau Story: Caminhões do Brasil

Este guia descreve, tela a tela, como montar a Story no Tableau Desktop a partir de
[`data/processed/anfavea_caminhoes_consolidado.csv`](../data/processed/anfavea_caminhoes_consolidado.csv)
(uma linha por ano) e [`anfavea_caminhoes_longo.csv`](../data/processed/anfavea_caminhoes_longo.csv)
(formato tidy: `Ano`, `Metrica`, `Valor` — melhor para gráficos com as três séries juntas).

Cada Story Point abaixo tem um **título que já conta parte da história** — não é só o nome da
métrica — seguindo a mesma sequência do README: abertura → desenvolvimento → insight central →
fechamento.

## Conexão dos dados

1. Conectar aos dois CSVs de `data/processed/` (extract, não live, já que os arquivos não mudam
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

## Story Point 4 — "Quem puxa o ciclo não é quem exporta"

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

## Story Point 5 — "O que os dados confirmam de quem já viveu isso por dentro"

**Fechamento.** Volta a ser uma tela de texto/imagem — sem gráfico novo, só a curva completa do
Story Point 2 ao fundo, mais leve — com o parágrafo de fechamento do README conectando o padrão
identificado (dependência do mercado interno + antecipação regulatória como gatilho) à experiência
prática de chão de fábrica.

## Publicação

1. Salvar como `.twbx` (packaged workbook, para incluir o extract dos dados).
2. Publicar no [Tableau Public](https://public.tableau.com/) (conta gratuita).
3. Colar o link público de volta na seção "Dashboard (Tableau Story)" do README principal.

## Pendência

Quando as planilhas mensais da ANFAVEA forem incorporadas (ver nota no topo do README principal),
adicionar um Story Point extra entre o 2 e o 3 mostrando sazonalidade mensal (ex.: gráfico de
linha com `Mês` no eixo X e uma linha por ano, ou heatmap Ano × Mês) — só depois que os dados
mensais reais estiverem consolidados em `data/processed/`.
