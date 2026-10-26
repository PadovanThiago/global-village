"""Lê os feeds das fontes aprovadas e lista o que foi publicado desde uma data.

Uso: python3 -I tools/ler-feeds.py 2026-10-23 > novidades.json

Os feeds vêm de PEOPLE (campo rss dos canais) e de ORGS (décimo campo) no index.html.
A saída é uma lista de itens com fonte, data, título, link e descrição do feed. Os resumos
do site continuam sendo escritos à mão a partir dela: o conteúdo dos feeds é de terceiros.
"""
import concurrent.futures as cf
import email.utils
import json
import pathlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (Macintosh) GlobalVillageFeedReader/1.0"


def fontes():
    s = (ROOT / "index.html").read_text(encoding="utf-8")
    linhas = s.split("\n")
    out = []
    i = linhas.index("const PEOPLE = [") + 1
    while not linhas[i].strip().startswith("].map"):
        m = re.match(r'^ \["([^"]+)","([^"]+)",.*rss:"([^"]+)"', linhas[i])
        if m:
            out.append({"tipo": "pessoa", "id": m.group(1), "nome": m.group(2), "feed": m.group(3)})
        i += 1
    i = linhas.index("const ORGS = [") + 1
    while not linhas[i].strip().startswith("].map"):
        t = linhas[i].strip().rstrip(",")
        if t.startswith('["'):
            a = json.loads(t)
            if len(a) > 9 and a[9]:
                out.append({"tipo": "org", "id": a[7], "nome": a[0], "feed": a[9]})
        i += 1
    return out


def baixar(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "15", "-A", UA, url], capture_output=True)
    return r.stdout.decode("utf-8", "replace")


def data(texto):
    texto = (texto or "").strip()
    try:
        return email.utils.parsedate_to_datetime(texto).date().isoformat()
    except Exception:
        m = re.match(r"(\d{4}-\d{2}-\d{2})", texto)
        return m.group(1) if m else ""


def itens(xml):
    try:
        raiz = ET.fromstring(xml.encode("utf-8"))
    except Exception:
        return []
    out = []
    for it in raiz.iter():
        if it.tag.split("}")[-1] not in ("item", "entry"):
            continue
        filho = {c.tag.split("}")[-1]: c for c in it}
        # Element sem filhos é falso em Python: comparar com None, nunca usar "or".
        quando = next((filho[k] for k in ("pubDate", "published", "updated", "date") if k in filho), None)
        desc = next((filho[k] for k in ("description", "summary") if k in filho), None)
        link = filho.get("link")
        out.append({
            "titulo": (filho["title"].text or "").strip() if "title" in filho else "",
            "url": ((link.text or link.get("href") or "").strip()) if link is not None else "",
            "data": data(quando.text if quando is not None else ""),
            "autor": (filho["creator"].text or "").strip() if "creator" in filho else "",
            "descricao": re.sub(r"<[^>]+>", " ", (desc.text or "") if desc is not None else "")[:600],
        })
    return out


def main():
    desde = sys.argv[1]
    lista = fontes()
    with cf.ThreadPoolExecutor(16) as ex:
        resultados = ex.map(lambda f: (f, itens(baixar(f["feed"]))), lista)
    saida, vistos = [], set()
    for f, its in resultados:
        for it in its:
            if it["data"] >= desde and it["url"] not in vistos:
                vistos.add(it["url"])
                saida.append({"fonte": f["nome"], "tipo": f["tipo"], "id": f["id"], **it})
    saida.sort(key=lambda x: x["data"], reverse=True)
    json.dump(saida, sys.stdout, ensure_ascii=False, indent=1)
    print(f"{len(lista)} feeds, {len(saida)} itens desde {desde}", file=sys.stderr)


if __name__ == "__main__":
    main()
