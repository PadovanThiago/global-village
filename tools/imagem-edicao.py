"""Gera a imagem de abertura de uma edição (1200 × 600, em alta resolução).

Uso:
  python3 -I tools/imagem-edicao.py brand/newsletter/2026-10-28-pt.png \
      "28 de outubro de 2026" "Título curto do dia" "Fato 1" "Fato 2" "Fato 3"

Recebe a data já escrita no idioma da edição, um título de até umas 40 letras e de 3 a 5 fatos curtos.
Usa o Chrome headless e o molde brand/newsletter/src/edicao.html.
"""
import pathlib
import subprocess
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main():
    if len(sys.argv) < 7:
        sys.exit(__doc__)
    saida = pathlib.Path(sys.argv[1]).resolve()
    data, titulo, fatos = sys.argv[2], sys.argv[3], sys.argv[4:9]
    if not 3 <= len(fatos) <= 5:
        sys.exit("São de 3 a 5 fatos.")
    query = urllib.parse.urlencode([("data", data), ("titulo", titulo)] + [("fato", f) for f in fatos])
    molde = (ROOT / "brand/newsletter/src/edicao.html").as_uri() + "?" + query
    saida.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--force-device-scale-factor=2", "--window-size=1200,600", "--virtual-time-budget=8000",
                    "--screenshot=" + str(saida), molde], check=True, capture_output=True)
    print(saida)


if __name__ == "__main__":
    main()
