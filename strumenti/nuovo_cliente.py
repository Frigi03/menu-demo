#!/usr/bin/env python3
"""
Crea il menu digitale di un nuovo cliente.

Uso:
    python strumenti/nuovo_cliente.py <cartella> "<Nome del locale>"
    es. python strumenti/nuovo_cliente.py imperium "Imperium Pizzeria-Bisteccheria"

Cosa fa:
  1. crea la cartella <cartella>/ con il modello (index.html) e un menu.json da compilare
  2. crea il QR code in qr/<cartella>.png (da stampare per i tavoli)
  3. stampa il link pubblico del menu

Se la cartella esiste già, aggiorna solo index.html all'ultima versione del modello
e rigenera il QR code: il menu.json del cliente non viene mai toccato.
"""
import json
import re
import shutil
import sys
from pathlib import Path

import qrcode

BASE_URL = "https://frigi03.github.io/menu-demo"
ROOT = Path(__file__).resolve().parent.parent

MENU_VUOTO = {
    "nome": "",
    "demo": False,
    "sottotitolo": {"it": "", "en": ""},
    "piatto_del_giorno": None,
    "coperto": None,
    "contatti": {"indirizzo": "", "telefono": "", "orari": {"it": "", "en": ""}},
    "categorie": [
        {
            "id": "antipasti",
            "nome": {"it": "Antipasti", "en": "Starters"},
            "piatti": [
                {
                    "nome": {"it": "", "en": ""},
                    "descrizione": {"it": "", "en": ""},
                    "prezzo": 0,
                    "tipico": False,
                    "vegetariano": False,
                    "allergeni": [],
                }
            ],
        }
    ],
}


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    slug = sys.argv[1].strip().lower()
    nome = sys.argv[2].strip()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,40}", slug) or slug in {"modello", "strumenti", "qr"}:
        sys.exit("Nome cartella non valido: usa lettere minuscole, numeri e trattini (es. da-mirko).")

    cartella = ROOT / slug
    cartella.mkdir(exist_ok=True)
    shutil.copyfile(ROOT / "modello" / "index.html", cartella / "index.html")

    menu = cartella / "menu.json"
    if not menu.exists():
        dati = json.loads(json.dumps(MENU_VUOTO))
        dati["nome"] = nome
        menu.write_text(json.dumps(dati, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Creato {menu.relative_to(ROOT)}: compilalo con i piatti del locale.")
    else:
        print(f"{menu.relative_to(ROOT)} esiste già: non l'ho toccato, ho aggiornato solo la pagina.")

    url = f"{BASE_URL}/{slug}/"
    (ROOT / "qr").mkdir(exist_ok=True)
    img = qrcode.make(url, box_size=20, border=2)
    qr_path = ROOT / "qr" / f"{slug}.png"
    img.save(qr_path)
    print(f"QR code: {qr_path.relative_to(ROOT)}")
    print(f"Link del menu: {url}")


if __name__ == "__main__":
    main()
