# Ocena doboru modeli i parametrów – artykuł „Trump przemianował AI na SI…” (28.09.2026)

Kryteria: trafność wyniku (ile uwag/ustaleń okazało się prawdziwych po mojej kontroli), koszt, obciążenie limitu Claude Code (tydzień 84→85%, 5 h 89→94%).

| Rola | Model / parametry | Koszt | Wynik po kontroli | Ocena doboru |
|---|---|---|---|---|
| Hajduk – fact-check | Gemini 3.8 Flash, T=0, wtyczka web (OpenRouter) | 0,08 USD (2 biegi, 1× błąd 502) | 5 trafnych poprawek (Altman/Friar, 262 mln zł, „5 z 7”, deklaracje producenta, precyzja „komunikatu”); 1 częściowo błędna („brak komunikatu” – komunikat istnieje); cytował strony główne zamiast artykułów | **Dobry** kosztowo. T=0 właściwe. Do finalnej rundy przed publikacją: silniejszy model z wyszukiwaniem na 5 kluczowych twierdzeniach |
| Cichoń + Wierzba – prawo | Gemini 3.8 Flash, T=0, **bez web i bez tekstu umowy** | 0,02 USD | 3 trafne (RODO – zdanie o maskowaniu, zastrzeżenie przy zdjęciu, odpowiedzialność redakcyjna); **2 halucynacje**: zmyślona nazwa paragrafu MCA, uznanie przemówienia Trumpa za fikcję | **Zły dobór konfiguracji** (nie modelu): ocena prawna bez dokumentów źródłowych. Następnym razem: tekst MCA + web w kontekście |
| Gawlik + Marczewska – redakcja | GPT-5.4 mini, T=0,4 | 0,014 USD | Większość uwag językowych trafna (lead 3 zdania, „Dla Polaków”, kalka „typowana decyzja”, „Financial Times”); 1 chybiona (podważanie nazw modeli – luka wiedzy modelu) | **Dobry**. T=0,4 dało naturalne propozycje brzmienia bez zmyślania |
| Motyka – liczby | GPT-5.4 mini, T=0,2 | 0,015 USD | 3 „krytyczne” uwagi **fałszywe** (pomylił CRT z maturą; błędny rachunek 2,66 zł zamiast 2,80 zł); trafne tylko doprecyzowania jednostek | **Zły dobór modelu**: kontrola rachunków bez wykonywania kodu to zadanie dla modelu z narzędziem obliczeń. Sobczuk (niżej) zrobił to dobrze |
| Sobczuk – ślepe przeliczenie | Claude **Haiku 4.5** (subagent, własny kod, bez dostępu do moich skryptów) | ~91 tys. tokenów planu | 67 liczb, 0 rozbieżności, poprawne rozpoznanie zaokrągleń | **Bardzo dobry**: najtańszy model + wykonywanie kodu = wiarygodność |
| Budowa zbioru maturalnego | subagent general-purpose (model domyślny = Opus) | ~252 tys. tokenów planu | 39 pozycji, 0 rozbieżności z kluczem CKE w drugim przebiegu | **Za drogo dla limitu**: jakość potrzebna, ale Sonnet z tą samą procedurą weryfikacji by wystarczył |
| 3× research (media PL, IPO, moc/PKB) | subagenci general-purpose (Opus) | ~100–170 tys. tokenów planu każdy | Wysoka jakość, jawne rozróżnienie fakt/pogłoska; 1 liczba „z pamięci” (Llama) – potwierdzona | **Za drogo dla limitu**: Sonnet do researchu webowego, Opus tylko do syntezy |
| Benchmark modeli (CRT, matura) | temperatura **nieustawiona** (domyślna dostawców) | 0,55 USD | Wyniki stabilne, ale | **Błąd metodologiczny**: w benchmarku trzeba było ustawić T=0 dla powtarzalności; do odnotowania w „Przyłap nas” |
| Lokalna Gemma 4 26B (ZBook) | `reasoning_effort: none` | 0 | 80,9% na antenie; bez wyłączenia rozumowania 34–100 s/okno | **Dobry** po korekcie; VLM nie ruszył (brak mmproj w LM Studio) |

