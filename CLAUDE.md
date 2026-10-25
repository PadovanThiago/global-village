# Villa · contexto para o Claude Code

Villa é um agregador internacional de análises do mundo contemporâneo pela lente da democracia liberal. O editor é Thiago Padovan. O lançamento para uma base controlada está marcado para 20/11/2026.

## Como o site é feito
- Um único arquivo, `index.html`, com HTML, CSS e JavaScript puros. Não há build nem dependências. Publicado pelo GitHub Pages a partir da branch `main`.
- Os dados ficam em constantes no início do script: `PEOPLE` (analistas), `ITEMS` (análises), `ORGS` (organizações e publicações), `AV` (filmes e séries), `AREAS` e `AVTH` (traduções de rótulos) e `L` (textos da interface em en, pt, es, fr, it).
- As rotas usam hash: `#inicio`, `#analises`, `#analistas`, `#a-<id>`, `#tema-<dem|geo|eco|tec>`, `#p-<id>`, `#assistir`, `#organizacoes`, `#newsletter`, `#sobre`.
- O inglês é o idioma principal. Todo texto novo de interface entra nos cinco idiomas.
- `localStorage` só guarda conveniências do leitor (idioma, seguidos, salvos), sempre com try/catch.
- Logos em `villa-black.png` e `villa-white.png`.

## Regras do projeto
- A curadoria é de Thiago. Nenhum nome, organização ou filme entra ou sai sem a aprovação dele. A fonte de verdade é a planilha de trabalho e o portal de curadoria.
- A home não menciona o Brasil. O projeto é internacional.
- Textos publicáveis em português evitam travessões, dois-pontos como recurso de estilo, frases fragmentadas, tríades anafóricas, paralelismos negativos e transições polidas. Todo texto passa por uma revisão de naturalidade antes de ir ao ar.
- Thiago revisa e aprova. Mudanças visíveis vão por pull request com um resumo curto em português.

## Pendências conhecidas
- Os formulários de newsletter já enviam ao Buttondown (POST para `https://buttondown.com/api/emails/embed-subscribe/<usuário>` com `email` e `tag` igual a `pt` ou `en`). Falta preencher a constante `BUTTONDOWN_USER` no `index.html`. Enquanto ela estiver vazia, o formulário só simula a inscrição.
- A newsletter sai em português e inglês. A página `#newsletter` oferece só esses dois idiomas, e os formulários da home usam `pt` quando a interface está em português e `en` nos demais casos.
- Separar os dados em arquivos JSON quando o volume crescer.
