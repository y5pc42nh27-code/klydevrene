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
