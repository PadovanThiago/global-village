"""Gera os dados do painel de fontes: o estado de cada fonte da base e os autores fora dela.

Uso: python3 -I tools/painel-fontes.py <pasta de saída>

Escreve dois arquivos JSON na pasta:
- fontes.json: uma linha por analista ou organização da base, com o feed, a situação (ativa, parada há
  mais de 30 dias, sem feed ou feed sem resposta), a última publicação no feed, quantas saíram nos
  últimos 7 dias e quantas análises estão no site.
- fora-da-base.json: autores que aparecem no site assinando análises de organizações aprovadas
  sem estar entre os analistas da base.
Os arquivos vão para o artifact "Fontes do Global Village" no claude.ai, como diz o roteiro da edição diária.
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

CAT = {"think": "Pensadores e acadêmicos", "econ": "Economistas", "journo": "Jornalistas e analistas", "pol": "Políticos e ativistas",
       "media": "Jornalismo independente", "index": "Índices de democracia", "tank": "Think tanks", "fund": "Fundações",
       "net": "Direitos e sociedade civil", "pub": "Publicações"}
REG = {"latam": "América Latina", "na": "América do Norte", "eu": "Europa", "afr": "África", "mena": "Oriente Médio",
       "asia": "Ásia e Pacífico", "int": "Global"}
TEMA = {"dem": "Democracia", "geo": "Geopolítica", "eco": "Economia", "tec": "Tecnologia"}


def bloco(linhas, inicio):
    i = linhas.index(inicio) + 1
    out = []
    while not linhas[i].strip().startswith("].map"):
        t = linhas[i].strip().rstrip(",")
        if t.startswith("["):
            out.append(t)
        i += 1
    return out


def main():
    destino = pathlib.Path(sys.argv[1])
    destino.mkdir(parents=True, exist_ok=True)
    s = (ROOT / "index.html").read_text(encoding="utf-8")
    linhas = s.split("\n")
    cc_reg = json.loads(re.search(r"const CC_REG = (\{.*?\});", s).group(1))

    pessoas = []
    for t in bloco(linhas, "const PEOPLE = ["):
        a = json.loads(re.sub(r"([{,])(\w+):", r'\1"\2":', t))
        pessoas.append({"id": a[0], "nome": a[1], "cat": a[2], "cc": a[4], "temas": a[7], "feed": a[8].get("rss", ""), "tipo": "Analista"})
    orgs = []
    for t in bloco(linhas, "const ORGS = ["):
        a = json.loads(t)
        orgs.append({"id": (a[7] if len(a) > 7 else "") or "", "nome": a[0], "cat": a[1], "cc": a[2], "temas": a[6], "feed": a[9] if len(a) > 9 else "", "tipo": "Organização"})

    i = s.index("const ITEMS = [")
    itens = re.findall(r'\{id:"[^"]+",who:\[([^\]]*)\](?:,pub:"([^"]*)")?(?:,by:"([^"]*)")?,theme:"[a-z]+",fmt:"[a-z]+",src:"([^"]*)",date:"([^"]*)"', s[i:])
    nomes_pessoas = {p["nome"] for p in pessoas}

    hoje = datetime.date.today()
    semana = (hoje - datetime.timedelta(days=7)).isoformat()

    def ler_feed(f):
        if not f["feed"]:
            return f, None
        return f, ler.itens(ler.baixar(f["feed"]))

    linhas_out = []
    with cf.ThreadPoolExecutor(16) as ex:
        for f, its in ex.map(ler_feed, pessoas + orgs):
            if f["tipo"] == "Analista":
                no_site = [d for who, pub, by, src, d in itens if f'"{f["id"]}"' in who]
            else:
                no_site = [d for who, pub, by, src, d in itens if src == f["nome"] or (f["id"] and pub == f["id"])]
            datas = sorted((x["data"] for x in its or [] if x["data"]), reverse=True)
            if its is None:
                estado = "Sem feed"
            elif not its:
                estado = "Feed sem resposta"
            else:
                estado = "Feed lido"
            dias = (hoje - datetime.date.fromisoformat(datas[0])).days if datas else None
            if estado != "Feed lido":
                situacao = estado
            elif dias is not None and dias > 30:
                situacao = "Parada há mais de 30 dias"
            else:
                situacao = "Ativa"
            linhas_out.append({
                "fonte": f["nome"], "tipo": f["tipo"], "categoria": CAT.get(f["cat"], f["cat"]),
                "pais": f["cc"], "regiao": REG.get(cc_reg.get(f["cc"], "int"), "Global"),
                "temas": ", ".join(TEMA.get(x, x) for x in f["temas"]),
                "situacao": situacao, "feed": f["feed"],
                "ultima_publicacao": datas[0] if datas else "",
                "dias_sem_publicar": dias,
                "publicacoes_7_dias": sum(1 for d in datas if d >= semana),
                "analises_no_site": len(no_site),
                "ultima_no_site": max(no_site) if no_site else "",
            })
    linhas_out.sort(key=lambda r: (r["tipo"], r["fonte"].lower()))

    fora = {}
    for who, pub, by, src, d in itens:
        if by and not who.strip() and by not in nomes_pessoas and "tradução" not in by and by != "Inteligência Democrática":
            r = fora.setdefault(by, {"autor": by, "publicado_em": set(), "analises_no_site": 0, "ultima_no_site": ""})
            r["publicado_em"].add(src)
            r["analises_no_site"] += 1
            r["ultima_no_site"] = max(r["ultima_no_site"], d)
    fora_out = sorted(({**r, "publicado_em": ", ".join(sorted(r["publicado_em"]))} for r in fora.values()),
                      key=lambda r: (-r["analises_no_site"], r["autor"]))

    (destino / "fontes.json").write_text(json.dumps(linhas_out, ensure_ascii=False, indent=1), encoding="utf-8")
    (destino / "fora-da-base.json").write_text(json.dumps(fora_out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(linhas_out)} fontes, {len(fora_out)} autores fora da base", file=sys.stderr)


if __name__ == "__main__":
    main()
