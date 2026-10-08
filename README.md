# su menu · menu digitali di Frigi

Menu digitali bilingui (italiano e inglese) per ristoranti e pizzerie, pubblicati gratis con GitHub Pages.

- Demo: https://frigi03.github.io/menu-demo/
- Ogni cliente ha la sua cartella: `https://frigi03.github.io/menu-demo/<cartella>/`

## Come è fatto

| Cosa | Dove |
|---|---|
| Pagina del menu (uguale per tutti) | `modello/index.html` |
| Piatti, prezzi, allergeni di un locale | `<cartella>/menu.json` |
| QR code da stampare | `qr/<cartella>.png` |
| Script | `strumenti/` |

La pagina sceglie da sola la lingua del telefono (italiano oppure inglese) e ha i pulsanti IT/EN.

## Nuovo cliente

1. `python strumenti/nuovo_cliente.py imperium "Imperium Pizzeria-Bisteccheria"`
2. Compila `imperium/menu.json` (Claude lo fa dalle foto o dal PDF del menu).
3. `python strumenti/controlla_menu.py imperium`
4. Carica su GitHub: il menu è online in 1-2 minuti, il QR code è in `qr/imperium.png`.
5. `python strumenti/cartoncino.py imperium` → `qr/imperium-cartoncini.pdf`: foglio A4 con 4 cartoncini da tavolo (A6) da stampare al 100% su cartoncino.

## Cambiare un piatto o un prezzo

Modifica solo `menu.json` del cliente e carica. Il QR code non cambia mai.

## Formato di menu.json

```json
{
  "nome": "Nome del locale",
  "demo": false,
  "sottotitolo": {"it": "Pizzeria e bisteccheria", "en": "Pizzeria and steakhouse"},
  "piatto_del_giorno": {"it": "…", "en": "…"},
  "coperto": {"it": "Coperto € 2", "en": "Cover charge € 2"},
  "contatti": {"indirizzo": "Via …", "telefono": "…", "orari": {"it": "…", "en": "…"}},
  "colore": "#1f5f7a",
  "categorie": [
    {"id": "pizze", "nome": {"it": "Pizze", "en": "Pizzas"}, "nota": {"it": "…", "en": "…"},
     "piatti": [
       {"nome": {"it": "Margherita", "en": "Margherita"},
        "descrizione": {"it": "Pomodoro, mozzarella, basilico", "en": "Tomato, mozzarella, basil"},
        "prezzo": 7, "tipico": false, "vegetariano": true, "allergeni": [1, 7]}
     ]}
  ]
}
```

`piatto_del_giorno`, `coperto`, `contatti`, `colore` e `nota` sono facoltativi (`null` o assenti).
`prezzo` può essere un numero (`7`, `7.5`) o un testo (`"5/hg"`, `"6 / 24"`).

Allergeni (Reg. UE 1169/2011): 1 Glutine · 2 Crostacei · 3 Uova · 4 Pesce · 5 Arachidi · 6 Soia · 7 Latte ·
8 Frutta a guscio · 9 Sedano · 10 Senape · 11 Sesamo · 12 Solfiti · 13 Lupini · 14 Molluschi.
