# Global Village · identidade visual

O Global Village é um projeto do Villa e usa só o que existe no sistema visual do Villa, guardado em `brand/villa/` (tokens, marcas e naipes) e em `fonts/`. Desde 23/11/2026 não há marca própria. O globo e o terracota da identidade anterior saíram de uso.

## Marca

- O logotipo é o monograma do Villa (`brand/villa/logos/villa-monograma.svg`, copiado sem alteração) seguido do nome Global Village em Newsreader 500, do mesmo jeito que o nome Villa aparece na capa do sistema.
- O ícone é o favicon do Villa, o monograma em papel sobre verde-veneziana.
- O nome se escreve sempre Global Village, com iniciais maiúsculas, e em português leva artigo masculino (o Global Village).

| Arquivo | Uso |
| --- | --- |
| `gv-logo-dark.png` | Logotipo em tinta, sobre papel, papel-2 e ocre-airbel |
| `gv-logo-light.png` | Logotipo em papel, sobre tinta e verde-veneziana |
| `gv-icon-512.png`, `gv-icon-1024.png` | Ícone quadrado (favicon, Substack, redes) |
| `src/` | Fontes das imagens, renderizadas com o Chrome headless |

## Peças

| Peça | Molde | Componente do Villa que segue |
| --- | --- | --- |
| Prévia de link do site | `brand/site/src/og-image.html` | Cover, com a fachada em blocos |
| Imagem da edição diária | `brand/newsletter/src/edicao.html` | CabecalhoArtigo, com a data em Carimbo (`23.XI.2026`) |
| Arte das seções no Substack | `brand/substack/src/secao.html` | Verso do baralho, verde-veneziana com o monograma |

Cada peça tem uma só referência perceptível ao sistema (a fachada, o carimbo ou o verde com o monograma).

## Cores

São os tokens do Villa (`brand/villa/tokens.css`).

| Token | Hex | Uso no Global Village |
| --- | --- | --- |
| papel | `#F3EBDD` | Fundo de página e de cartões |
| papel-2 | `#E8DCC6` | Faixas, notas do editor, caixas laterais |
| tinta | `#1E1A16` | Texto, títulos, fios fortes |
| tinta-suave | `#5E5547` | Metadados, rótulos e texto secundário |
| linha | `#CDBFA6` | Fios finos. Nunca texto |
| verde-veneziana | `#415E3A` | Botão principal, idioma ativo, avatares, foco de teclado e ícone |
| ocre-airbel | `#C19440` | Só preenchimento, com tinta por cima. A faixa da newsletter e a fachada da prévia |
| ocre-texto | `#7A5718` | Números de destaque (radar, estatísticas, fatos da edição) |
| violeta-carimbo | `#55478A` | O carimbo da imagem da edição. Uma vez por peça |

O Villa não usa cor para erro nem para alerta.

## Tipografia

| Fonte | Uso |
| --- | --- |
| Newsreader | Títulos (peso 500), resumos e textos de leitura |
| Archivo | Interface, rótulos em caixa-alta, botões, navegação e números de destaque |
| Courier Prime | Datas do feed e carimbos. Nunca frases longas |

## Regras do Villa aplicadas aqui

- Cantos retos em tudo, inclusive avatares e botões. Sem sombras e sem degradês.
- Foco de teclado em anel contínuo de 2px, com 2px de afastamento, em verde-veneziana.
- Nenhum ícone novo. Os naipes do Villa marcam artigos do Villa e não são usados nos temas do Global Village.
