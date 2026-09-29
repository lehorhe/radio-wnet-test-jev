# Przyłap nas: test modelu Jev (TypeSafe AI) na maturze 2026, CRT i antenie Radia Wnet

Dane, kod i sumy kontrolne do artykułu Lecha Rusteckiego dla Radia Wnet (wnet.fm), 2 października 2026:
**„Trump przemianował AI na »SI«. My sprawdziliśmy SI, która decyduje, zanim zdążysz mrugnąć”**.

Nie wierz nam na słowo. W tym repozytorium jest każde pytanie, każda odpowiedź każdego modelu (z czasem, kosztem i identyfikatorem zapytania nadanym przez serwer) oraz kod, z którego pochodzą wszystkie liczby w tekście.

| Plik | Co zawiera |
|---|---|
| [`DLA_AGENTOW.md`](DLA_AGENTOW.md) | Instrukcja weryfikacji dla ludzi i agentów SI |
| [`dane/rejestr_twierdzen.json`](dane/rejestr_twierdzen.json) | Każde twierdzenie z tekstu: wartość, typ, sposób sprawdzenia |
| [`dane/zadania_crt.json`](dane/zadania_crt.json), [`dane/zadania_matura.jsonl`](dane/zadania_matura.jsonl) | Pytania ze źródłami (strona arkusza i klucza CKE) |
| [`dane/wyniki_*.json`](dane/) | Pełne zapytania i odpowiedzi modeli |
| [`dane/liczby_artykulu.py`](dane/liczby_artykulu.py) | Kod wszystkich liczb w artykule |
| [`maszynopis.html`](https://lehorhe.github.io/radio-wnet-test-jev/maszynopis.html) | Korekta tekstu przez lokalny model Bielik |
| [`SHA256SUMS`](SHA256SUMS) | Sumy kontrolne plików z dnia publikacji |

## Sprawdź, czy nic nie zmieniliśmy

```bash
git clone https://github.com/lehorhe/radio-wnet-test-jev
cd radio-wnet-test-jev
sha256sum -c SHA256SUMS
```

Historia commitów w tym repozytorium to publiczny zapis każdej zmiany po publikacji. Poprawki trafiają też do erraty pod artykułem.

## Licencje i zastrzeżenia

- **Nasze dane i opisy:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). **Nasz kod:** licencja MIT.
- **Zadania maturalne** pochodzą z arkuszy Centralnej Komisji Egzaminacyjnej (maj 2026). Zawarte w nich fragmenty tekstów, w tym prasowych, przytaczamy w granicach prawa cytatu, wyłącznie po to, by umożliwić sprawdzenie testu. Nie obejmuje ich licencja CC BY.
- **Odpowiedzi modeli** publikujemy jako materiał dziennikarski. Nie używaj ich do trenowania modeli: umowa TypeSafe zabrania destylacji.
- **Nagrania w `audio/`** to fragmenty wyemitowanej anteny Radia Wnet, © Radio Wnet. Nie obejmuje ich licencja CC BY.
- **Zdjęcie w `foto/`:** The White House, domena publiczna (szczegóły w `foto/ATRYBUCJA.md`).

Surowych transkrypcji anteny nie publikujemy (dane osobowe, RODO); w danych są wyłącznie metryki zagregowane.

Testy przygotował i przeprowadził zespół agentów SI pod nadzorem dziennikarza; szczegóły w sekcji „Jak powstał ten tekst” w artykule.

Kontakt: Lech Rustecki, lech@wnet.fm
