# QA — Klyde Vrene

## Sprawdzone

- Format: 1080 × 1920, H.264, yuv420p, stałe 30 FPS, 40,00 s. Pełne dekodowanie wszystkich 1200 klatek bez błędów. Brak czarnych klatek.
- Narracja: wyłącznie dostarczone MP3; bez regeneracji, zmiany tempa, wycinania pauz i dodatkowej muzyki. Oryginalne audio trwa 39,967 s; obraz ma 40,00 s. AAC 48 kHz. Pomiar gotowego eksportu: około −16,26 LUFS, true peak −1,45 dBTP, LRA 2,8 LU; bez przesterowania.
- Tekst: wszystkie 88 słów zgodne z oryginalnym skryptem ElevenLabs dostarczonym przez użytkownika. 27 krótkich fraz, maksymalnie dwa wiersze, 88 indywidualnych podświetleń. SRT i JSON dołączone.
- Synchronizacja: lokalne akustyczne znaczniki tokenów CTC, nie równy podział czasu fraz. Drugi lokalny model służył do porównania transkrypcji. Siatka czasowa modelu wynosi 80 ms; nie jest to gwarancja błędu poniżej 80 ms ani ręcznie zatwierdzony alignment każdego fonemu. Szczegóły w `source/ALIGNMENT.md`.
- Układ: napisy zaczynają się na y=1440, drugi wiersz na y=1513; marginesy boczne co najmniej 110 px. Postać, rekwizyty i marka pozostają powyżej napisów. Brak nakładania napisów na twarz. Nie umieszczono CTA ani przycisków w filmie.
- Ruch: stawy rąk i nóg rozwiązywane kinematyką odwrotną, drobne ruchy tułowia i głowy, mruganie, gesty oraz animowane kosmetyki. Quintic easing, przejścia 0,65 s, render z wygładzaniem 2×. Brak długich zatrzymań animacji; spokojna ekspozycja okładki na końcu jest zamierzona.
- Sceny: lustro 0–5,85 s; kosmetyki 5,85–9,40 s; podrażnienie 9,40–14,04 s; redukcja produktów i obserwacja 14,04–23,12 s; podstawy 23,12–28,80 s; etykieta 28,80–36,88 s; okładka 36,88–40,00 s.
- Przegląd wizualny klatek całej osi czasu, co 0,5 s, oraz dokładniejsze kadry gestów i napisów. Wykryty problem zasłaniania głowy przez warstwę symboli został poprawiony. Końcowy eksport ponownie zdekodowano i sprawdzono.
- Źródła: autorska animacja programowa, oryginalne MP3 oraz ta sama okładka wycięta z dostarczonego filmu za zgodą użytkownika. Bez płatnych zasobów, płatnych API i kopiowania klatek animacji z referencji. Dołączono licencję fontu.

## Granice weryfikacji

Kontrola obejmuje analizę techniczną całego pliku i przegląd statycznych klatek; nie wykonano pełnego oglądu z odsłuchem w czasie rzeczywistym ani testu po publikacji w aplikacji TikTok. Nie traktuję tego jako potwierdzonego ludzkim odsłuchem sprawdzenia każdego podświetlenia słowa. Rzeczywisty interfejs TikToka zależy od urządzenia i wersji aplikacji. Okładka pochodzi z klatki wideo, nie z oryginalnego pliku graficznego.

Edytowalne źródła są plikami Python/JSON/ASS; nie jest to projekt After Effects ani CapCut. `qa-metrics.json` zawiera wyniki dla konkretnego końcowego eksportu oraz jego SHA-256.
