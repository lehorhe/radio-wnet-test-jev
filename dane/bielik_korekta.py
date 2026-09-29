"""Bielik 11B v3 (lokalnie, ZBook/LM Studio przez tunel :12340) jako redaktor i korektor „starej daty”.
Akapit po akapicie: poprawki z nazwą znaku korektorskiego (PN-P-55366). Walidacja: fragment musi istnieć dosłownie w akapicie.
T=0.1 (korekta = zadanie deterministyczne; odrobina swobody tylko w propozycjach stylistycznych)."""
import html, json, os, re, sys, time
import requests

A = r"D:\TECH\jev_testy\pokaz\artykul\artykul.html"
URL = "http://127.0.0.1:12340/v1/chat/completions"
ZNAKI = ["skreślenie (dele)", "wstawienie", "zamiana liter/wyrazów", "przestawienie (transpozycja)", "spacja – dodać", "spacja – usunąć",
         "nowy akapit", "połączenie akapitów", "wielka litera", "mała litera", "kursywa", "zmiana interpunkcji", "łącznik/półpauza/pauza", "cudzysłów", "redakcyjna – przeredagować"]
SYS = ("Jesteś doświadczoną polską redaktorką i korektorką prasową starej daty. Poprawiasz tekst jak na maszynopisie: tylko to, co konieczne. "
       "Dwa rodzaje uwag: KOREKTA (ortografia, interpunkcja, typografia: cudzysłowy „…”, półpauza –, spacje, wielkie/małe litery, odmiana) "
       "oraz REDAKCJA (składnia, styl, kalki z angielskiego, powtórzenia, niejasność). Nie zmieniaj faktów, liczb, nazw własnych ani cytatów w cudzysłowie. "
       "Odpowiadasz WYŁĄCZNIE tablicą JSON: [{\"fragment\": \"<dokładnie skopiowany fragment akapitu, 1-8 słów>\", \"poprawka\": \"<nowe brzmienie tego fragmentu>\", "
       "\"rodzaj\": \"korekta\"|\"redakcja\", \"znak\": \"<jeden z: " + "; ".join(ZNAKI) + ">\", \"uzasadnienie\": \"<krótko, po polsku>\"}]. "
       "Jeśli akapit jest poprawny, zwróć []. Najwyżej 4 uwagi na akapit.")


def akapity():
    s = open(A, encoding="utf-8").read()
    s = s[s.index("<main>"):s.index('<div class="ramka bursztyn" id="przylap">')]   # bez ramek technicznych i źródeł
    s = re.sub(r"<(script|style|audio)[\s\S]*?(</\1>|>)", "", s)
    out = []
    for m in re.finditer(r"<(h1|h2|h3|p|blockquote|figcaption)[^>]*>([\s\S]*?)</\1>", s):
        t = html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
        t = re.sub(r"\s+", " ", t)
        if len(t.split()) >= 4:
            out.append({"tag": m.group(1), "tekst": t})
    return out


def bielik(t):
    body = {"model": "bielik-korektor", "temperature": 0.1, "max_tokens": 900,
            "messages": [{"role": "system", "content": SYS}, {"role": "user", "content": "Akapit:\n" + t}]}
    t0 = time.perf_counter()
    d = requests.post(URL, json=body, timeout=300).json()
    c = d["choices"][0]["message"].get("content") or ""
    m = re.search(r"\[[\s\S]*\]", c)
    try:
        return json.loads(m.group(0)), time.perf_counter() - t0, d.get("usage", {})
    except Exception:
        return [{"blad_parsowania": c[:300]}], time.perf_counter() - t0, d.get("usage", {})


if __name__ == "__main__":
    P = akapity(); wyn = []; odrz = 0; tok = 0; T = 0
    for i, a in enumerate(P):
        u, dt, us = bielik(a["tekst"]); T += dt; tok += us.get("completion_tokens", 0) or 0
        dobre = []
        for x in u:
            f = (x.get("fragment") or "").strip()
            if f and f in a["tekst"] and x.get("poprawka") and x["poprawka"].strip() != f:
                dobre.append(x)
            else:
                odrz += 1
        wyn.append({"nr": i, "tag": a["tag"], "tekst": a["tekst"], "uwagi": dobre, "s": round(dt, 1)})
        print(i, a["tag"], f"{dt:.1f}s", len(dobre), "uwag |", " ; ".join(f"{x['fragment']} → {x['poprawka']} [{x.get('znak')}]" for x in dobre)[:260], flush=True)
    json.dump({"model": "Bielik 11B v3.0 Instruct Q8_0 (lokalnie, LM Studio, ZBook)", "temperatura": 0.1, "akapity": wyn,
               "odrzucone_niedosłowne": odrz, "czas_s": round(T, 1), "tokeny_wyjscia": tok},
              open(os.path.join(os.path.dirname(A), "..", "bielik_korekta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("akapitów", len(P), "uwag przyjętych do oceny", sum(len(w["uwagi"]) for w in wyn), "odrzuconych (fragment nie istnieje)", odrz, "czas", round(T), "s")
