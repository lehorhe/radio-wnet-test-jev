"""Test pokazowy „Pierwsza sekunda” - Jev vs modele LLM na CRT i maturze 2026 (zadania zamkniete).
Zapisuje KAZDE zapytanie i odpowiedz w calosci + identyfikatory (x-typesafe-request-id, id generacji OpenRouter),
zeby czytelnicy mogli wszystko sprawdzic. Opcje w CRT tasowane deterministycznie (litery A-D).
Uzycie: python test_pokaz.py crt|matura [modele...]"""
import json, os, random, re, sys, time, threading
from concurrent.futures import ThreadPoolExecutor
import requests

TU = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(TU, "..", "weryfikacja")); sys.path.insert(0, os.path.join(TU, "..", "etap3"))
from bench_jev import TS_KEY, OR_KEY  # noqa
import jev_antena as JA  # noqa  (licznik budzetu Jev)
from llm_antena import dolicz, wydane, STOP_USD  # noqa  (licznik budzetu OpenRouter)

MODELE = ["anthropic/claude-opus-5.5", "openai/gpt-6-astra", "google/gemini-3.8-flash",
          "anthropic/claude-haiku-4.5", "openai/gpt-5.4-mini"]


def zadania(zb):
    if zb == "crt":
        out = []
        for z in json.load(open(os.path.join(TU, "zadania_crt.json"), encoding="utf-8")):
            klucze = list(z["opcje"]); random.Random(z["id"]).shuffle(klucze)
            litery = "ABCD"
            opc = {litery[i]: z["opcje"][k] for i, k in enumerate(klucze)}
            out.append({"id": z["id"], "typ": "choice", "material_zrodlowy": "", "polecenie": "Wybierz poprawną odpowiedź.",
                        "tresc": z["tresc"], "opcje": opc, "poprawna": litery[klucze.index("poprawna")],
                        "intuicyjna": litery[klucze.index("intuicyjna")], "zrodlo": z["zrodlo"]})
        return out
    return [json.loads(l) for l in open(os.path.join(TU, "zadania_matura.jsonl"), encoding="utf-8")]


def jev(s, z):
    stan = {k: z[k] for k in ("material_zrodlowy", "polecenie", "tresc") if z.get(k)}
    if z["typ"] == "choice":
        q = {"odp": {"type": "choice", "instructions": "Która odpowiedź jest poprawna?", "criteria": z["opcje"]}}
    else:
        q = {"odp": {"type": "noul", "instructions": "Czy to stwierdzenie jest prawdziwe?"}}
    body = {"model": "jev-latest", "state": stan, "questions": q}
    t0 = time.perf_counter()
    r = s.post(JA.URL, json=body, timeout=60)
    dt = time.perf_counter() - t0
    d = r.json(); tok = (d.get("usage") or {}).get("input_tokens") or 0; JA.dolicz(tok)
    a = (d.get("answers") or {}).get("odp") or {}
    if z["typ"] == "choice":
        odp, p = a.get("choice"), (a.get("probabilities") or {}).get(a.get("choice"))
    else:
        pn = a.get("noul"); odp = None if pn is None else pn > 0.5; p = None if pn is None else max(pn, 1 - pn)
    return {"model": "typesafe/jev-latest", "model_faktyczny": d.get("model"), "odp": odp, "pewnosc": p, "surowa": a,
            "s": round(dt, 3), "serwer_ms": r.headers.get("x-envoy-upstream-service-time"),
            "request_id": r.headers.get("x-typesafe-request-id"), "tok_in": tok, "koszt_usd": tok * 0.042e-6,
            "zapytanie": body}


def llm(s, model, z):
    if wydane() > STOP_USD:
        return {"model": model, "blad": "STOP budzet"}
    txt = ""
    if z.get("material_zrodlowy"):
        txt += "Materiał źródłowy:\n" + z["material_zrodlowy"] + "\n\n"
    txt += z["polecenie"] + "\n" + z["tresc"] + "\n"
    if z["typ"] == "choice":
        txt += "\n".join(f"{k}. {v}" for k, v in z["opcje"].items())
        txt += '\n\nOdpowiedz WYŁĄCZNIE obiektem JSON: {"odp": "<litera>", "pewnosc": <0-1>}'
    else:
        txt += '\nCzy to stwierdzenie jest prawdziwe? Odpowiedz WYŁĄCZNIE obiektem JSON: {"odp": true|false, "pewnosc": <0-1>}'
    body = {"model": model, "messages": [{"role": "user", "content": txt}], "usage": {"include": True}, "max_tokens": int(os.environ.get("MAXTOK", "8000"))}
    t0 = time.perf_counter()
    try:
        r = s.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers={"Authorization": f"Bearer {OR_KEY}"}, timeout=300)
        d = r.json()
    except Exception as e:
        return {"model": model, "blad": str(e)[:200], "s": time.perf_counter() - t0}
    dt = time.perf_counter() - t0
    u = d.get("usage") or {}; koszt = u.get("cost") or 0.0; dolicz(koszt)
    c = ((d.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
    from parsuj import parsuj  # ostatni obiekt JSON z polem "odp" (LaTeX \frac{..} nie jest JSON-em)
    odp, p = parsuj(c, z["typ"])
    return {"model": model, "model_faktyczny": d.get("model"), "provider": d.get("provider"), "odp": odp, "pewnosc": p,
            "surowa": c, "s": round(dt, 3), "generation_id": d.get("id"), "tok_in": u.get("prompt_tokens"),
            "tok_out": u.get("completion_tokens"), "tok_rozumowania": (u.get("completion_tokens_details") or {}).get("reasoning_tokens"),
            "koszt_usd": koszt, "zapytanie": body, "blad": None if odp is not None else (c or str(d))[:300]}


if __name__ == "__main__":
    zb = sys.argv[1]; modele = sys.argv[2:] or MODELE
    Z = zadania(zb)
    sj = requests.Session(); sj.headers.update({"Authorization": f"Bearer {TS_KEY}"})
    wyn = {"zbior": zb, "data": time.strftime("%Y-%m-%d %H:%M:%S %z"), "zadania": Z, "odpowiedzi": []}
    for z in Z:
        w = jev(sj, z); w["id"] = z["id"]; wyn["odpowiedzi"].append(w)
    print("Jev gotowy", sum(1 for w in wyn["odpowiedzi"] if w["odp"] == next(z["poprawna"] for z in Z if z["id"] == w["id"])), "/", len(Z), flush=True)
    lok = threading.local()

    def ses():
        if not hasattr(lok, "s"):
            lok.s = requests.Session()
        return lok.s

    def bieg(model):
        with ThreadPoolExecutor(int(os.environ.get("RWN", "4"))) as ex:
            out = list(ex.map(lambda z: dict(llm(ses(), model, z), id=z["id"]), Z))
        print(model, "gotowy", f"OR {wydane():.3f} USD", flush=True)
        return out

    with ThreadPoolExecutor(len(modele)) as ex:
        for out in ex.map(bieg, modele):
            wyn["odpowiedzi"] += out
    json.dump(wyn, open(os.path.join(TU, f"wyniki_{zb}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
