"""Wszystkie liczby artykulu liczone z surowych plikow (do niezaleznego przeliczenia przez zespol B)."""
import json, math, os, collections, statistics as st
KURS = 3.70  # PLN/USD - zalozenie, podac w tekscie


def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return round(100 * (c - h)), round(100 * (c + h))


out = {}
for f in ("wyniki_crt.json", "wyniki_matura.json"):
    W = json.load(open(f, encoding="utf-8")); Z = {z["id"]: z for z in W["zadania"]}
    g = collections.defaultdict(list)
    for w in W["odpowiedzi"]:
        g[w["model"]].append(w)
    tab = {}
    for m, ws in g.items():
        k = sum(w.get("odp") == Z[w["id"]]["poprawna"] for w in ws); n = len(ws)
        tab[m] = {"trafne": k, "n": n, "proc": round(100 * k / n), "ci95": wilson(k, n), "p50_s": round(st.median([w.get("s") or 0 for w in ws]), 2),
                  "suma_s": round(sum(w.get("s") or 0 for w in ws), 1), "koszt_usd": round(sum(w.get("koszt_usd") or 0 for w in ws), 4),
                  "koszt_gr": round(100 * KURS * sum(w.get("koszt_usd") or 0 for w in ws), 2)}
        if W["zbior"] == "crt":
            tab[m]["intuicyjne"] = sum(w.get("odp") == Z[w["id"]].get("intuicyjna") for w in ws)
    out[W["zbior"]] = tab
A = json.load(open("porownanie_antena.json" if os.path.exists("porownanie_antena.json") else "../etap3/porownanie_antena.json", encoding="utf-8"))
out["antena"] = {k: {"trafnosc": round(100 * v["trafnosc"], 1), "ece": round(v["ece"], 3), "n": v["n"], "brak": v["n_brak"]} for k, v in A.items()}
# koszt Jev na dobe anteny: decyzja co 3 s, ~626 tokenow wejscia (sredni stan z etapu 3A)
dec = 24 * 3600 / 3; tok = 626
out["jev_doba_anteny"] = {"decyzji": int(dec), "usd": round(dec * tok * 0.042e-6, 2), "pln": round(dec * tok * 0.042e-6 * KURS, 2)}
# Polska: czas treningu na publicznej mocy AI (szacunek ~3000 H100e po uruchomieniu Gaia + PIAST-AI)
H = 3000
out["polska"] = {"llama405_h100_h": 30.84e6, "dni_na_3000": round(30.84e6 / H / 24), "bielik45_gpu_h": 10.6e3, "godz_na_3000": round(10.6e3 / H, 1),
                 "udzial_swiat_proc": round(100 * H / 15e6, 3), "usa_h100e": 0.75 * 15e6, "usa_do_pl": round(0.75 * 15e6 / H),
                 "ioi_zlote_na_10mln": {"PL": round(47 / 36.5 * 10, 1), "KOR": round(49 / 51.7 * 10, 1), "USA": round(68 / 341.9 * 10, 1), "CHN": round(102 / 1405.1 * 10, 2)},
                 "budzet_ai_proc": round(100 * 262 / 918900, 3), "budzet_ai_proc_gg": round(100 * 262 / (517e3 * KURS), 4),
                 "korea_krotnosc": round(0.22 / (100 * 262 / (517e3 * KURS)), 1), "pl_przy_korei_mld_usd": round(0.0022 * 517, 2), "pl_przy_korei_mld_zl": round(0.0022 * 517 * KURS, 1),
                 "ocean_proc_czasu": round(100 * 220 / 280, 1)}
json.dump(out, open("liczby_artykulu.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
