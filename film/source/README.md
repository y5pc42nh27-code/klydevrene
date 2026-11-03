# Klyde Vrene — edytowalne źródła

Autorska proceduralna animacja 1080 × 1920, 30 FPS, 40 s. Nie używa klatek animacji z referencji. Postać: kinematyka odwrotna rąk i nóg, ruch głowy i tułowia, mruganie. Ruch rekwizytów oraz przejścia używają easing quintic.

## Odtworzenie

Wymagania: Python 3, Pillow (oraz NumPy do qa.py), FFmpeg z libx264 i libass, font DejaVu Sans. W tym środowisku font jest w `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`. Po przeniesieniu popraw ścieżkę w `animate.py` i `captions.py`, jeśli to konieczne. `bash build.sh` uruchamia pełny eksport. To edytowalne źródła programowe, nie projekt After Effects.

- `animate.py`: wygląd postaci, gesty, rekwizyty, czasy scen w `SCENES`.
- `words.json`: słowa i rzeczywiste czasy z lokalnego CTC; edycja tekstu nie wymaga ponownego renderu animacji.
- `captions.py`: dwuwierszowe napisy, pozycja, krój i kolor podświetlenia.
- `captions.ass`: pełna ścieżka z podświetlaniem pojedynczych słów.
- `captions.srt`: standardowe napisy; SRT nie obsługuje podświetlania słów.
- `alignment-raw.json`: surowe tokeny i czasy analizy lokalnego modelu NeMo CTC.
- `assets/narration.mp3`: oryginalne dostarczone MP3, bez zmiany tempa i pauz.
- `assets/cover.png`: ta sama okładka wycięta z dostarczonego MP4, za zgodą użytkownika; ograniczona jakością klatki wideo.

Nie dodano muzyki ani efektów z zewnętrznych bibliotek. Głos ma korekcję głośności i ograniczenie szczytów. Animacja i rekwizyty powstały specjalnie dla tego filmu. Font DejaVu: licencja dołączona w `FONT-LICENSE.txt`. Prawa do dostarczonego głosu i okładki pozostają po stronie ich właścicieli.

Synchronizacja jest oparta na akustycznych znacznikach tokenów, z rozdzielczością modelu 80 ms, nie na równym podziale czasu. Drugi model Whisper służył do porównania tekstu, nie dostarczył czasów słów. Szczegóły i pozostałe niepewności są w raporcie QA.

## Iteracja dynamiczna

`source /workspace/klydevrene-env/bin/activate`, następnie z tego katalogu
`bash export-dynamic.sh`. Skrypt eksportuje film, uruchamia QA i kopiuje nowy film
jako `../Klyde-Vrene-dynamiczny.mp4`, bez nadpisania zaakceptowanej bazy.
Nie potrzeba nowych frameworków ani API. Python: Pillow>=11,<13, NumPy>=2,<3.
Zweryfikowano Python 3.12, Pillow 12.3, NumPy 2.5.4 i FFmpeg 7.1 z libx264/libass.
Wymagane fonty DejaVu Sans i DejaVu Sans Bold.

- `animate.py / CAMERA`: ujęcia, centra i skale kamery na osi nagrania; quintic easing.
- `character`, `product_motion`, `shelf`: ekspresja i gesty, wspólna oś ruchu ręki i kosmetyków.
- `captions.py`: 74 px Bold, 30 krótkich fraz, kolor i łagodna skala 106–110%.
- `words.json`: oryginalne, niezmienione akustyczne czasy słów.
- `qa.py`: pełne dekodowanie i bezpieczne marginesy z uwzględnieniem powiększenia słów.
- `../porownanie.html`: lokalne odtworzenie starego i nowego filmu obok siebie.

Napisy pozostają nieruchome względem ekranu; kamera działa wyłącznie na warstwę sceny
(y=180..1325). Sceny są cięte, bez przenikania dwóch postaci. Nie zastosowano motion blur,
muzyki ani efektów audio, aby zachować czystość minimalistycznych konturów i głosu.
