# 🚀 Lista 4: "Środowisko systemowe, CLI i automatyzacja procesów"

---

## 👥 Skład zespołu

- Paweł Goliński
- Mateusz Zadrozny

---

## 🎯 Cel projektu
- Zarządzanie zmiennymi środowiskowymi systemu operacyjnego.
- Tworzenie interfejsów linii komend (CLI).
- Przetwarzanie plików w formatach strukturalnych (CSV, JSON).
- Automatyzacja zadań systemowych i komunikacja międzyprocesowa (moduł subprocess).
- Integracja zewnętrznych narzędzi CLI (FFmpeg).

---

## 🛠️ Funkcjonalności programu
Projekt obejmuje zestaw narzędzi do manipulacji systemem plików i danymi środowiskowymi.

1. ✅ **Zarządzanie Środowiskiem**
  * **Filtrowanie zmiennych**: Skrypt wyświetlający zmienne środowiskowe z opcją nieczułego na wielkość liter (case-insensitive) filtrowania nazw.
  * **Analizator PATH**: Narzędzie do parsowania zmiennej systemowej PATH, listujące katalogi oraz znajdujące się w nich pliki wykonywalne (obsługa rozszerzeń .exe, .bat dla Windows oraz flagi X_OK dla systemów Unix).
2. ✅ **Przetwarzanie Strumieni i Plików**
  * **Własny tail**: Uproszczona wersja narzędzia systemowego obsługująca parametr --lines oraz tryb --follow (śledzenie zmian w pliku w czasie rzeczywistym).
  * **Obsługa potoków**: Możliwość czytania danych zarówno z plików, jak i bezpośrednio z wejścia standardowego (sys.stdin).
3. ✅ **Analiza Statystyczna i Subprocesy**
  * **Statystyki Tekstu**: Program obliczający metryki pliku (liczba znaków, słów, wierszy, najczęstszy znak i słowo).
  * **Automatyzacja zbiorcza**: Skrypt typu "wrapper", który rekurencyjnie przeszukuje katalogi i uruchamia analizator dla każdego pliku przy pomocy subprocess, agregując wyniki końcowe.
4. ✅ **Konwersja Multimedialna i Przetwarzanie Obrazów**
  * **Automatyczne wykrywanie typu**: Skrypt samodzielnie rozpoznaje typ pliku (audio/wideo vs. obraz) i dobiera odpowiednie narzędzie: FFmpeg dla multimediów lub ImageMagick (magick) dla grafiki.
  * **Obsługa parametrów zewnętrznych**: Program pozwala na przekazywanie niestandardowych flag i argumentów bezpośrednio do procesów ffmpeg lub magick, co umożliwia np. zmianę bitrate'u, nakładanie filtrów czy zmianę rozmiaru obrazu.
  * **Konfiguracja ENV**: Pełna kontrola nad folderem wyjściowym poprzez zmienną CONVERTED_DIR oraz logowanie szczegółów technicznych (użyty program, parametry) w historii konwersji.


---

## 📂 Struktura projektu
```text
Lista4/
├── data/                          # Pliki wejściowe
├── docs/                          # Dokumentacja i specyfikacja zadań
├── src/                           # Kod źródłowy aplikacji
│   ├── java/                      # Program do analizy statystycznej pliku (Zadanie 4a-c)
│   ├── utils/                     # Moduły pomocnicze (np. error_handler_, dict_tools)
│   ├── analyzer_runner.py         # Zadanie 4d: Wrapper uruchamiający analizator Java przez subprocess
│   ├── mediaconvert.py            # Zadanie 5: Konwerter multimediów (FFmpeg/Magick)
│   ├── pathOperator.py            # Zadanie 2: Zarządzanie i analiza zmiennej PATH
│   ├── print_all_os_environ.py    # Zadanie 1: Wyświetlanie i filtrowanie zmiennych środowiskowych
│   └── tail.py                    # Zadanie 3: Implementacja narzędzia tail
├── README.md                      # Dokumentacja projektu
└── requirements.txt               # Lista bibliotek
```

## INSTRUKCJA URUCHOMIENIA PROJEKTU
```
1. WYMAGANIA SYSTEMOWE:
   - Python 3.8+
   - Narzędzie systemowe FFmpeg lub Magick (wymagane do Zadania 5)

2. KONFIGURACJA:
   - Sklonuj repozytorium i przejdź do folderu:
     cd Lista4
   - Utwórz i aktywuj środowisko wirtualne:
     python -m venv venv
     source venv/bin/activate  # Linux/macOS
     venv\Scripts\activate     # Windows

3. PRZYKŁADY URUCHOMIENIA:
   - Zadanie 1 (Filtrowanie zmiennych):
     python src/print_all_os_environ PATH USER

   - Zadanie 2 (Wyswietlanie folderow/plikow z PATH):
     python src/pathOperator --folders
     python src/pathOperator --all

   - Zadanie 3 (Tail):
     cat data/long.txt | python src/tail.py --lines 5

   - Zadanie 4:
     python src/analyzer_runner.py data

textAnalyzer % java -jar target/textAnalyzer-1.0-SNAPSHOT-jar-with-dependencies.jar
/Users/pawel/Studia/SEM4/Jezyki Skryptowe/Jezyk-Skryptowe/Lista4/data/Andersen-brzydkie-kaczatko.txt

   - Zadanie 5 (Konwersja):
     set CONVERTED_DIR=./output  # Windows
     python src/mediaconvert.py data webm

   - Zadanie 5 (Konwersja obrazu z parametrami ImageMagick):
     python src/mediaconvert.py data png -colorspace Gray

```

## 📝 Podsumowanie pracy i Podział obowiązków

| Członek Zespołu | Zakres obowiązków i wykonane zadania                                                                                                                                                                                                                      |
| :--- |:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Paweł Goliński** | Zadanie 2: Analiza zmiennej PATH i wykrywanie plików wykonywalnych. <br> Zadanie 4d: Skrypt integrujący analizator przy użyciu subprocess. <br>  Zadanie 5: Skrypt mediaconvert.py z obsługą FFmpeg, ImageMagick oraz przekazywaniem parametrów linii komend do procesów zewnętrznych.
| **Mateusz Zadrozny** | Zadanie 1: Lista i filtracja zmiennych środowiskowych. <br> Zadanie 3: Implementacja programu tail (w tym --follow). <br> Zadanie 4a-c: Implementacja statystycznego analizatora tekstu (CSV/JSON).

---

## ⚠️ Napotkane problemy
* Wykrywanie plików wykonywalnych wymagało osobnej logiki dla systemów Windows (sprawdzanie rozszerzeń) i Unix (sprawdzanie bitu wykonywalności os.X_OK).
* Buforowanie wyjścia: Podczas implementacji tail --follow oraz subprocess, standardowy bufor Pythona opóźniał wyświetlanie linii. Rozwiązano to za pomocą wymuszenia opróżniania bufora (sys.stdout.flush()).

---

## 🎓 Czego się nauczyliśmy?
* Praca z systemową ścieżką PATH
* Czytanie parametrów z lini komend
* Automatyzacja procesów: Integracja wielu zewnętrznych narzędzi (FFmpeg i ImageMagick) w ramach jednej spójnej logiki biznesowej.