## Wnioski na przyszłość (standard)
1. **Weryfikacja = inny dostawca + dokumenty źródłowe w kontekście.** Model bez źródeł „dopowiada” (MCA, Trump).
2. **Liczby sprawdza tylko model wykonujący kod** – najtańszy wystarczy (Haiku). Model „liczący w głowie” generuje fałszywe alarmy.
3. **Temperatura:** 0 dla ocen i benchmarku, 0,3–0,5 dla propozycji redakcyjnych.
4. **Limit Claude:** research i ekstrakcja → Sonnet/Haiku; Opus tylko do syntezy i decyzji. W tej sesji ~5 subagentów na Opusie to główna przyczyna zużycia 5-godzinnego okna.
5. **Każdy recenzent sam bywa recenzowany**: ok. 7 z 32 uwag zespołów odrzuciłem jako błędne lub chybione – ten odsetek (~22%) warto raportować w ramce „Jak powstał ten tekst”.

## Dopisek (29.09): Bielik 11B v3 jako korektor
| Rola | Model / parametry | Koszt | Wynik po kontroli | Ocena doboru |
|---|---|---|---|---|
| Redakcja i korekta językowa | Bielik 11B v3.0 Instruct **Q8_0**, lokalnie (ZBook, LM Studio), T=0,1, akapit po akapicie | 0 zł, 70 min (6,4 tok/s) | 125 propozycji: **9 przyjętych (7%)**; 25 psuje polską typografię („…” → "…", – → -) mimo polecenia; 15 zmienia fakt/liczbę; 14 odrzuconych automatycznie (fragment nie istnieje) | **Model dobry jako „ołówek”** (wskazuje miejsca), **zły jako „pióro”** (poprawki). Q8 za wolne – do tej pracy Q4/Q5 (2–3× szybciej). Lepszy prompt: tylko wskazanie + kategoria, bez przepisywania; typografię sprawdzać deterministycznie (regex), nie modelem. Błąd mój: skrypt nie pokazywał postępu na bieżąco |

