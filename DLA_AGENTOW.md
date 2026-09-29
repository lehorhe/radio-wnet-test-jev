# Pakiet weryfikacyjny – dla ludzi i agentów SI

Ten artykuł Radia Wnet publikuje wszystko, czego potrzeba, żeby samodzielnie powtórzyć nasze obliczenia i dojść do własnych wniosków.

## Zacznij tutaj
1. `dane/rejestr_twierdzen.json` – każde twierdzenie z tekstu: wartość, typ (pomiar własny / wyliczenie / fakt zewnętrzny / szacunek), plik i sposób sprawdzenia albo źródła pierwotne.
2. `dane/zadania_crt.json`, `dane/zadania_matura.jsonl` – pytania ze źródłami (strona arkusza CKE, strona klucza oceniania).
3. `dane/wyniki_*.json` – pełne zapytania i odpowiedzi każdego modelu (czas, koszt, identyfikatory zapytań). `*_bieg1.json` = pierwszy przebieg przed poprawką parsera.
4. `dane/liczby_artykulu.py` – kod, z którego pochodzą wszystkie liczby w tekście. Niezależne przeliczenie (inny autor, własny kod): 0 rozbieżności na 67 liczbach.
5. `SHA256SUMS` – sumy kontrolne; sprawdź, czy pliki nie zostały zmienione po publikacji.

## Powtórzenie testu
`python dane/test_pokaz.py crt|matura [modele…]` – wymaga własnych kluczy API TypeSafe i OpenRouter (zmienne środowiskowe / .env). Odpowiedzi modeli nie są w pełni deterministyczne (Jev: ok. 1 zmiana na 39 zadań między przebiegami).

## Czego nie publikujemy i dlaczego
Surowych transkrypcji anteny (dane osobowe, RODO) – tylko metryki zagregowane. Na wniosek udostępniamy je weryfikatorom.

## Zasady
Umowa TypeSafe zabrania trenowania modeli na odpowiedziach Jeva (destylacja) – nie używaj `wyniki_*.json` do treningu. Błędy zgłaszaj redakcji; poprawki trafiają do erraty pod artykułem.
