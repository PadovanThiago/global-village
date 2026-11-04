"""Gera a base do agente "Pergunte ao Global Village" e mantém o arquivo dos feeds.

Uso: python3 -I tools/base-agente.py <arquivo de saída base.json> [dias]

Faz duas coisas:
1. Lê agora os feeds das fontes aprovadas e junta o que encontrar ao arquivo local
   dados/arquivo-feeds.json, guardando só título, autor, data, um trecho curto da descrição
   e o link. O arquivo fica fora do Git (veja .gitignore), porque o conteúdo é de terceiros.
   Publicações mais velhas que [dias] (padrão 60) saem do arquivo.
2. Escreve a base do agente: as análises publicadas no site, com resumos e notas do editor,
   os analistas, as organizações, os títulos da seção Assistir e o arquivo dos feeds.
A base vai para o artifact "Pergunte ao Global Village" no claude.ai, como diz o roteiro da edição diária.
"""
import concurrent.futures as cf
import datetime
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("ler_feeds", ROOT / "tools/ler-feeds.py")
ler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ler)

ARQUIVO = ROOT / "dados/arquivo-feeds.json"
SITE = "https://padovanthiago.github.io/global-village/"
REG = {"latam": "América Latina", "na": "América do Norte", "eu": "Europa", "afr": "África", "mena": "Oriente Médio",
       "asia": "Ásia e Pacífico", "int": "Global"}
TEMA = {"dem": "Democracia e instituições", "geo": "Geopolítica", "eco": "Economia", "tec": "Tecnologia e liberdades"}


def conserta(texto):
    """Desfaz o texto em latin-1 lido como UTF-8, que aparece em alguns feeds (Folha)."""
    try:
        texto = texto.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    # O que já chegou corrompido do feed não tem conserto: tira o caractere de substituição.
    return texto.replace("�", "")


def bloco(linhas, inicio):
    i = linhas.index(inicio) + 1
    out = []
    while not linhas[i].strip().startswith("].map"):
        t = linhas[i].strip().rstrip(",")
        if t.startswith("["):
            out.append(t)
        i += 1
    return out


def atualizar_arquivo(dias):
    arquivo = json.loads(ARQUIVO.read_text(encoding="utf-8")) if ARQUIVO.exists() else []
    vistos = {x["url"] for x in arquivo}
    lista = ler.fontes()
    with cf.ThreadPoolExecutor(16) as ex:
        resultados = list(ex.map(lambda f: (f, ler.itens(ler.baixar(f["feed"]))), lista))
    novos = 0
    for f, its in resultados:
        for it in its:
            if not it["url"] or not it["data"] or it["url"] in vistos:
                continue
            vistos.add(it["url"])
            desc = re.sub(r"\s+", " ", conserta(it["descricao"])).strip()
            arquivo.append({
                "titulo": conserta(it["titulo"]).strip(), "fonte": f["nome"], "tipo": f["tipo"], "id": f["id"],
                "autor": conserta(it["autor"]).strip(), "data": it["data"], "trecho": desc[:280], "url": it["url"],
            })
            novos += 1
    limite = (datetime.date.today() - datetime.timedelta(days=dias)).isoformat()
    arquivo = sorted((x for x in arquivo if x["data"] >= limite), key=lambda x: x["data"], reverse=True)
    ARQUIVO.parent.mkdir(exist_ok=True)
    ARQUIVO.write_text(json.dumps(arquivo, ensure_ascii=False), encoding="utf-8")
    print(f"{len(lista)} feeds, {novos} publicações novas, {len(arquivo)} no arquivo", file=sys.stderr)
    return arquivo


def main():
    saida = pathlib.Path(sys.argv[1])
    dias = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    arquivo = atualizar_arquivo(dias)

    src = (ROOT / "index.html").read_text(encoding="utf-8")
    linhas = src.split("\n")
    cc = json.loads(re.search(r"const CC_REG = (\{.*?\});", src).group(1))

    analistas = []
    for t in bloco(linhas, "const PEOPLE = ["):
        a = json.loads(re.sub(r"([{,])(\w+):", r'\1"\2":', t))
        analistas.append({"id": a[0], "nome": a[1], "area": a[3], "pais": a[4], "regiao": REG[cc.get(a[4], "int")],
                          "vinculo": a[5], "temas": [TEMA.get(x, x) for x in a[7]], "pagina": SITE + "#a-" + a[0]})
    nomes = {p["id"]: p["nome"] for p in analistas}

    organizacoes = []
    for t in bloco(linhas, "const ORGS = ["):
        a = json.loads(t)
        organizacoes.append({"nome": a[0], "pais": a[2], "regiao": REG[cc.get(a[2], "int")], "descricao": a[5],
                             "temas": [TEMA.get(x, x) for x in a[6]], "url": a[3]})

    i = src.index("const ITEMS = [")
    j = src.index("\n];", i)
    analises = []
    for m in re.finditer(r"^ \{(.*)\},?$", src[i:j], re.M):
        x = json.loads(re.sub(r'([{,])(\w+):', r'\1"\2":', "{" + m.group(1) + "}"))
        autor = ", ".join(nomes.get(w, w) for w in x.get("who", [])) or x.get("by", "") or x["src"]
        it = {"titulo": x["title"], "autor": autor, "fonte": x["src"], "data": x["date"], "tema": TEMA.get(x["theme"], x["theme"]),
              "formato": x.get("fmt", ""), "idioma": x.get("lang", ""), "resumo": x.get("sum", ""), "resumo_en": x.get("sum_en", ""),
              "url": x["url"]}
        if x.get("nota"):
            it["nota_do_editor"] = x["nota"]
            it["nota_url"] = x.get("nota_url", "")
        analises.append(it)
    curadas = {a["url"] for a in analises}

    k = src.index("const AV = [")
    l = src.index("\n].map", k)
    assistir = []
    for t in src[k:l].split("\n")[1:]:
        t = t.rstrip(",")
        if t.startswith("["):
            a = json.loads(t)
            assistir.append({"titulo": a[1], "original": a[2], "tipo": a[3], "ano": a[4], "categoria": a[11],
                             "onde": a[6] or a[7] or a[8] or "sem streaming no Brasil", "url": a[9]})

    fontes = []
    for x in arquivo:
        if x["url"] in curadas:
            continue
        x = {k: conserta(v) if isinstance(v, str) else v for k, v in x.items()}
        nome = x["fonte"]
        autor = x["autor"] or nome
        # Num canal de pessoa da base, outro autor assinando é autor fora da base.
        fora = x["tipo"] == "pessoa" and bool(x["autor"]) and x["autor"].strip().lower() != nome.lower()
        fontes.append({"titulo": x["titulo"], "autor": autor, "fonte": nome, "data": x["data"], "trecho": x["trecho"],
                       "url": x["url"], "autor_fora_da_base": fora})

    base = {"gerado_em": datetime.date.today().isoformat(), "analises": analises, "fontes": fontes,
            "analistas": analistas, "organizacoes": organizacoes, "assistir": assistir}
    saida.write_text(json.dumps(base, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"base: {len(analises)} análises, {len(fontes)} publicações das fontes, {saida.stat().st_size // 1024} KB", file=sys.stderr)


if __name__ == "__main__":
    main()
