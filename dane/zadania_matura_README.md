# Zestaw testowy: matura 2026 (maj) – zadania zamknięte

Plik danych: `zadania_matura.jsonl` (UTF-8, jeden obiekt JSON w wierszu, 39 pozycji).

Źródła (kopie z arkusze.pl, w `zrodla/`):

| Przedmiot | Arkusz | Zasady oceniania (CKE, publ. 26.06.2026) |
|---|---|---|
| WOS, poziom rozszerzony | `wos-2026-maj-matura-rozszerzona.pdf` – MWHP-R0-100-2605, 12.05.2026 | `wos-2026-maj-matura-rozszerzona-odpowiedzi.pdf` |
| Matematyka, poziom podstawowy | `matematyka-2026-maj-matura-podstawowa.pdf` – MMAP-P0-100-2605, 05.05.2026 | `matematyka-2026-maj-matura-podstawowa-odpowiedzi.pdf` |

`strona_pdf` to numer strony pliku PDF liczony od 1; w obu arkuszach jest równy numerowi „Strona N z …” nadrukowanemu na stronie. `zrodlo_klucza` podaje stronę PDF zasad oceniania (też równą nadrukowanej).

## Liczebność

| Przedmiot | choice (A–D) | pf (P/F) | razem |
|---|---|---|---|
| WOS rozszerzony | 2 | 13 (w tym 5 zadań „Rozstrzygnij”) | 15 |
| Matematyka podstawowa | 20 | 4 | 24 |
| **Razem** | **22** | **17** | **39** |

Rozkład odpowiedzi: pf – 9× true, 8× false (WOS 6/7, matematyka 3/1). Choice: A 3, B 5, C 6, D 8.

Zadania P/F z dwoma stwierdzeniami rozbito na dwie pozycje (`-a` = stwierdzenie górne, `-b` = dolne). W arkuszu 1 pkt dostaje się tylko za oba stwierdzenia naraz.

## Konwencje zapisu

- **WOS:** materiał źródłowy, polecenie, treść i opcje przepisano dosłownie, łącznie z `[…]` i wstawkami w nawiasach kwadratowych. Połamane wiersze scalono w akapity, a podział na akapity lub ustępy zachowano przez `\n`. Przypis w zad. 7 zapisano jako `¹`. Tabelę z zad. 12 zapisano jako wiersze rozdzielone `|` między znacznikami `[TABELA]…[/TABELA]`. Utracono formatowanie: kursywę tytułów, podkreślenia (zad. 13, etykiety „Opis A/B/C:” w zad. 17) i pogrubienie poleceń.
- **Zadania „Rozstrzygnij”** (WOS 2, 7.2, 12.2, 13.2, 17.2) mają typ `pf`: true = „Tak”, false = „Nie”. W `polecenie` jest pełne polecenie, a w `tresc` jego pierwsze zdanie (dosłownie). Uwaga: w arkuszu punkt przyznaje się tylko za rozstrzygnięcie **wraz z uzasadnieniem**. Tu oceniane jest samo rozstrzygnięcie, więc pozycja jest łatwiejsza niż oryginał.
- **Matematyka:** notacja tekstowa: `^` (potęga), `sqrt()`, ułamki `(a)/(b)`, `log_8(4)`, indeksy `a_n`, mnożenie `·`, minus ASCII `-`. Przecinek dziesiętny zostawiono jak w oryginale (`4,9`, `3,5`, `t = 1,5 s`). W parach współrzędnych przecinek ze spacją rozdziela współrzędne, np. `(0, -3)`. Okrąg `𝒪` (litera kaligraficzna) zapisano jako `O`. Wstęp zadania (dane) jest w `material_zrodlowy`, a zdanie do dokończenia w `tresc`.

## Weryfikacja

1. **Treść WOS – automatycznie:** 149 fragmentów (każdy akapit materiału, polecenie, treść, każda opcja, komórki tabeli) po normalizacji białych znaków porównano z warstwą tekstową PDF. Niezgodności: 0. Dodatkowo każdą stronę obejrzano jako obraz.
2. **Treść matematyki – wzrokowo:** warstwa tekstowa PDF gubi wzory, więc każde zadanie porównano z obrazem strony (140 dpi). Dodatkowo sprawdzono automatycznie, że każde polskie słowo (min. 4 litery) z pozycji występuje na odpowiedniej stronie PDF: 0 odstępstw.
3. **Klucz – drugi, niezależny przebieg:** skrypt ponownie odczytał oba PDF zasad oceniania. Dla WOS brał wiersz po „Rozwiązanie” albo „Rozstrzygnięcie: Tak/Nie”. Dla matematyki brał kolumnę „Wersja A” według położenia na stronie. Wynik porównano z polem `poprawna` i numerem strony klucza: **0 rozbieżności na 39**. Układ kolumn Wersja A / Wersja B sprawdzono też na obrazach stron 2, 32 i 38 klucza.

