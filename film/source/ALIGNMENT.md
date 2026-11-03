# Pochodzenie synchronizacji

1. Oryginalne MP3 zdekodowano lokalnie do mono PCM 16 kHz, bez zmiany tempa.
2. Lokalnie wykonano sherpa-onnx `OfflineRecognizer.from_nemo_ctc`, model `sherpa-onnx-nemo-fast-conformer-ctc-be-de-en-es-fr-hr-it-pl-ru-uk-20k-int8`, z oficjalnego wydania:
   https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-nemo-fast-conformer-ctc-be-de-en-es-fr-hr-it-pl-ru-uk-20k-int8.tar.bz2
3. Surowy wynik: `alignment-raw.json`. Znaczniki czasu dotyczą rzeczywistych akustycznych tokenów CTC, z krokiem 80 ms. Odtworzono cały tekst ze wszystkich tokenów, również samodzielnych spacji. Przedziały słów wyznaczono od pierwszego do ostatniego tokenu słowa (+ jedna ramka modelu na końcu). Nie dzielono czasu fraz równomiernie.
4. Porównano transkrypcję z drugim lokalnym modelem Whisper base z tego samego oficjalnego projektu. Ten eksport Whisper nie dostarczył znaczników słów, więc nie używano jego segmentów do wyznaczania czasu pojedynczych słów.
5. Użytkownik dostarczył oryginalny tekst ElevenLabs. Zastosowano go w całości, wraz z formą „Nowy żel”, pozostawiając akustyczne czasy dopasowanych słów. Finalny tekst: `transcript.txt`.
6. `captions.py` tworzy pozycjonowane zdarzenie podświetlenia dla każdego słowa. Rozdzielczość 80 ms opisuje siatkę modelu, nie gwarantowaną maksymalną niedokładność. Nie jest to wymuszony alignment fonemowy; są to bezpośrednie znaczniki rozpoznawania CTC.

Przetwarzanie audio odbyło się lokalnie. Nie wysłano nagrania do API, nie regenerowano lektora i nie użyto płatnych usług.
