"""Gera os slides do carrossel do Instagram (1080 × 1350) a partir de um JSON.

Uso:
  python3 -I tools/carrossel.py brand/instagram/2026-11-10-pt.json brand/instagram/2026-11-10-pt/

O JSON tem "data" e "slides", cada slide com "tipo" (capa, fato, humor, final) e os campos
titulo, texto, kicker, n, fontes, pecas, balao, url. Usa o Chrome headless e o molde
brand/instagram/src/carrossel.html.
"""
import json
import pathlib
import subprocess
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    dados = json.loads(pathlib.Path(sys.argv[1]).read_text())
    saida = pathlib.Path(sys.argv[2]).resolve()
    saida.mkdir(parents=True, exist_ok=True)
    total = len(dados["slides"])
    for i, s in enumerate(dados["slides"], 1):
        s = dict(s, data=s.get("data", dados["data"]), pagina=f"{i}/{total}")
        molde = (ROOT / "brand/instagram/src/carrossel.html").as_uri() + "?" + urllib.parse.urlencode({"s": json.dumps(s, ensure_ascii=False)})
        png = saida / f"{i:02d}.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                        "--force-device-scale-factor=1", "--window-size=1080,1350", "--virtual-time-budget=8000",
                        "--screenshot=" + str(png), molde], check=True, capture_output=True)
        print(png)


if __name__ == "__main__":
    main()