## Wątpliwości (do oceny przed publikacją)

1. **Matematyka – wersja A/B arkusza.** Zasady oceniania dla MMAP-P0-100 podają dwie wersje („A i B”) z innym ustawieniem odpowiedzi. Na pobranym arkuszu nie ma nadruku wersji. Przyjęto **wersję A** z dwóch powodów. Po pierwsze, taką wersję CKE zwykle publikuje. Po drugie, sprawdzono zgodność na zadaniach elementarnych (1, 2, 4, 6, 33.1, 33.2): odpowiedzi z kolumny B wskazywałyby na nich opcje jawnie sprzeczne z treścią. Przykład: w zad. 4 kolumna B wskazuje C = 1, a log_8(4) - log_8(32) = -1. Ten test służył tylko **identyfikacji wersji**. Wszystkie wartości `poprawna` pochodzą z kolumny A klucza. Przy 6 pozycjach (5-a/b, 18, 25-a/b, 26) obie wersje mają tę samą odpowiedź. Warto potwierdzić wersję na oryginale z cke.gov.pl.
2. **Pominięte rysunki (matematyka 18, 19, 20)** – uznano, że tekst zawiera wszystkie potrzebne dane. Odwołanie „(zobacz rysunek)” zostawiono dla wierności oryginałowi. Najsłabszy przypadek to zad. 19: położenie punktu D trzeba wywnioskować z kąta wpisanego. Można go wyłączyć.
3. **WOS 10.3 bez schematu** – polecenie nie odwołuje się do schematu, ale w arkuszu schemat był widoczny i podpowiada odpowiedź (organ wykonawczy wybiera organ stanowiący).
4. **WOS 1.2** – pominięto mapę z materiału zadania 1, bo nie jest potrzebna.
5. **WOS 13.2** – klucz ma osobny wariant (prokuratura) dla arkuszy 200 i Q00. Arkusz 100 dotyczy NIK, a odpowiedź w obu wariantach to „Tak”.
6. Pliki pochodzą z mirrora arkusze.pl (znak wodny na marginesie, metadane autora „arkusze.pl”), a nie wprost z cke.gov.pl.

## Wyłączone zadania

### WOS rozszerzony
| Zadanie | Powód |
|---|---|
| 1.1, 1.3 | otwarte (1.1 wymaga też mapy) |
| 3 | P/F „na podstawie wykresów” – wymaga wykresów |
| 4.1, 5.1, 5.2, 5.3 | otwarte |
| 6 | zamknięte, ale w formacie A/B + 1/2/3 (klucz: A2) – poza przyjętymi typami |
| 7.1, 8.2, 9.2 | otwarte |
| 10.1, 10.2 | uzupełnianie schematu/zdania (otwarte) |
| 11.1, 11.2, 12.3, 13.1, 13.3 | otwarte |
| 14.1, 14.3 | otwarte |
| 14.2 | P/F – organizację trzeba rozpoznać z fotografii |
| 15.1 | otwarte, wymaga mapy |
| 15.2 | P/F „na podstawie danych przedstawionych na mapie” – wymaga mapy |
| 16.1, 16.2 | otwarte |
| 17.1 | przyporządkowanie z wpisywaniem nazw (otwarte) |
| 18 | wypracowanie |

### Matematyka podstawowa
| Zadanie | Powód |
|---|---|
| 7, 21 | dowód (otwarte) |
| 10, 11, 14, 15, 27, 30 | otwarte obliczeniowe |
| 12.1, 12.2 | uzupełnianie zdań (otwarte), oparte na wykresie funkcji |
| 13.1, 13.2 | wymagają wykresu funkcji liniowej (znaki a i b oraz tangens odczytuje się z rysunku) |
| 17, 22 | uzupełnij liczbę (otwarte krótkie) |
| 31 | P/F – dane tylko na dwóch diagramach słupkowych. Dałoby się je dokładnie przepisać jako tabelę, ale wyłączono je zachowawczo (klucz: PP) |
