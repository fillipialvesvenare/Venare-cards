# venare-cards

Modelo visual dos cards semanais de ideias de posts da Venare (@venareinvestimentos).

## Como gerar os cards
```
python3 build.py caminho/cards.json pasta_de_saida
```
Gera `venare_ideia_1.png` ... `venare_ideia_5.png` (1200 px de largura) com Playwright + Chromium.
Requer: `pip install playwright` e Chromium instalado.

## Formato do cards.json
Lista com 5 objetos: `n`, `eixo`, `titulo`, `formato`, `duracao`, `dado`, `fonte`, `gancho`,
`roteiro_titulo`, `roteiro` (lista), `roteiro_lista` (true para carrossel com slides numerados),
`legenda`, `cta`, `atencao`. Veja `exemplo/cards_exemplo.json`.

## Regras da marca (não alterar)
- Cores: #070F40, #2A3BA0, #4C67FF, #8698FF, #F0F0F0, #1A1A1A, branco.
- Fonte Prompt (ExtraBold em caixa alta nos títulos). Arquivos em `assets/`.
- Logos, glow, símbolo, dots e pattern são os originais, sem distorção, recolor ou redimensionamento desproporcional.
- Não editar nada em `assets/`.

## Rotina semanal
Pesquisar a semana anterior (3 eixos: mercado de Florianópolis; investir com consultor; números de Santa Catarina),
montar cards.json com 5 ideias (mín. 1 por eixo), gerar os PNGs, subir ao Drive em
`CONTEÚDO SEMANAL VENARE/AAAA-MM - Mês/Semana DD.MM a DD.MM` e enviar o e-mail com o link da pasta.
