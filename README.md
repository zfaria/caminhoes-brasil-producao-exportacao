# Caminhões do Brasil: Produção, Exportação e os Ciclos de um Mercado Interno

Análise de dados públicos da ANFAVEA (1957–2025) sobre produção, exportação e emplacamento
(vendas internas) de caminhões no Brasil — construída por alguém que passou os últimos 4+
anos montando os caminhões que estão dentro desses números.

---

## Por que caminhão, por que eu

Caminhão não é um produto de prateleira — é o meio pelo qual quase tudo que se consome no
Brasil chega a algum lugar: o modal rodoviário responde por cerca de 61% da
[matriz de transporte de cargas do país, segundo a CNT](https://data.cnt.org.br/en/) (Confederação
Nacional do Transporte). Quando
a produção de caminhões sobe ou cai 40% em um único ano, como os dados abaixo mostram que já
aconteceu **cinco vezes** desde 1957, isso não é uma linha de gráfico — é linha de montagem
parando ou trabalhando em três turnos, é fornecedor sendo chamado ou dispensado, é gente sendo
contratada ou mandada embora.

Passei mais de 4 anos na Scania Latin America, na linha de montagem de caminhões pesados. Vi de
dentro o que os números da ANFAVEA registram de fora: os ciclos de alta que exigem hora extra e
contratação emergencial, e as retrações que esvaziam a fábrica. Esse projeto nasce dessa vivência
— não para confirmar o que eu já "sentia" no chão de fábrica, mas para testar isso contra os dados
públicos e reais da indústria, sem inventar número ou causa que a série não sustente.

## Fonte dos dados

