# Global Village · contexto para o Claude Code

Global Village é um agregador internacional de análises do mundo contemporâneo pela lente da democracia liberal. O editor é Thiago Padovan. O lançamento para uma base controlada está marcado para 20/11/2026.

## Como o site é feito
- Um único arquivo, `index.html`, com HTML, CSS e JavaScript puros. Não há build nem dependências. Publicado pelo GitHub Pages a partir da branch `main`.
- Os dados ficam em constantes no início do script: `PEOPLE` (analistas), `ITEMS` (análises), `ORGS` (organizações e publicações), `AV` (filmes e séries), `AREAS` e `AVTH` (traduções de rótulos) e `L` (textos da interface em en, pt, es, fr, it).
- As rotas usam hash: `#inicio`, `#analises`, `#analistas`, `#a-<id>`, `#tema-<dem|geo|eco|tec>`, `#p-<id>`, `#assistir`, `#organizacoes`, `#newsletter`, `#sobre`.
- O inglês é o idioma principal. Todo texto novo de interface entra nos cinco idiomas.
- Um item de `ITEMS` sem `who` pode ter `pub` (só `revista-id` e `dagobah` têm página) ou apenas `src` e, se houver, `by`. Nesse último caso o cartão aponta direto para o original e não mostra o botão de seguir.
- Para testar uma mudança, confira o conteúdo renderizado dentro de `<main>` (Chrome headless com `--dump-dom`), nunca o HTML bruto, porque os dados ficam no próprio script e aparecem mesmo com a página quebrada.
- Os feeds de cada fonte ficam no campo `rss` dos canais em `PEOPLE` e no décimo campo de `ORGS`, copiados da coluna Feed RSS da planilha. Quem não tem feed aparece na planilha como "sem feed" com o motivo. Para buscar novidades, rode `python3 -I tools/ler-feeds.py <data>`.
- `localStorage` só guarda conveniências do leitor (idioma, seguidos, salvos), sempre com try/catch.
- Logotipo em `gv-logo-dark.png` (fundos claros) e `gv-logo-light.png` (fundos escuros). O guia da marca, com cores e fontes, está em `brand/global-village/README.md`.
- Ícones em `favicon.png` e `apple-touch-icon.png`. A prévia de link usa `og-image.png`, cuja fonte fica em `brand/site/src/`. As tags `og:` usam o endereço absoluto do GitHub Pages e precisam ser trocadas se o domínio mudar.

## Nome
- O projeto se chamou Villa até 26/10/2026 e passou a se chamar Global Village. As chaves `villa:` do localStorage ficaram com o nome antigo de propósito, para não apagar as preferências dos leitores.

## Newsletter
- A newsletter sai pelo Substack do Projeto Villa (https://projetovilla.substack.com), que já tem cerca de 250 inscritos e os ensaios de Thiago. O Global Village tem duas seções lá, `global-village` em português e `global-village-english` em inglês, para que quem só quer os ensaios possa sair da edição diária sem cancelar tudo. O site não coleta e-mails. Os botões de assinatura levam à seção do idioma (constantes `SUBSTACK` e `NL_SECTION` do `index.html`).
- A newsletter é diária, de segunda a sexta, com de 3 a 5 fatos do dia anterior, os temas do site cobertos sempre que houver material e pelo menos um fato fora do eixo Estados Unidos e Europa. O roteiro completo está em `.claude/skills/edicao-diaria/SKILL.md`.
- A edição tem uma decisão humana no meio. Uma tarefa agendada no app do Claude ("Global Village · edição diária") roda às 6h dos dias úteis a primeira etapa do roteiro e entrega a pauta do dia num documento do Claude Docs, com os candidatos de cada tema. Thiago marca os fatos que entram. Só então a segunda etapa abre o PR com o feed do site, gera a imagem do dia com `tools/imagem-edicao.py` (molde em `brand/newsletter/src/edicao.html`) e escreve a edição em outro documento. Thiago revisa, aprova o PR e publica cada edição como post na seção do idioma no Substack.

## Regras do projeto
- A curadoria é de Thiago. Nenhum nome, organização ou filme entra ou sai sem a aprovação dele. A fonte de verdade é a planilha de trabalho e o portal de curadoria.
- A home não menciona o Brasil. O projeto é internacional.
- Na voz do Global Village (notas do editor, introduções, títulos de seção), a vitória de Lula não é tratada como vitória da democracia liberal. Lula e o PT são um populismo de esquerda e o bolsonarismo um populismo de direita, os dois do campo da democracia eleitoral, como argumenta a [Carta a Francis Fukuyama](https://www.revistaid.com.br/p/carta-a-francis-fukuyama) da Revista ID.
- Os resumos de análises curadas descrevem o que o autor diz e atribuem a avaliação a ele ("Para Fukuyama, …"), sem corrigir o autor. Quando discordamos do enquadramento, a correção vai na nota do editor do item (campos `nota`, `nota_en` e, se houver, `nota_url` em `ITEMS`) e, na newsletter, na parte "Onde divergem". Uma voz que trate o PT como democrático de forma sistemática é caso para o Conselho de Curadoria, nunca para exclusão pela edição.
- O contexto regional mora na aba Contexto regional do portal de curadoria, com cópia em `conhecimento/leituras-regionais.md` e o histórico de casos em `conhecimento/casos.md`. A meta é ter um curador por região ou sub-região do mundo, que propõe os registros da sua região. Um registro só vale depois de aprovado pelo editor e validado por curador de outra tradição política. O registro é interno, e o efeito público dele são as notas do editor e os contrapontos da newsletter. A edição diária consulta esses registros (veja o roteiro).
- Textos publicáveis em português evitam travessões, dois-pontos como recurso de estilo, frases fragmentadas, tríades anafóricas, paralelismos negativos e transições polidas. Todo texto passa por uma revisão de naturalidade antes de ir ao ar.
- Thiago revisa e aprova. Mudanças visíveis vão por pull request com um resumo curto em português.

## Pendências conhecidas
- O `index.html` tem `<meta name="robots" content="noindex, nofollow">` durante a fase de teste. Retirar no lançamento para o site aparecer nas buscas.
- Separar os dados em arquivos JSON quando o volume crescer.
- Portal de curadoria (artifact "Global Village Curadoria" no claude.ai, https://claude.ai/artifact/MA4yjRaLbECoNTeEHv46Xg): a Mesa do editor só aparece para o dono, e os curadores entram como Contribuidor. Nos dados a separação ainda é só visual, porque votos, decisões e notas do editor ficam no mesmo registro de cada item, que qualquer Contribuidor lê e altera. Antes de ampliar o conselho além dos primeiros cinco curadores de confiança, mover os votos para um espaço por curador e as decisões do editor para um caminho só do editor, migrando os dados existentes. A aba Contexto regional já nasceu nesse modelo, com a validação de cada curador em `validacoes/<id do curador>` e a aprovação do editor em `editor/contexto`, que só o dono grava.
- O Buttondown foi usado nos testes de outubro de 2026 e deixou de ser o meio de envio. Os materiais em `brand/buttondown/` ficaram como histórico.
