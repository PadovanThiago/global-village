# Global Village · identidade visual

O Global Village é um projeto do Villa e segue o sistema visual do Villa, cujos tokens, fontes, marcas e naipes estão em `brand/villa/`. O que é próprio do Global Village é o símbolo e o nome.

A ideia vem de McLuhan, o mundo como uma aldeia onde muitas vozes se encontram. O símbolo é um globo desenhado com três linhas (o contorno, um meridiano e o equador), e o disco no cruzamento é a praça onde essas vozes se encontram. Desde novembro de 2026 o disco é ocre-airbel, o mesmo preenchimento dos discos de naipe do Villa, e é a única referência perceptível ao sistema do Villa em cada peça.

## Arquivos

| Arquivo | Uso |
| --- | --- |
| `gv-logo-dark.png` | Logotipo horizontal em tinta, sobre papel e papel-2 |
| `gv-logo-light.png` | Logotipo horizontal em papel, sobre tinta e verde-veneziana |
| `gv-symbol-dark.svg`, `gv-symbol-light.svg` | Símbolo sozinho, em vetor |
| `gv-icon-512.png`, `gv-icon-1024.png` | Ícone quadrado, símbolo em papel sobre verde-veneziana, como o favicon do Villa |
| `src/` | Fontes HTML das imagens, renderizadas com o Chrome headless |

O nome se escreve sempre Global Village, com iniciais maiúsculas, e em português leva artigo masculino (o Global Village). O símbolo nunca aparece sem o nome em tamanhos acima do ícone.

## Cores

São os tokens do Villa (`brand/villa/tokens.css`).

| Token | Hex | Uso no Global Village |
| --- | --- | --- |
| papel | `#F3EBDD` | Fundo de página e de cartões |
| papel-2 | `#E8DCC6` | Faixas, notas do editor, caixas laterais |
| tinta | `#1E1A16` | Texto, títulos, fios fortes, botão escuro |
| tinta-suave | `#5E5547` | Metadados e texto secundário |
| linha | `#CDBFA6` | Fios finos e o globo em marca-d'água. Nunca texto |
| verde-veneziana | `#415E3A` | Links, idioma ativo, avatares, foco de teclado e o ícone |
| ocre-airbel | `#C19440` | Só preenchimento, com tinta por cima. O disco do símbolo, a faixa da newsletter e os fios dos fatos da edição |
| ocre-texto | `#7A5718` | Números de destaque (radar, estatísticas, fatos da edição) |
| violeta-carimbo | `#55478A` | A data da imagem da edição, em Courier Prime. Uma vez por peça |

O Villa não usa cor para erro nem para alerta.

## Tipografia

As fontes ficam em `fonts/` na raiz do repositório e o site as carrega dali, sem depender do Google Fonts.

| Fonte | Uso |
| --- | --- |
| Newsreader | Títulos (peso 500), resumos e textos de leitura |
| Archivo | Interface, rótulos em caixa-alta, botões, navegação e números de destaque |
| Courier Prime | Datas do feed e da edição. Nunca frases longas |

## Regras do Villa aplicadas aqui

- Cantos retos em tudo, inclusive avatares e botões. Sem sombras e sem degradês.
- Foco de teclado em anel contínuo de 2px, com 2px de afastamento, em verde-veneziana.
- O Global Village não usa os naipes do Villa. Os quatro temas do site (democracia, geopolítica, economia e tecnologia) não correspondem às famílias editoriais dos naipes.
