# Klyde Vrene — jedna iteracja dynamiczna

Nowy film: `Klyde-Vrene-dynamiczny.mp4`. Zaakceptowana baza
`Klyde-Vrene-TikTok.mp4` pozostała bez zmian. Odtwarzacze: `porownanie.html`.

| Element | Baza | Nowa iteracja |
|---|---|---|
| Otwarcie | Szerokie lustro, małe ruchy | Reakcja i szybkie zbliżenie, przejazd do odbicia, odsłonięcie sytuacji przed 3 s |
| Kamera | Stała | Reżyserowane centrum i skala 1–2,9×, quintic easing, krótki tłumiony wstrząs przy podrażnieniu |
| Kosmetyki | Równe tempo odkładania | Wspólne czasy ręki i kosmetyku przy 5,85 / 6,90 / 8,00 s; coraz ciaśniejsze kadry |
| Emocje | Drobne ruchy głowy | Pochylenie, brwi, spojrzenia, otwarte usta, cofnięcie przy zaskoczeniu i frustracja |
| Rozwiązanie | Powtarzający się gest | Jeden świadomy wybór, odsunięcie nadmiaru, przejście dłoni do spokojnej obserwacji |
| Przejścia | Przenikanie scen przez 0,65 s | Cięcia na zmianach myśli, ruch wewnątrz ujęć, bez podwójnych postaci |
| Napisy | 52 px regular | 74 px Bold, 30 krótkich fraz, do 2 wierszy; kolor i płynna skala 106%, wybrane słowa 110% |
| Zakończenie | Dostępna okładka | Ta sama okładka, subtelny ruch wejścia, bez CTA, ceny i przycisków |

## Rytm na rzeczywistym nagraniu

- **0–5,85 s — ciekawość:** emocjonalne zbliżenie, dynamiczny przejazd na odbicie,
  szerszy spokojny kadr, powrót do reakcji przy końcu pytania.
- **5,85–14,04 s — problem:** dynamiczne śledzenie produktów, odbicie przy
  „podrażnienie” (10,64 s), emocjonalny najazd na twarz przy „nie wiesz”
  (11,68 s), pytajniki i zatrzymanie kamery, dające czas na odczytanie reakcji.
- **14,04–23,12 s — rozwiązanie:** szersza kompozycja; wybór jednego produktu
  przy „jedną rzecz naraz” (17,52–18,56 s), uspokojenie kamery i obserwacja.
- **23,12–28,80 s — podstawy:** czysty układ trzech stopniowo pojawiających się symboli.
- **28,80–36,88 s — zrozumienie:** świadome oglądanie produktu, spokojny najazd
  na produkt i etykietę przy „wiedzieć, po co używasz”.
- **36,88–40 s — zakończenie:** subtelna ekspozycja zachowanej okładki.

Nie znaleziono oryginału B v02_3 w dostępnych plikach. Użyto istniejącego
`source/assets/cover.png`; nie tworzono zamiennika. Zachowano kolory i konstrukcję postaci.
Nie dodano muzyki, SFX ani motion blur: cienkie kontury i głos pozostają czyste.
Nie użyto nowych frameworków, generowania głosu ani płatnych API.

## Walidacja

- Pełny nowy render i QA: **1200 klatek, 1080 × 1920, H.264/yuv420p,
  30 FPS, 40,00 s**. Zero błędów dekodowania i czarnych klatek.
- 88 słów, oryginalny tekst i czasy; wszystkie przedziały ASS zgodne ze znacznikami
  do zaokrąglenia ASS 10 ms. Bez zmiany tempa lub długości głosu.
- Napisy: sprawdzone granice także po powiększeniu słowa; lewy margines >=110 px,
  prawa krawędź <=900 px, środki wierszy y=1440/1540. Scena kończy się na y=1325.
- Zdekodowane audio nowego filmu ma **identyczny SHA-256 jak audio bazy**:
  `8ec068b8666ed0905bc34929b881df79fa6f9134ae8285ca23090505bfcb2a58`.
  Oryginalny MP3, znaczniki słów, okładka i poprzedni MP4 są identyczne z bazowym HEAD.
- Wyniki: `qa-dynamiczny.json`, `audio-check-dynamiczny.json`.
  `git diff --check` bez błędów.

## Ocena odbioru i jej granice

Wykonano przegląd wizualny 80 klatek co 0,5 s na całej osi, dodatkowo
12 gęstszych próbek otwarcia oraz pełnowymiarowych napisów i kluczowych scen.
Ocena dotyczy kompozycji i sekwencji kadrów; nie wykonano pełnego oglądu z odsłuchem
w czasie rzeczywistym ani badania z widzami na TikToku.

- **Pierwsze 3 s:** twarz i reakcja są większe, potem widoczne odbicie i kontekst.
  Sytuacja jest łatwiejsza do odczytania bez tekstu niż w szerokiej bazie.
- **Cel gestów:** ręka odkłada produkty, wskazuje jeden, a później podtrzymuje produkt
  do obejrzenia. Usunięto cykliczne powtarzanie gestu odsuwania produktów.
- **Kamera:** skupia wzrok na twarzy, odbiciu, dłoni lub produkcie; zatrzymuje się,
  kiedy trzeba odczytać emocję. Największa aktywność występuje przed rozwiązaniem.
- **Napisy:** pogrubienie i większy rozmiar poprawiają czytelność w miniaturze telefonu;
  podświetlenia nie powodują skakania całych linii. Ograniczono szerokość po prawej.
- **Synchronizacja:** zachowano akustyczne czasy CTC o rozdzielczości 80 ms.
  Sprawdzono ich przeniesienie do napisów; nie deklarujemy ponownej ręcznej
  weryfikacji każdego słowa z odsłuchem ani dokładności lepszej od źródłowych danych.
- **Chaos i kontrast:** brak migania, podwójnych postaci i ciągłego drżenia;
  rozwiązanie oraz część edukacyjna mają spokojniejszą kamerę.
- **Zakończenie:** okładka bez dodatkowego hasła sprzedażowego, ceny czy przycisku.

To ocena montażowa na podstawie próbek, nie dowód poprawy retencji.
Rzeczywisty interfejs TikToka zależy od urządzenia; nie wykonano testu po publikacji.

## Pliki i odtworzenie

`source/` zawiera edytowalną animację, kamerę, generator napisów, oryginalne MP3,
czasy i okładkę. `source/export-dynamic.sh` eksportuje, sprawdza i kopiuje nowy film
bez nadpisania bazy. SRT jest statyczny; animacje słów zachowuje ASS i gotowy MP4.
Historyczny pakiet `Klyde-Vrene-komplet.zip` zachowuje także źródła poprzedniej wersji.
Nowy pakiet `Klyde-Vrene-dynamiczny-komplet.zip` zawiera nowy film i źródła,
napisy, raporty, porównanie i bazę do lokalnego odtwarzania.
