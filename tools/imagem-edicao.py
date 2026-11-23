"""Gera a imagem de abertura de uma edição (1200 × 600, em alta resolução).

Uso:
  python3 -I tools/imagem-edicao.py brand/newsletter/2026-10-28-pt.png \
      "28 de outubro de 2026" "Título curto do dia" "Fato 1" "Fato 2" "Fato 3"

Recebe a data já escrita no idioma da edição, um título de até umas 40 letras e de 3 a 5 fatos curtos.
Usa o Chrome headless e o molde brand/newsletter/src/edicao.html.

Opções, antes dos argumentos, para a capa não sair igual todo dia:
  --paleta noite|papel|terracota|oliva   cor de fundo (noite é a padrão)
  --imagem caminho/da/imagem.png          charge, meme, post ou foto do dia, na metade direita
  --credito "Texto do crédito"            obrigatório quando há imagem
  --post                                  mostra a imagem inteira, sem cortar (posts e charges)
"""
import pathlib
import subprocess
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def opcoes(args):
    extra, resto = [], list(args)
    while resto and resto[0].startswith("--"):
        nome = resto.pop(0)[2:]
        if nome == "post":
            extra.append(("enquadre", "post"))
        elif nome in ("paleta", "credito"):
            extra.append((nome, resto.pop(0)))
        elif nome == "imagem":
            extra.append(("imagem", pathlib.Path(resto.pop(0)).resolve().as_uri()))
        else:
            sys.exit(f"Opção desconhecida: --{nome}")
    if any(k == "imagem" for k, _ in extra) and not any(k == "credito" for k, _ in extra):
        sys.exit("Imagem de terceiros sempre leva --credito.")
    return extra, resto


def main():
    extra, args = opcoes(sys.argv[1:])
    if len(args) < 6:
        sys.exit(__doc__)
    saida = pathlib.Path(args[0]).resolve()
    data, titulo, fatos = args[1], args[2], args[3:8]
    if not 3 <= len(fatos) <= 5:
        sys.exit("São de 3 a 5 fatos.")
    query = urllib.parse.urlencode([("data", data), ("titulo", titulo)] + [("fato", f) for f in fatos] + extra)
    molde = (ROOT / "brand/newsletter/src/edicao.html").as_uri() + "?" + query
    saida.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--force-device-scale-factor=2", "--window-size=1200,600", "--virtual-time-budget=8000",
                    "--screenshot=" + str(saida), molde], check=True, capture_output=True)
    print(saida)


if __name__ == "__main__":
    main()
