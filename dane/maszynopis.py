"""Render „maszynopisu” z poprawkami Bielika naniesionymi ołówkiem: znak w tekście + ten sam znak z poprawką na marginesie (zasada korekty PN-P-55366).
Znaki uproszczone graficznie; nazwa znaku w dymku. Wejście: bielik_korekta.json (+ decyzje.json jeśli istnieje: przyjęte/odrzucone przez redakcję)."""
import html, json, os
B = r"D:\TECH\jev_testy\pokaz"
K = json.load(open(os.path.join(B, "bielik_korekta.json"), encoding="utf-8"))
D = json.load(open(os.path.join(B, "bielik_decyzje.json"), encoding="utf-8")) if os.path.exists(os.path.join(B, "bielik_decyzje.json")) else {}
SYM = {"skreślenie (dele)": "ꝺ", "wstawienie": "⌐", "zamiana liter/wyrazów": "⌐", "przestawienie (transpozycja)": "⟲", "spacja – dodać": "#",
       "spacja – usunąć": "⁀", "nowy akapit": "⌐¶", "połączenie akapitów": "⌒", "wielka litera": "≡", "mała litera": "/", "kursywa": "〰",
       "zmiana interpunkcji": "⌐", "łącznik/półpauza/pauza": "⌐–", "cudzysłów": "⌐„", "redakcyjna – przeredagować": "?"}
KOL = ["#1f3a8a", "#7a1f1f", "#1f5f3a", "#6b4a1f"]


def akapit(a):
    t = a["tekst"]; marg = []; uw = sorted(a["uwagi"], key=lambda x: t.find(x["fragment"]))
    out, poz = "", 0
    for j, x in enumerate(uw):
        i = t.find(x["fragment"], poz)
        if i < 0:
            continue
        znak = x.get("znak") or "redakcyjna – przeredagować"; sym = SYM.get(znak, "⌐"); kol = KOL[j % len(KOL)]
        dec = D.get(f'{a["nr"]}:{x["fragment"]}', "")
        cls = "kor" + (" red" if x.get("rodzaj") == "redakcja" else "") + (f" {dec}" if dec else "")
        out += html.escape(t[poz:i]) + f'<span class="{cls}" style="--k:{kol}" title="{html.escape(znak)}: {html.escape(x.get("uzasadnienie",""))}"><s>{html.escape(x["fragment"])}</s><sup>{sym}</sup></span>'
        poz = i + len(x["fragment"])
        marg.append(f'<div class="m {dec}" style="--k:{kol}"><b>{sym}</b> {html.escape(x["poprawka"])}<small>{html.escape(znak)}{" · " + dec if dec else ""}</small></div>')
    out += html.escape(t[poz:])
    tag = "h" if a["tag"].startswith("h") else "p"
    return f'<div class="wiersz"><div class="tx {tag}">{out}</div><div class="margines">{"".join(marg)}</div></div>'


n = sum(len(a["uwagi"]) for a in K["akapity"])
nk = sum(1 for a in K["akapity"] for x in a["uwagi"] if x.get("rodzaj") == "korekta")
strona = f"""<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Maszynopis z korektą Bielika – Radio Wnet</title>
<link href="https://fonts.googleapis.com/css2?family=Courier+Prime&family=Caveat:wght@500;700&family=Exo+2:wght@700&display=swap" rel="stylesheet">
<style>
:root{{--papier:#f6f1e3;--tusz:#222;--olowek:#555;--tlo:#d9d4c7}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--tlo:#1b1a17}}}}
body{{margin:0;background:var(--tlo);font:16px/1 "Courier Prime",monospace;color:var(--tusz)}}
.naglowek{{max-width:900px;margin:24px auto 0;padding:0 16px;font:700 22px/1.3 "Exo 2",sans-serif;color:#274f5c}}
.naglowek p{{font:15px/1.5 system-ui,sans-serif;color:#444;margin:8px 0 0}}
@media (prefers-color-scheme: dark){{.naglowek,.naglowek p{{color:#cfd8dc}}}}
.kartka{{max-width:900px;margin:18px auto 40px;background:var(--papier);box-shadow:0 2px 12px #0004;padding:48px 16px 60px 16px;
  background-image:repeating-linear-gradient(transparent 0 35px,#0000000a 35px 36px)}}
.wiersz{{display:grid;grid-template-columns:1fr 230px;gap:18px;margin:0 0 22px}}
@media (max-width:700px){{.wiersz{{grid-template-columns:1fr}} .margines{{border-left:2px dashed #9995;padding-left:8px}}}}
.tx{{line-height:36px;font-size:16px;letter-spacing:.2px}} .tx.h{{font-weight:bold;text-transform:uppercase}}
.kor{{position:relative;white-space:normal}}
.kor s{{text-decoration:line-through;text-decoration-color:var(--k);text-decoration-thickness:2px}}
.kor.red s{{text-decoration:underline wavy var(--k);text-decoration-thickness:1.5px}}
.kor sup{{font:700 20px "Caveat",cursive;color:var(--k);margin-left:1px}}
.margines .m{{font:500 21px/1.1 "Caveat",cursive;color:var(--k);margin-bottom:10px;transform:rotate(-1.5deg)}}
.margines .m b{{font-size:24px;margin-right:4px}} .margines small{{display:block;font:12px/1.3 system-ui,sans-serif;color:#666;transform:none}}
.odrzucona{{opacity:.45}} .m.odrzucona b{{text-decoration:line-through}}
.stopka{{max-width:900px;margin:0 auto 40px;padding:0 16px;font:13px/1.5 system-ui,sans-serif;color:#555}}
</style></head><body>
<div class="naglowek">Maszynopis z korektą: Bielik 11B jako redaktor starej daty
<p>Każdą poprawkę zaznaczono jak ołówkiem na maszynopisie: znak w tekście i ten sam znak z nowym brzmieniem na marginesie. Linia prosta = korekta (ortografia, interpunkcja, typografia), linia falista = uwaga redakcyjna (styl, składnia). Najedź na poprawkę, żeby zobaczyć nazwę znaku i uzasadnienie. {n} uwag ({nk} korektorskich, {n-nk} redakcyjnych); {K['odrzucone_niedosłowne']} propozycji odrzucono automatycznie, bo wskazywały fragmenty, których w tekście nie ma.</p></div>
<div class="kartka">{''.join(akapit(a) for a in K['akapity'])}</div>
<div class="stopka">{html.escape(K['model'])}, temperatura {K['temperatura']}, łączny czas pracy {K['czas_s']} s na lokalnym komputerze redakcji (bez chmury, bez kosztu tokenów). Znaki korektorskie oddane w uproszczeniu graficznym, nazwy według polskiej normy znaków korektorskich (PN-P-55366). Uwagi oznaczone jako „odrzucona” redakcja rozpatrzyła i nie przyjęła.</div>
</body></html>"""
open(os.path.join(B, "artykul", "maszynopis.html"), "w", encoding="utf-8").write(strona)
print("maszynopis:", n, "uwag")
