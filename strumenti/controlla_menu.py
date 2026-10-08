#!/usr/bin/env python3
"""
Controlla un menu.json prima di pubblicarlo.

Uso:
    python strumenti/controlla_menu.py <cartella>      es. imperium   (o "." per la demo)

Segnala: traduzioni inglesi mancanti, prezzi assenti, allergeni fuori dall'elenco UE (1-14),
categorie vuote o con id doppio.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    cart = sys.argv[1] if len(sys.argv) > 1 else "."
    path = ROOT / cart / "menu.json"
    try:
        m = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        sys.exit(f"ERRORE: non riesco a leggere {path}: {e}")

    problemi = []
    if not m.get("nome"):
        problemi.append("manca il nome del locale")
    ids = set()
    n_piatti = 0
    for c in m.get("categorie", []):
        cid = c.get("id", "")
        if not cid or cid in ids:
            problemi.append(f"categoria con id mancante o doppio: '{cid}'")
        ids.add(cid)
        if not c.get("nome", {}).get("en"):
            problemi.append(f"categoria '{cid}': manca il nome in inglese")
        if not c.get("piatti"):
            problemi.append(f"categoria '{cid}': nessun piatto")
        for d in c.get("piatti", []):
            n_piatti += 1
            nome = d.get("nome", {}).get("it") or "(senza nome)"
            if not d.get("nome", {}).get("it"):
                problemi.append(f"[{cid}] piatto senza nome italiano")
            if not d.get("nome", {}).get("en"):
                problemi.append(f"[{cid}] {nome}: manca il nome in inglese")
            if d.get("descrizione", {}).get("it") and not d.get("descrizione", {}).get("en"):
                problemi.append(f"[{cid}] {nome}: manca la descrizione in inglese")
            if d.get("prezzo") in (None, "", 0):
                problemi.append(f"[{cid}] {nome}: prezzo mancante")
            for a in d.get("allergeni", []):
                if not isinstance(a, int) or not 1 <= a <= 14:
                    problemi.append(f"[{cid}] {nome}: allergene non valido {a!r} (usa i numeri 1-14)")

    print(f"{m.get('nome', '?')}: {len(m.get('categorie', []))} categorie, {n_piatti} piatti")
    if problemi:
        print(f"{len(problemi)} cose da sistemare:")
        for p in problemi:
            print(" -", p)
        sys.exit(1)
    print("Tutto a posto: si può pubblicare.")


if __name__ == "__main__":
    main()
