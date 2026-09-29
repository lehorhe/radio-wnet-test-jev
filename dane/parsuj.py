"""Ponowne parsowanie zapisanych odpowiedzi LLM: ostatni poprawny obiekt JSON z polem "odp" (naprawa bledu: LaTeX \frac{..} lapany jako JSON)."""
import json, re, sys


def parsuj(c, typ):
    for m in reversed(re.findall(r"\{[^{}]*\}", c or "")):
        try:
            o = json.loads(m)
        except Exception:
            continue
        if "odp" not in o:
            continue
        odp = o["odp"]
        if typ == "choice" and isinstance(odp, str):
            odp = odp.strip()[:1].upper()
        if typ == "pf" and isinstance(odp, str):
            odp = odp.lower() in ("true", "prawda", "tak", "p")
        return odp, o.get("pewnosc")
    return None, None


if __name__ == "__main__":
    for plik in sys.argv[1:]:
        W = json.load(open(plik, encoding="utf-8")); Z = {z["id"]: z for z in W["zadania"]}; zm = 0
        for w in W["odpowiedzi"]:
            if w["model"].startswith("typesafe"):
                continue
            o, p = parsuj(w.get("surowa"), Z[w["id"]]["typ"])
            if o != w.get("odp"):
                zm += 1; w["odp"], w["pewnosc"] = o, p; w["uwaga_parsera"] = "przeparsowane (ostatni obiekt JSON)"
        W["parser"] = "parsuj.py v2 (ostatni obiekt JSON z polem odp)"
        json.dump(W, open(plik, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(plik, "zmienionych odpowiedzi:", zm)
