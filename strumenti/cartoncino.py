#!/usr/bin/env python3
"""
Crea i cartoncini da tavolo con il QR code del menu di un cliente.

Uso:
    python strumenti/cartoncino.py <cartella>        es. imperium
    python strumenti/cartoncino.py demo              (la demo Locanda Maestrale)

Risultato: qr/<cartella>-cartoncini.pdf, un foglio A4 con 4 cartoncini A6
(105 x 148 mm) e i segni di taglio. Si stampa a casa o in copisteria al 100%,
senza "adatta alla pagina", meglio su cartoncino da 250-300 g.
"""
import json
import sys
from io import BytesIO
from pathlib import Path

import qrcode
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

BASE_URL = "https://frigi03.github.io/menu-demo"
ROOT = Path(__file__).resolve().parent.parent
FONT = Path(__file__).resolve().parent / "font"

NOTTE = HexColor("#14233a")
MARE = HexColor("#1f5f7a")
ZAFFERANO = HexColor("#d39a1c")
LINO = HexColor("#f6f7f4")
GRIGIO = HexColor("#5d6878")

pdfmetrics.registerFont(TTFont("YoungSerif", FONT / "YoungSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Figtree", FONT / "Figtree-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Figtree-Bold", FONT / "Figtree-Bold.ttf"))

CARD_W, CARD_H = 105 * mm, 148 * mm


def marchio(c, x, y, size):
    """Il marchio su menu (QR con il rombo sardo) disegnato a vettori."""
    s = size / 132
    c.setFillColor(NOTTE)
    c.roundRect(x, y, size, size, 30 * s, stroke=0, fill=1)
    c.setStrokeColor(LINO)
    c.setLineWidth(6 * s)
    for bx, by in ((20, 20), (78, 20), (20, 78)):
        # coordinate SVG (origine in alto) -> PDF (origine in basso)
        c.roundRect(x + bx * s, y + (132 - by - 34) * s, 34 * s, 34 * s, 7 * s, stroke=1, fill=0)
        c.setFillColor(LINO)
        c.roundRect(x + (bx + 11) * s, y + (132 - by - 23) * s, 12 * s, 12 * s, 2 * s, stroke=0, fill=1)
    def rombo(cx, cy, r, col):
        p = c.beginPath()
        p.moveTo(x + cx * s, y + (132 - cy + r) * s)
        p.lineTo(x + (cx + r) * s, y + (132 - cy) * s)
        p.lineTo(x + cx * s, y + (132 - cy - r) * s)
        p.lineTo(x + (cx - r) * s, y + (132 - cy) * s)
        p.close()
        c.setFillColor(col)
        c.drawPath(p, stroke=0, fill=1)
    rombo(95, 95, 19, ZAFFERANO)
    rombo(95, 95, 9, NOTTE)


def qr_image(url):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=20, border=1)
    q.add_data(url)
    q.make(fit=True)
    img = q.make_image(fill_color="#14233a", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def testo_centrato(c, txt, font, size, cx, y, max_w, color):
    while pdfmetrics.stringWidth(txt, font, size) > max_w and size > 8:
        size -= 0.5
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawCentredString(cx, y, txt)


def cartoncino(c, x, y, nome, sottotitolo, qr):
    cx = x + CARD_W / 2
    c.setFillColor(LINO)
    c.rect(x, y, CARD_W, CARD_H, stroke=0, fill=1)
    # fascia alta
    c.setFillColor(NOTTE)
    c.rect(x, y + CARD_H - 34 * mm, CARD_W, 34 * mm, stroke=0, fill=1)
    testo_centrato(c, nome, "YoungSerif", 22, cx, y + CARD_H - 18 * mm, CARD_W - 16 * mm, LINO)
    if sottotitolo:
        testo_centrato(c, sottotitolo, "Figtree", 9.5, cx, y + CARD_H - 26 * mm, CARD_W - 16 * mm, HexColor("#c9d3dc"))
    # invito
    testo_centrato(c, "Inquadra per il menu", "Figtree-Bold", 15, cx, y + CARD_H - 46 * mm, CARD_W - 12 * mm, NOTTE)
    testo_centrato(c, "Scan for the menu · in English", "Figtree", 10.5, cx, y + CARD_H - 52.5 * mm, CARD_W - 12 * mm, MARE)
    # QR
    q = 58 * mm
    c.setFillColor(HexColor("#ffffff"))
    c.roundRect(cx - q / 2 - 3 * mm, y + 26 * mm, q + 6 * mm, q + 6 * mm, 4 * mm, stroke=0, fill=1)
    c.drawImage(qr, cx - q / 2, y + 29 * mm, q, q)
    # info
    testo_centrato(c, "Allergeni indicati per ogni piatto · Allergens listed", "Figtree", 8, cx, y + 19 * mm, CARD_W - 12 * mm, GRIGIO)
    # firma su menu
    m = 6 * mm
    w_txt = pdfmetrics.stringWidth("menu digitale di su menu", "Figtree", 7.5)
    start = cx - (m + 2 * mm + w_txt) / 2
    marchio(c, start, y + 7 * mm, m)
    c.setFont("Figtree", 7.5)
    c.setFillColor(GRIGIO)
    c.drawString(start + m + 2 * mm, y + 9 * mm, "menu digitale di su menu")


def segni_taglio(c, xs, ys):
    c.setStrokeColor(HexColor("#9aa6b6"))
    c.setLineWidth(0.3)
    W, H = A4
    for x in xs:
        c.line(x, 0, x, 6 * mm)
        c.line(x, H - 6 * mm, x, H)
    for y in ys:
        c.line(0, y, 6 * mm, y)
        c.line(W - 6 * mm, y, W, y)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    slug = sys.argv[1].strip().lower()
    cartella = ROOT if slug == "demo" else ROOT / slug
    url = f"{BASE_URL}/" if slug == "demo" else f"{BASE_URL}/{slug}/"
    menu = cartella / "menu.json"
    if not menu.exists():
        sys.exit(f"Non trovo {menu}: crea prima il cliente con nuovo_cliente.py")
    dati = json.loads(menu.read_text(encoding="utf-8"))
    nome = dati.get("nome") or slug
    sott = (dati.get("sottotitolo") or {}).get("it", "")

    (ROOT / "qr").mkdir(exist_ok=True)
    out = ROOT / "qr" / f"{slug}-cartoncini.pdf"
    c = canvas.Canvas(str(out), pagesize=A4)
    c.setTitle(f"Cartoncini QR · {nome}")
    c.setAuthor("su menu")
    W, H = A4
    ox, oy = (W - 2 * CARD_W) / 2, (H - 2 * CARD_H) / 2
    qr = qr_image(url)
    for i in range(2):
        for j in range(2):
            cartoncino(c, ox + i * CARD_W, oy + j * CARD_H, nome, sott, qr)
    segni_taglio(c, [ox, ox + CARD_W, ox + 2 * CARD_W], [oy, oy + CARD_H, oy + 2 * CARD_H])
    c.showPage()
    c.save()
    print(f"Cartoncini: {out.relative_to(ROOT)}  (link nel QR: {url})")


if __name__ == "__main__":
    main()
