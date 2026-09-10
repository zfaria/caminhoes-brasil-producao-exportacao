# Caminhões do Brasil: Produção, Exportação e os Ciclos de um Mercado Interno

Análise de dados públicos da ANFAVEA (1957–2025) sobre produção, exportação e emplacamento
(vendas internas) de caminhões no Brasil — construída por alguém que passou os últimos 4+
anos montando os caminhões que estão dentro desses números.

> **Status:** projeto em construção. A seção de sazonalidade mensal está pendente de novas
> planilhas mensais da ANFAVEA (os arquivos originais usados aqui são séries **anuais**,
> 1957–2025). Este README será atualizado assim que essa parte for incorporada.

---

## Por que caminhão, por que eu

Caminhão não é um produto de prateleira — é o meio pelo qual quase tudo que se consome no
Brasil chega a algum lugar: mais de 60% da carga do país roda sobre pneus de caminhão. Quando
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
- Três séries anuais, categoria **Caminhões**, extraídas em 10/09/2026:
  - `PRODUCAO` — 1957–2025 (69 anos)
  - `EMPLACAMENTO` — 1957–2025 (69 anos) — proxy oficial da ANFAVEA para vendas no mercado interno
  - `EXPORTACAO` — 1965–2025 (61 anos; a ANFAVEA não reporta exportação de caminhões antes de 1965)
- Arquivos originais em [`data/raw/`](data/raw/), sem qualquer alteração de conteúdo.

Todos os números citados neste README vêm diretamente dessas três séries ou de fontes públicas
explicitamente linkadas na seção [Fontes das causas apontadas](#fontes-das-causas-apontadas-para-os-pontos-de-inflexão).
Nenhuma tendência, número ou causa foi presumida sem essa base.

## Metodologia

1. **Consolidação** ([`scripts/consolidar_dados.py`](scripts/consolidar_dados.py)): lê os três CSVs
   brutos (separador `;`, linha de título antes do cabeçalho, encoding UTF-8 com BOM), padroniza
   nomes de colunas e período, e gera dois datasets tidy em [`data/processed/`](data/processed/):
   - `anfavea_caminhoes_longo.csv` — formato longo (`Ano`, `Metrica`, `Valor`), pronto para o Tableau
   - `anfavea_caminhoes_consolidado.csv` — formato largo com métricas derivadas: participação da
     exportação/emplacamento na produção (%) e variação percentual ano a ano de cada série
2. **Checagem de integridade**: nenhum ano duplicado por métrica; conversão numérica com validação
   de tipo (`Ano` como inteiro, `Valor` como numérico).
3. **Exploração** ([`analysis/eda_caminhoes.py`](analysis/eda_caminhoes.py)): identifica picos e
   vales locais na série de produção (ano estritamente maior/menor que o anterior e o seguinte),
   maiores variações ano a ano, extremos de participação da exportação e correlações entre as três
   séries — em nível e em variação percentual anual.

Para reproduzir:

```bash
python -m pip install pandas numpy
python scripts/consolidar_dados.py
python analysis/eda_caminhoes.py
```

## A curva: quase 70 anos em cinco movimentos

A produção de caminhões no Brasil não cresce em linha reta — ela sobe e desaba em ciclos
abruptos, quase sempre de dois dígitos percentuais em um único ano. Os dados mostram picos e
vales locais em praticamente metade dos 69 anos da série. Cinco desses movimentos concentram os
maiores saltos e quedas:

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

## Insight central: quem puxa o ciclo não é quem exporta

A pergunta óbvia para uma indústria que exporta caminhões é: os ciclos de alta e baixa vêm da
demanda externa? **Os dados dizem que não.**

Em nível (quanto se produz, exporta e vende internamente a cada ano, 1965-2025), produção e
emplacamento (mercado interno) têm correlação de **0,972** — andam praticamente juntos, o que já
era esperado, já que a maior parte do que se produz é vendido no Brasil. Produção e exportação
correlacionam bem menos: **0,751**.

A diferença fica ainda mais clara quando se olha para a **variação percentual ano a ano** — ou
seja, não "o quanto se produz", mas "o quanto o mercado oscila de um ano para o outro":

| Correlação da variação anual (%) | Coeficiente |
|---|---|
| Produção × Emplacamento | **0,923** |
| Produção × Exportação | **0,003** |

A correlação entre a variação da produção e a variação da exportação é essencialmente **zero**. Os
ciclos de boom e crise que caracterizam a indústria de caminhões no Brasil — as quedas de 30-50%
em um único ano — são movidos quase inteiramente pelo mercado interno. A exportação se comporta
como um fluxo largamente independente desses ciclos.

Isso não significa que a exportação seja irrelevante nos anos de crise — pelo contrário: a
participação da exportação na produção total **atinge seus maiores valores exatamente nos anos
de colapso do mercado interno** (35,6% em 2016 e 34,0% em 2017, os dois maiores picos da série,
bem acima da média histórica de ~16%). Em números absolutos a exportação não cresce nesses anos —
ela simplesmente cai menos do que a produção total, funcionando como um amortecedor parcial para
os fabricantes justamente quando o mercado interno mais precisa de alívio, sem no entanto ser a
força que dita o tamanho do ciclo.

## O que isso significa pra quem já viveu por dentro

Cada linha desse dataset que despenca 30, 40, quase 50% em um único ano tem um equivalente
concreto no chão de fábrica: turnos cancelados, linha rodando mais devagar, fornecedores
reprogramando entregas. E cada recuperação de +40%, +57%, +74% também tem o seu — hora extra,
contratação às pressas, pressão para entregar o que ficou represado. Trabalhar dentro desse
setor por mais de quatro anos não me deu acesso a nenhum dado que não esteja aqui; me deu a
referência para reconhecer, nos números, o motivo de cada virada de ciclo que meus colegas de
linha sentiam antes de qualquer manchete confirmar.

O padrão mais útil que os dados revelam — dependência do mercado interno, não do externo, como
motor do ciclo, e antecipação regulatória como gatilho recorrente e previsível de queda — é
exatamente o tipo de leitura que interessa a quem planeja produção, estoque e contratação num
ambiente industrial: a próxima mudança de norma de emissões (ou de crédito, ou de juros) vale
mais como sinal de alerta do que qualquer expectativa isolada de mercado externo.

## Estrutura do repositório

```
├── data/
│   ├── raw/                 CSVs originais da ANFAVEA (não editados)
│   └── processed/           Dataset consolidado (longo e largo) pronto para Tableau
├── scripts/
│   └── consolidar_dados.py  Limpeza e consolidação das 3 séries
├── analysis/
│   └── eda_caminhoes.py     Picos, vales, variações e correlações
├── tableau/
│   └── story_guide.md       Roteiro de construção da Story no Tableau Desktop
└── README.md
```

## Dashboard (Tableau Story)

O dashboard final é construído como uma **Story** no Tableau Public, seguindo a mesma narrativa
deste README (abertura → evolução → insight central → fechamento). Roteiro completo de construção
em [`tableau/story_guide.md`](tableau/story_guide.md). Link para a versão publicada: *(a incluir
após publicação no Tableau Public)*.

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