## Dopisek: pozostałe etapy (ścieżki pomiarowe)
| Etap | Model / parametry | Koszt | Wynik | Ocena doboru |
|---|---|---|---|---|
| Decyzje na antenie (346 okien) | **Jev 1.13**, kategorie z opisami + tagi audio, 6 wątków, keep-alive | ok. 0,03 USD / 346 decyzji | 82,4%, ECE 0,070, p50 0,28 s | **Trafny**: najlepsza kalibracja i najniższy koszt; opisy kategorii = +25 pp (bez nich 53%) |
| To samo – linie odniesienia | GPT-5.4 mini, Haiku 4.5, DeepSeek v4 Flash (T=0) | 0,60 / 1,01 / 0,13 USD za 1000 | 80,9 / 78,9 / 84,2% (DeepSeek: 35 braków → realnie 75,7%) | Właściwy zestaw porównawczy; DeepSeek nieprzydatny do czasu rzeczywistego (p95 17 s) |
| To samo – lokalnie | **Gemma 4 26B MoE** (Q4), `reasoning_effort: none`, T=0 | 0 zł | 80,9%, ECE 0,136, p50 16 s pod obciążeniem ZBooka | **Dobry jako zapasowy offline**, zły do czasu rzeczywistego przy równoległym obciążeniu; bez wyłączenia rozumowania 34–100 s |
| Reguły lokalne | regex + tagi SMD | 0 | 53,2% | Potrzebne tylko jako dolna granica – spełniły rolę |
| Test Refleksji Poznawczej, matura | Jev vs Opus 5.5, **GPT-6 Astra**, Gemini 3.8 Flash, Haiku 4.5, GPT-5.4 mini | 0,62 USD łącznie | Astra 17/17 i 39/39, 2,4–2,5 s, ale najdroższa (61 gr/arkusz); ~~402 przy 4 wątkach~~ → sekwencyjnie z `max_tokens` 3–4 tys. | Zestaw trafny (3 czołowe + 2 tanie). Błąd: **brak T=0**, oraz Astra na 4 wątkach wyczerpała limit „w locie” OpenRouter |
| Percepcja kadrów | EasyOCR + **Florence-2-large** fp16 na GTX 1660 (1,9 GB VRAM) | 0 | OCR podpisu gościa 100%; ~8 s/kadr (beam 3) | **Dobry wybór pod 6 GB**; do wideo na żywo zmniejszyć `num_beams` do 1 (≈3× szybciej). Gemma-VLM nie ruszyła (LM Studio bez mmproj) |
| Kadry – ścieżka chmurowa | **jev-router** (OpenRouter) z surowym obrazem | 0,05 USD / 30 kadrów | 67% rodzaju kadru, 5 s, 3 braki; kierował do DeepSeek v4.1 Flash | Słusznie tylko jako punkt odniesienia – nie do produkcji |
| ASR klipów | faster-whisper **large-v3-turbo** int8_float16, GTX 1660 | 0 | 11× szybciej niż czas rzeczywisty; posłużył też do weryfikacji 4 klipów cytatów | **Trafny** |
| Własny klasyfikator audio (Etap 6) | **EfficientAT mn04_as** zamrożony (CPU, niski priorytet) + regresja logistyczna, podział grupowy | 0; 19 min cech na CPU ZBooka | 72% (reklamy 80% na niewidzianych spotach), ECE 0,21 | **Trafny jako baza** (tani, nie zabiera GPU produkcji). Słaba kalibracja → dodać kalibrację (Platta/izotoniczną) i cechy tekstowe; większy model audio (BEATs) dopiero przy GPU |
| Wyszukiwanie cytatów w korpusie | Szpieg+ FTS5 + semantyczne (MiniLM, :8799) | 0 | FTS: 17 trafień (odmiana!), semantyka: trafne rozmowy (Bartosiak, Grzywaczewski) | **Semantyka konieczna** dla polskiej fleksji; FTS tylko jako uzupełnienie |

## Budżety – podsumowanie (stan 29.09.2026, 01:15)
| Budżet | Limit / plan | Zużycie | Uwagi |
|---|---|---|---|
| **Claude Code – tydzień (wszystkie modele)** | 100% planu Team, reset 30.09 ok. 05:59 | **84% → 88%** w tej serii prac (+4 pp; od startu sesji dużo więcej – sesja trwała od 28.09 ~19:00) | Główne zużycie: ~5 subagentów na domyślnym Opusie (research, zbiór maturalny). Zostaje ~12% na 1 dzień 4 h – wystarczy na wysyłkę szkicu (kilka poleceń, bez subagentów) |
| Claude Code – okno 5 h | reset co 5 h | szczyt **94%** (28.09 ~20:40), teraz 14% | Po osiągnięciu szczytu praca przeniesiona na OpenRouter i skrypty |
| OpenRouter – seria testów | ≤ 5 USD (handoff) | **1,74 USD** (w tym 0,37 z ZBooka) | Saldo konta po doładowaniu: 13,83 USD |
| Jev (TypeSafe) | ≤ 2 mln tokenów wejścia | **1,60 mln** (2075 wywołań) ≈ 0,07 USD | Zostaje 0,4 mln – na dalsze testy tylko wybiórczo |
| ElevenLabs | – | 0 | Nie używany (cytaty z oryginalnego audio anteny) |
| Lokalne (ZBook, CN) | prąd | Bielik 70 min, Gemma ~1,5 h, EfficientAT 19 min CPU, Whisper/Florence minuty | Bez kosztu tokenów |

**Wniosek budżetowy:** wysyłka szkicu na wnet.fm to ~6 zapytań REST (5 plików + wzorzec + wpis) i 1–2 kroki moje – szacunkowo <1 pp tygodniowego limitu, 0 USD API.
