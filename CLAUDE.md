# Global Village · contexto para o Claude Code

Global Village é um agregador internacional de análises do mundo contemporâneo pela lente da democracia liberal. O editor é Thiago Padovan. O lançamento para uma base controlada está marcado para 20/11/2026.

## Como o site é feito
- Um único arquivo, `index.html`, com HTML, CSS e JavaScript puros. Não há build nem dependências. Publicado pelo GitHub Pages a partir da branch `main`.
- Os dados ficam em constantes no início do script: `PEOPLE` (analistas), `ITEMS` (análises), `ORGS` (organizações e publicações), `AV` (filmes e séries), `AREAS` e `AVTH` (traduções de rótulos) e `L` (textos da interface em en, pt, es, fr, it).
- As rotas usam hash: `#inicio`, `#analises`, `#analistas`, `#a-<id>`, `#tema-<dem|geo|eco|tec>`, `#p-<id>`, `#assistir`, `#organizacoes`, `#newsletter`, `#sobre`.
- O inglês é o idioma principal. Todo texto novo de interface entra nos cinco idiomas.
- Um item de `ITEMS` sem `who` pode ter `pub` (só `revista-id` e `dagobah` têm página) ou apenas `src` e, se houver, `by`. Nesse último caso o cartão aponta direto para o original e não mostra o botão de seguir.
- Para testar uma mudança, confira o conteúdo renderizado dentro de `<main>` (Chrome headless com `--dump-dom`), nunca o HTML bruto, porque os dados ficam no próprio script e aparecem mesmo com a página quebrada.
- `localStorage` só guarda conveniências do leitor (idioma, seguidos, salvos), sempre com try/catch.
- Logotipo em `gv-logo-dark.png` (fundos claros) e `gv-logo-light.png` (fundos escuros). O guia da marca, com cores e fontes, está em `brand/global-village/README.md`.
- Ícones em `favicon.png` e `apple-touch-icon.png`. A prévia de link usa `og-image.png`, cuja fonte fica em `brand/site/src/`. As tags `og:` usam o endereço absoluto do GitHub Pages e precisam ser trocadas se o domínio mudar.

## Nome
- O projeto se chamou Villa até 26/10/2026 e passou a se chamar Global Village. As chaves `villa:` do localStorage ficaram com o nome antigo de propósito, para não apagar as preferências dos leitores.

## Regras do projeto
- A curadoria é de Thiago. Nenhum nome, organização ou filme entra ou sai sem a aprovação dele. A fonte de verdade é a planilha de trabalho e o portal de curadoria.
- A home não menciona o Brasil. O projeto é internacional.
- Textos publicáveis em português evitam travessões, dois-pontos como recurso de estilo, frases fragmentadas, tríades anafóricas, paralelismos negativos e transições polidas. Todo texto passa por uma revisão de naturalidade antes de ir ao ar.
- Thiago revisa e aprova. Mudanças visíveis vão por pull request com um resumo curto em português.

## Pendências conhecidas
- Os formulários de newsletter já enviam ao Buttondown (POST para `https://buttondown.com/api/emails/embed-subscribe/<usuário>` com `email` e `tag` igual a `pt` ou `en`). O usuário fica na constante `BUTTONDOWN_USER` do `index.html` (hoje `padovan`). Se ela ficar vazia, o formulário só simula a inscrição.
- A newsletter sai em português e inglês. A página `#newsletter` oferece só esses dois idiomas, e os formulários da home usam `pt` quando a interface está em português e `en` nos demais casos.
- O `index.html` tem `<meta name="robots" content="noindex, nofollow">` durante a fase de teste. Retirar no lançamento para o site aparecer nas buscas.
- Separar os dados em arquivos JSON quando o volume crescer.
- Portal de curadoria (artifact "Global Village Curadoria" no claude.ai, https://claude.ai/artifact/MA4yjRaLbECoNTeEHv46Xg): a Mesa do editor só aparece para o dono, e os curadores entram como Contribuidor. Nos dados a separação ainda é só visual, porque votos, decisões e notas do editor ficam no mesmo registro de cada item, que qualquer Contribuidor lê e altera. Antes de ampliar o conselho além dos primeiros cinco curadores de confiança, mover os votos para um espaço por curador e as decisões do editor para um caminho só do editor, migrando os dados existentes.
- Enviar os temas escolhidos na página `#newsletter` como etiquetas do Buttondown (`dem`, `geo`, `eco`, `tec`). O código está pronto na branch `feat/newsletter-temas` (PR #2, fechado). Depende do plano pago do Buttondown, que é o que permite criar etiquetas. Retomar quando houver assinatura.
