"""Jev: API TypeSafe bezposrednio vs OpenRouter (/api/alpha/decisions) - ten sam format zapytania, CRT + matura (tylko dane publiczne),
3 przebiegi na droge, naprzemiennie. Zapisuje model zwrocony przez kazda droge, czas z Warszawy, czas serwera (TypeSafe), id generacji (OpenRouter)."""
import json, os, sys, time, statistics as st
import requests

TU = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(TU, "..", "weryfikacja")); sys.path.insert(0, os.path.join(TU, "..", "etap3")); sys.path.insert(0, TU)
from bench_jev import TS_KEY, OR_KEY  # noqa
import jev_antena as JA  # noqa (licznik tokenow Jev)
from llm_antena import dolicz, wydane  # noqa (licznik OpenRouter)
from test_pokaz import zadania  # noqa

Z = zadania("crt") + zadania("matura")


def body(z):
    stan = {k: z[k] for k in ("material_zrodlowy", "polecenie", "tresc") if z.get(k)}
    q = ({"odp": {"type": "choice", "instructions": "Która odpowiedź jest poprawna?", "criteria": z["opcje"]}} if z["typ"] == "choice"
         else {"odp": {"type": "noul", "instructions": "Czy to stwierdzenie jest prawdziwe?"}})
    return stan, q


sd = requests.Session(); sd.headers.update({"Authorization": f"Bearer {TS_KEY}"})
so = requests.Session(); so.headers.update({"Authorization": f"Bearer {OR_KEY}"})
wyn = []
for przebieg in range(3):
    for droga in ("bezposrednio", "openrouter"):
        for z in Z:
            stan, q = body(z)
            t0 = time.perf_counter()
            if droga == "bezposrednio":
                r = sd.post(JA.URL, json={"model": "jev-latest", "state": stan, "questions": q}, timeout=60)
            else:
                r = so.post("https://openrouter.ai/api/alpha/decisions", json={"model": "typesafe/jev-1.13", "state": stan, "questions": q}, timeout=60)
            dt = time.perf_counter() - t0
            d = r.json(); u = d.get("usage") or {}
            if droga == "bezposrednio":
                JA.dolicz(u.get("input_tokens") or 0)
            else:
                dolicz(u.get("cost") or 0)
            a = (d.get("answers") or {}).get("odp") or {}
            odp = a.get("choice") if z["typ"] == "choice" else (None if a.get("noul") is None else a["noul"] > 0.5)
            wyn.append({"przebieg": przebieg + 1, "droga": droga, "id": z["id"], "http": r.status_code, "model": d.get("model"),
                        "odp": odp, "poprawna": z["poprawna"], "trafna": odp == z["poprawna"], "surowa": a, "s": round(dt, 3),
                        "serwer_ms": r.headers.get("x-envoy-upstream-service-time"), "id_generacji": r.headers.get("X-Generation-Id"),
                        "tok_in": u.get("input_tokens"), "koszt_usd": u.get("cost")})
        print(przebieg + 1, droga, "gotowe", flush=True)
json.dump({"data": time.strftime("%Y-%m-%d %H:%M:%S %z"), "wyniki": wyn}, open(os.path.join(TU, "wyniki_kanaly.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for droga in ("bezposrednio", "openrouter"):
    w = [x for x in wyn if x["droga"] == droga]
    for p in (1, 2, 3):
        wp = [x for x in w if x["przebieg"] == p]
        print(f"{droga:13s} przebieg {p}: trafnych {sum(x['trafna'] for x in wp)}/{len(wp)}, p50 {st.median(x['s'] for x in wp):.3f}s, p95 {sorted(x['s'] for x in wp)[int(.95*len(wp))]:.3f}s")
    print("   modele:", sorted({x['model'] for x in w}), "| bledy http:", sum(x['http'] != 200 for x in w), "| koszt OR:", round(sum(x['koszt_usd'] or 0 for x in w), 5))
print("zgodnosc odpowiedzi miedzy drogami (ten sam przebieg):",
      sum(1 for x in wyn if x["droga"] == "bezposrednio" for y in wyn if y["droga"] == "openrouter" and y["id"] == x["id"] and y["przebieg"] == x["przebieg"] and y["odp"] == x["odp"]), "/", len(wyn) // 2)
print("Jev tok:", JA.budzet(), "| OR seria:", round(wydane(), 3))