- **ANFAVEA** (Associação Nacional dos Fabricantes de Veículos Automotores) — [Edições em Excel](https://anfavea.com.br/site/edicoes-em-excel/)
- Seis séries, categoria **Caminhões**, extraídas em 10/09/2026 — anuais (1957/1965–2025) e
  mensais (1957/1965 – ago/2026, com 2026 ainda em curso):
  - `PRODUCAO` — anual 1957–2025 (69 anos) · mensal jan/1957–ago/2026
  - `EMPLACAMENTO` — anual 1957–2025 (69 anos) · mensal jan/1957–ago/2026 — proxy oficial da ANFAVEA para vendas no mercado interno
  - `EXPORTACAO` — anual 1965–2025 (61 anos; a ANFAVEA não reporta exportação de caminhões antes de 1965) · mensal jan/1965–ago/2026
- Arquivos originais em [`data/raw/`](data/raw/), sem qualquer alteração de conteúdo. 2026 é
  tratado como ano incompleto (8 meses) em todas as análises de sazonalidade, para não distorcer
  a média histórica.

Todos os números citados neste README vêm diretamente dessas três séries ou de fontes públicas
explicitamente linkadas na seção [Fontes das causas apontadas](#fontes-das-causas-apontadas-para-os-pontos-de-inflexão).
Nenhuma tendência, número ou causa foi presumida sem essa base.

## Metodologia

1. **Consolidação** ([`scripts/consolidar_dados.py`](scripts/consolidar_dados.py)): lê os três CSVs
   brutos (separador `;`, linha de título antes do cabeçalho, encoding UTF-8 com BOM), padroniza
   nomes de colunas e período, e gera dois datasets tidy em [`data/processed/`](data/processed/):
   - `anfavea_caminhoes_longo.csv` — formato longo (`Ano`, `Metrica`, `Valor`), pronto para gráficos com as três séries juntas
   - `anfavea_caminhoes_consolidado.csv` — formato largo com métricas derivadas: participação da
     exportação/emplacamento na produção (%) e variação percentual ano a ano de cada série
2. **Checagem de integridade**: nenhum ano duplicado por métrica; conversão numérica com validação
   de tipo (`Ano` como inteiro, `Valor` como numérico).
3. **Exploração anual** ([`analysis/eda_caminhoes.py`](analysis/eda_caminhoes.py)): identifica
   picos e vales locais na série de produção (ano estritamente maior/menor que o anterior e o
   seguinte), maiores variações ano a ano, extremos de participação da exportação e correlações
   entre as três séries — em nível e em variação percentual anual.
4. **Sazonalidade mensal** ([`analysis/eda_sazonalidade.py`](analysis/eda_sazonalidade.py)): calcula
   um índice sazonal por mês (valor do mês ÷ média dos 12 meses do mesmo ano), o que isola o
   padrão de calendário sem o efeito de tendência de longo prazo — necessário numa série cuja
   produção anual do pico de 2011 é ~13,7 vezes a de 1957 (16.259 → 223.602 unidades).

Para reproduzir:

```bash
python -m pip install pandas numpy
python scripts/consolidar_dados.py
python analysis/eda_caminhoes.py
python analysis/eda_sazonalidade.py
```

## A curva: quase 70 anos em cinco movimentos

A produção de caminhões no Brasil não cresce em linha reta — ela sobe e desaba em ciclos
abruptos, quase sempre de dois dígitos percentuais em um único ano. Os dados mostram picos e
vales locais em praticamente metade dos 69 anos da série. Cinco desses movimentos concentram os
maiores saltos e quedas. Duas dessas causas citam o **PROCONVE** (Programa de Controle da Poluição
do Ar por Veículos Automotores) — o programa brasileiro que define, em fases (P1 a P8), os limites
máximos de poluentes (NOx e material particulado) para motores novos, seguindo aproximadamente o
mesmo cronograma das normas europeias Euro: **P7 (2012) equivale ao Euro 5**, **P8 (2023) equivale
ao Euro 6**.

| Período | Produção (unid.) | Variação | O que os dados públicos apontam como causa |
|---|---|---|---|
| 1980 → 1982 | 97.463 → 44.000 | **-33% em 2 anos** | Crise da dívida externa: choque de juros internacionais, recessão mundial e moratória do México (ago/1982) cortaram o crédito externo do Brasil e derrubaram a produção industrial do país¹ |
| 2008 → 2009 | 163.757 → 120.994 | **-26,1%** | Crise financeira global; exportações da indústria automotiva caíram 52% no 1º trimestre de 2009² |
| **2011 → 2012** | 223.602 (recorde histórico) → 133.403 | **-40,3%** | Antecipação de compras em 2011 para escapar do aumento de custo do PROCONVE P7 (Euro 5), obrigatório a partir de jan/2012 — produção de caminhões pesados caiu 37% no período jan-set/2012 vs. igual período de 2011³ |
| 2014 → 2016 | 139.965 → 60.482 | **-56,8% em 2 anos** | Recessão de 2015-2016: dois anos seguidos de PIB negativo, juros subindo de ~8-10% (2013) para mais de 14% (2016), desemprego saltando de 7% para acima de 11%⁴ |
| **2022 → 2023** | 161.992 → 100.535 | **-37,9%** | Mesmo padrão de 2011-2012, uma década depois: antecipação de compras antes do PROCONVE P8 (Euro 6), obrigatório a partir de jan/2023, que elevou custos em ~30%; 2023 começou com 68 mil caminhões P7 em estoque no mercado⁵ |

O padrão regulatório de 2011-2012 e 2022-2023 é o achado mais nítido da série: **duas vezes em
onze anos**, uma mudança na legislação de emissões (PROCONVE P7 e depois P8/Euro 6) gerou o mesmo
comportamento — pico de produção no ano anterior à nova norma, seguido de queda de praticamente
40% no ano em que ela entra em vigor. Não é coincidência de mercado; é reação previsível a uma
data de corte regulatória conhecida com antecedência.

A recuperação também é rápida quando o gatilho é reduzido demanda reprimida: depois da queda mais
branda de 2020 (-19,9%, amortecida pelo agronegócio e e-commerce, que sustentaram a demanda por
caminhões mais do que outros segmentos automotivos durante a pandemia⁶), 2021 veio com alta de
**+74,6%** — a segunda maior expansão anual da série inteira, atrás apenas de 2010 (pós-crise de
2008/09, +57,0%).

## Dentro do ano: o ritmo previsível por trás dos ciclos

Além dos ciclos de anos, existe um ciclo menor que se repete dentro de cada ano — e que qualquer
um que já trabalhou numa linha de montagem reconhece: o calendário de produção não é plano.

Calculando um índice sazonal por mês (valor do mês dividido pela média dos 12 meses do mesmo ano) é
possível isolar o padrão de calendário do crescimento de longo prazo da série — sem isso, comparar
"janeiro de 1960" com "janeiro de 2020" em unidades absolutas não diria nada sobre sazonalidade, só
sobre o quanto a indústria cresceu entre as duas datas. Na prática, o índice funciona como um "% em
relação à média do próprio ano": um índice de **0,82** em janeiro significa que aquele mês produz,
em média, **18% a menos** do que a média dos 12 meses daquele ano; um índice de **1,12** em outubro
significa **12% a mais**. Aplicando esse cálculo, o padrão é o mesmo nas três métricas — produção,
emplacamento e exportação:

| | Mês mais fraco (índice) | Mês mais forte (índice) |
|---|---|---|
| Produção (1957-2025) | Janeiro (0,82) | Outubro (1,12) |
| Emplacamento (1957-2025) | Janeiro (0,84) | Agosto (1,10) |
| Exportação (2001-2025)* | Janeiro (0,59) | Outubro (1,17) |

Janeiro é o mês mais fraco do ano em **26 dos 69 anos** da série, e Dezembro em outros **23** — juntos,
Dezembro e Janeiro concentram o vale sazonal em **71% dos anos** da série. Isso bate com uma
prática real da indústria automotiva brasileira, que eu vivenciei em primeira mão: o **recesso
coletivo de fim de ano** — férias coletivas e parada de linha entre o fim de dezembro e o início
de janeiro, geralmente coincidindo com balanço de estoque e, em alguns anos, transição de ano-modelo.
A produção então acelera ao longo do ano, atingindo o pico entre agosto e outubro — período que
historicamente concentra tanto a renovação de frota antes do fim do ano quanto a demanda logística
ligada à safra agrícola de exportação (soja e milho, que dependem fortemente de transporte
rodoviário no escoamento).

\* A série de exportação mensal completa (1965-2025) tem índice extremamente ruidoso nas décadas de
1960-80, quando os volumes mensais de exportação eram próximos de zero (às vezes 0-3 unidades/mês)
e qualquer variação pequena gera índices desproporcionais. Por isso a leitura de sazonalidade de
exportação usa a janela mais recente e mais representativa do padrão atual (2001-2025); os dados
completos seguem disponíveis em [`data/processed/anfavea_caminhoes_mensal_consolidado.csv`](data/processed/anfavea_caminhoes_mensal_consolidado.csv).

## Insight central: o mercado interno sempre decidiu o ciclo — mas a exportação parou de ser irrelevante

A pergunta óbvia para uma indústria que exporta caminhões é: os ciclos de alta e baixa vêm da
demanda externa? A primeira leitura dos dados sugeriria que não, quase por completo — mas essa
leitura inicial escondia um artefato estatístico que só apareceu ao investigar mais a fundo, e vale
registrar o processo, não só a conclusão final.

Em nível (quanto se produz, exporta e vende internamente a cada ano, 1965-2025), produção e
emplacamento (mercado interno) têm correlação de **0,972**, enquanto produção e exportação
correlacionam bem menos: **0,751**. Até aqui, nenhuma surpresa — a maior parte do que se produz é
vendido no Brasil.

O teste mais rigoroso é a correlação da **variação percentual ano a ano** — não "o quanto se
produz", mas "o quanto o mercado oscila de um ano para o outro". Rodada sobre a série inteira
(1966-2025), essa correlação despenca para **0,003** entre produção e exportação — praticamente
zero — contra **0,923** entre produção e emplacamento. À primeira vista, isso sugeriria que a
exportação é um fluxo totalmente desconectado dos ciclos domésticos.

Mas esse quase-zero é um artefato de base pequena, não um sinal real: nas décadas de 1960-70 o
volume de exportação de caminhões era tão baixo (às vezes 3 a 9 unidades por ano) que qualquer
oscilação mínima virava uma variação percentual absurda — em 1970, a exportação foi de 4 para 122
unidades, uma "alta" de **+2.950%** que não representa nada além do tamanho ínfimo da base. Esses
outliers de décadas em que a exportação ainda não existia como mercado relevante dominam a
correlação da série inteira e escondem o padrão real.

Restringindo a mesma correlação a janelas onde a exportação já tinha uma base minimamente
relevante, o quadro muda — e de forma consistente e crescente:

| Janela | Produção × Emplacamento | Produção × Exportação |
|---|---|---|
| 1958/66–2025 (série completa) | 0,910 | 0,003 |
| 1980–2025 | 0,899 | 0,430 |
| 2000–2025 | 0,850 | 0,508 |
| 2010–2025 | 0,844 | 0,575 |

Duas coisas ficam claras ao mesmo tempo: o mercado interno **sempre foi e continua sendo** o que
mais dita o tamanho do ciclo de produção — sua correlação fica estável entre 0,84 e 0,91 em
qualquer janela. E a exportação **deixou de ser um fluxo desconectado**: à medida que o mercado
externo amadureceu, seus movimentos passaram a acompanhar cada vez mais os da produção total —
mas, mesmo na janela mais recente (2010-2025), ainda com bem menos força (0,575) do que o mercado
doméstico (0,844).

Isso também explica um padrão visível nos anos de crise doméstica: a participação da exportação na
produção total **atinge seus maiores valores exatamente nos anos de colapso do mercado interno**
(35,6% em 2016 e 34,0% em 2017, os dois maiores picos da série, bem acima da média histórica de
13,3%). Em números absolutos a exportação não necessariamente cresce nesses anos — ela cai menos do
que a produção total, funcionando como amortecedor parcial para os fabricantes justamente quando o
mercado interno mais precisa de alívio, sem no entanto ser, ainda hoje, a força que mais dita o
tamanho do ciclo.

## O que isso significa pra quem já viveu por dentro

Cada linha desse dataset que despenca 30, 40, quase 50% em um único ano tem um equivalente
concreto no chão de fábrica: turnos cancelados, linha rodando mais devagar, fornecedores
reprogramando entregas. E cada recuperação de +40%, +57%, +74% também tem o seu — hora extra,
contratação às pressas, pressão para entregar o que ficou represado. Trabalhar dentro desse
setor por mais de quatro anos não me deu acesso a nenhum dado que não esteja aqui; me deu a
referência para reconhecer, nos números, o motivo de cada virada de ciclo que meus colegas de
linha sentiam antes de qualquer manchete confirmar.

O padrão mais útil que os dados revelam — dependência maior do mercado interno do que do externo
como motor do ciclo (ainda que a exportação venha ganhando peso), e antecipação regulatória como
gatilho recorrente e previsível de queda — é
exatamente o tipo de leitura que interessa a quem planeja produção, estoque e contratação num
ambiente industrial: a próxima mudança de norma de emissões (ou de crédito, ou de juros) vale
mais como sinal de alerta do que qualquer expectativa isolada de mercado externo.

## Estrutura do repositório

```
├── data/
│   ├── raw/                      CSVs originais da ANFAVEA, anuais e mensais (não editados)
│   └── processed/                Datasets consolidados (anual e mensal, longo e largo) prontos para análise
├── scripts/
│   └── consolidar_dados.py       Limpeza e consolidação das 6 séries (3 anuais + 3 mensais)
├── analysis/
│   ├── eda_caminhoes.py          Picos, vales, variações e correlações (anual)
│   └── eda_sazonalidade.py       Índice sazonal mensal e recesso de fim de ano
├── docs/
│   └── index.html                Dashboard interativo (HTML/SVG puro, sem dependências), 6 telas — servido via GitHub Pages
└── README.md
```

## Dashboard

**[Ver o dashboard ao vivo](https://zfaria.github.io/caminhoes-brasil-producao-exportacao/)** (GitHub Pages)
— também disponível como [Claude Artifact](https://claude.ai/code/artifact/d19aa6c8-4d74-4303-a74a-a15b88e1fca2).

O dashboard é uma página HTML/SVG standalone em [`docs/index.html`](docs/index.html), sem nenhuma
dependência externa. Segue a mesma narrativa deste README (abertura → evolução → padrão regulatório
→ sazonalidade → insight central → fechamento) em 6 telas navegáveis, com os gráficos reais (linha,
barras, dispersão), legendas clicáveis, tooltips e tabela de dados por trás de cada gráfico.

Para rodar localmente: baixe o arquivo e abra direto no navegador, ou sirva a pasta
(`python -m http.server`, por exemplo) e acesse `docs/index.html`.

## Fontes das causas apontadas para os pontos de inflexão

Toda causa citada na seção "A curva" veio de reportagem ou documento público, nunca de suposição:

1. Crise da dívida externa (1980-82): [Blog do Desenvolvimento – BNDES](https://blogdodesenvolvimento.bndes.gov.br/serie/eventos/1983-1992-crise-da-divida-externa-alta-da-inflacao-e-Estado-de-bem-estar-social/); [SciELO – Recessão e taxa de juros nos anos 1980](https://www.scielo.br/j/rep/a/pNSndMyzFPCpJZyQzNDs97Q/?lang=pt)
2. Crise financeira 2008-09: [Correio Braziliense – Em 2009, produção cai mas vendas aumentam](https://www.correiobraziliense.com.br/app/noticia/economia/2010/01/08/internas_economia,165141/em-2009-producao-da-industria-automotiva-cai-mas-vendas-aumentam.shtml)
3. PROCONVE P7 / antecipação 2011-12: [Revista MT – O peso para as construtoras](https://revistamt.com.br/Materias/Exibir/o-peso-para-as-construtoras); [Anfavea – Cartilha PROCONVE P7](https://anfavea.com.br/docs/cartilha_proconveP7.pdf)
4. Recessão 2015-16: [McKinsey Brasil – O que aconteceu com a indústria automotiva no Brasil](https://www.mckinsey.com/br/our-insights/blog-made-in-brazil/o-que-aconteceu-com-a-industria-automotiva-no-brasil)
5. PROCONVE P8 / Euro 6 / antecipação 2022-23: [AutoIndústria – Proconve P8 limitou desempenho do segmento de caminhões em 2023](https://www.autoindustria.com.br/2024/01/10/proconve-p8-limitou-desempenho-do-segmento-de-caminhoes-em-2023/); [Portal da Autopeça – Produção de caminhões despenca quase 40% com Euro 6](https://portaldaautopeca.com.br/noticias/local/producao-de-caminhoes-despenca-quase-40-com-euro-6/)
6. Pandemia 2020 / recuperação 2021: [ANFAVEA – Release coletiva 08/01/2021](https://anfavea.com.br/docs/release_coletiva_08_01_2021.pdf); [Agência Brasil – Produção de veículos tem alta de 11,6% em 2021](https://agenciabrasil.ebc.com.br/economia/noticia/2022-01/producao-de-veiculos-tem-alta-de-116-em-2021-diz-anfavea)

---

*José Faria Neto — analista de dados em transição de carreira, com background em manufatura
industrial (Scania Latin America).*
