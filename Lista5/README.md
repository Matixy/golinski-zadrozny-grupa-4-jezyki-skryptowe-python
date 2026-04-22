# 🚀 Lista 5: "Wyrażenia regularne, interfejsy linii komend"

---

## 👥 Skład zespołu

- Paweł Goliński
- Mateusz Zadrozny

---

## 🎯 Cel projektu
1. Przetwarzanie wyrażeń regularnych.
2. Zapoznanie z wybranymi modułami biblioteki standardowej Pythona.
3. Tworzenie tekstowych interfejsów użytkownika.


---

## 🛠️ Funkcjonalności programu
1. ✅ Analiza i Parsowanie Danych (CSV & Regex)
  - Metadata Parser: Odczyt danych o stacjach pomiarowych (stacje.csv) i konwersja na słowniki.
  - Measurement Parser: Przetwarzanie plików pomiarowych z uwzględnieniem specyficznego formatu (wiele kolumn stacji, nagłówki techniczne).
  - Grupowanie plików: Automatyczne mapowanie plików w katalogu na podstawie wzorca nazwy <rok>_<wielkość>_<częstotliwość>.csv przy użyciu wyrażeń regularnych.

2. ✅ Przetwarzanie Tekstu i Walidacja (Zadanie 4)
  - Ekstrakcja współrzędnych: Wyciąganie szerokości i długości geograficznej z dokładnością do 6 miejsc po przecinku.
  - Normalizacja nazw: Automatyczna zamiana polskich znaków diakrytycznych oraz zamiana spacji na symbole podkreślenia (_).
  - Analiza adresowa: Wykrywanie lokalizacji wieloczłonowych oraz rozpoznawanie prefiksów ulic (ul.) i alei (al.) w danych tekstowych.
  - Walidacja mobilna: Weryfikacja spójności kodów stacji kończących się na "MOB" z ich typem.

3. ✅ Interfejs Linii Komend (Argparse)
  - Program oferuje dwa główne tryby działania (podkomendy):
  - losowa_stacja: Losuje stację, która w podanym przedziale czasowym prowadziła pomiary danej substancji i wyświetla jej dane adresowe.
  - statystyki: Oblicza średnią oraz odchylenie standardowe (moduł statistics) dla konkretnej stacji w zadanym oknie czasowym.

4. ✅ System Logowania (Zadanie 6 i dodatkowe)
  - DEBUG: Informacje o liczbie przeczytanych bajtów z każdego wiersza danych.
  - INFO: Powiadomienia o otwieraniu i zamykaniu plików.
  - WARNING: Ostrzeżenia o braku danych dla wybranych filtrów lub braku wsparcia stacji dla danego parametru.
  - ERROR/CRITICAL: Obsługa błędów krytycznych (np. brak pliku).
  - Rozdział strumieni: Logi niskiego poziomu trafiają na stdout, natomiast błędy na stderr.

---

## 📂 Struktura projektu
```text
Lista5/
├── data/                          # Pliki wejściowe (stacje.csv, measurements/*.csv)
├── docs/                          # Specyfikacja zadań
├── src/                           # Kod źródłowy aplikacji
│   ├── enums/                     # Klucze i stałe (CLI_KEYS, MEASUREMENTS_KEYS, itp.)
│   ├── utils/                     # Narzędzia pomocnicze
│   │   └── regex_tools.py         # Logika operacji na wyrażeniach regularnych
│   ├── cli.py                     # Główny punkt wejścia aplikacji (Main / Argparse)
│   ├── csv_parser.py              # Logika parsowania plików
│   ├── group_measurement_files.py # Grupowanie plików pomiarowych
├── README.md                      # Dokumentacja projektu
└── requirements.txt               # Lista bibliotek
```

## INSTRUKCJA URUCHOMIENIA PROJEKTU
```Bash
  # 1. Przygotowanie środowiska
  python -m venv venv
  source venv/bin/activate # lub venv\Scripts\activate na Windows

  # 2. Przykłady użycia CLI

  # Losowanie stacji mierzącej As(PM10) w styczniu 2023:
  python src/cli.py --wielkosc "As(PM10)" --czestotliwosc 24g --start 2023-01-01 --koniec 2023-01-31 losowa_stacja

  # Statystyki dla konkretnej stacji (np. SlGodGliniki):
  python src/cli.py --wielkosc "As(PM10)" --czestotliwosc 24g --start 2023-01-01 --koniec 2023-01-31 statystyki --stacja "SlGodGliniki"

  #Warning bo niewystarczajaca liczba danych
  py src\cli.py --wielkosc As(PM10) --czestotliwosc 24g --start 2023-01-01 --koniec 2023-01-01 statystyki --stacja "SlGodGliniki"

  #Error bo błędna wartosc czestotliwosci
  py src\cli.py --wielkosc As(PM10) --czestotliwosc 2g --start 2023-01-01 --koniec 2023-01-31 statystyki --stacja "SlGodGliniki"
  
  #Anomalie
  py src\cli.py --wielkosc As(PM10) --czestotliwosc 24g --start 2023-01-01 --koniec 2023-12-31 anomalie

  # 3. Przykład użycia CLI Typer
  python src/cli_typer.py losowa-stacja --wielkosc PM10 --czestotliwosc 24g --start 2023-01-01 --koniec 2023-01-31

  python src/cli_typer.py statystyki DsJelGorSoko --wielkosc PM10 --czestotliwosc 24g --start 2023-01-01 --koniec 2023-01-31 

  python src/cli_typer.py --help 
```

## 📝 Podsumowanie pracy i Podział obowiązków
| Członek Zespołu | Zakres obowiązków i wykonane zadania                                                                                                                                                                                                                      |
| :--- |:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Paweł Goliński** | Konfiguracja systemu logowania z podziałem na stdout/stderr <br/> Zadania dodatkowe:<Br> Stworzenie Aplikacji Cli z biblioteką Typer <br> Detekcja anomalii w seriach pomiarowych <br> Przygotowanie README
| **Mateusz Zadrozny** | Implementacja parserów CSV  <br/> grupowań Regex <br/> ekstrakcji adresów <br/> Transformacja i walidacja danych  <br/> Przygotowanie szkieletu CLI w argparse.

---

## ⚠️ Napotkane problemy
- Struktura tabel pomiarowych: Pliki CSV z pomiarami nie posiadają standardowej struktury (nagłówki stacji są w poziomych rzędach zamiast kolumn), co wymagało niestandardowego podejścia do modułu csv.
- Złożoność Regex: Opracowanie uniwersalnych wzorców dla współrzędnych geograficznych oraz nazw stacji z myślnikami wymagało obszernego testowania przypadków brzegowych.
- Dopasowanie dat: Filtrowanie pomiarów wymagało precyzyjnego rzutowania typów str na datetime, zwłaszcza przy walidacji końcowej daty przedziału.
---

## 🎓 Czego się nauczyliśmy?
- Tworzenia zaawansowanych wzorców Regex (grupy nazwane, look-ahead).
- Projektowania interfejsów CLI z podkomendami.
- Zarządzania logami w aplikacji wielomodułowej.
- Strukturyzowania niejednorodnych danych pochodzących z instytucji publicznych (GIOŚ).