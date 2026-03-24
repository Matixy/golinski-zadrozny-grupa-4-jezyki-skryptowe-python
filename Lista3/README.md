# 🚀 Lista 3: "Podstawowe struktury danych Pythona"

---

## 👥 Skład zespołu

- Paweł Goliński
- Mateusz Zadrozny

---

## 🎯 Cel projektu
- Praca na listach, krotkach i słownikach
- Parsowanie nieustrukturalizowanych danych tekstowych
- Filtrowanie, sortowanie i agregacja danych
- Podstawy analizy logów

---

## 🛠️ Funkcjonalności programu
Projekt składa się z zestawu modułów analitycznych, które przetwarzają logi serwera HTTP.

1. ✅ **Wczytywanie i Parsowanie Danych**
  * Dynamiczne wczytywanie ze stdin: Program czyta logi strumieniowo, co pozwala na pracę z plikami o dowolnym rozmiarze bez obciążania pamięci RAM.
  * Konwersja typów: Automatyczna konwersja pól tekstowych na odpowiednie typy danych (np. datetime, int), z obsługą brakujących wartości (-).
2. ✅ **Filtrowanie i Sortowanie**
  * Sortowanie logów po dowolnej kolumnie (np. znaczniku czasu, adresie IP).
  * Filtrowanie wpisów na podstawie kodu statusu HTTP, adresu IP czy rozszerzenia pliku w URI.
3. ✅ **Agregacja i Analiza Danych**
  * Grupowanie po sesji (uid): Tworzenie słownika, w którym kluczami są unikalne identyfikatory sesji, a wartościami listy wszystkich żądań w danej sesji.
  * Statystyki sesji: Obliczanie i wyświetlanie kluczowych metryk dla każdej sesji, takich jak liczba żądań, unikalne adresy IP, czas trwania, rozkład metod HTTP i stosunek udanych zapytań (2xx).
  * Rankingi: Wyszukiwanie "top N" najczęściej występujących adresów IP oraz URI.
  * Analiza kodów HTTP: Grupowanie kodów statusu w klasy (2xx, 3xx, 4xx, 5xx) i zliczanie ich wystąpień.

---

## 📂 Struktura projektu
```text
Lista3/
├── data/                          # Plik wejściowy (http_first_100k.log)
├── docs/                          # Dokumentacja i specyfikacja zadań
├── src/                           # Kod źródłowy aplikacji
│   ├── enums/                     # Enumeracje dla kluczy w słownikach
│   │   ├── http_log_keys.py
│   │   └── session_log_keys.py
│   ├── utils/                     # Moduły pomocnicze
│   │   └── errorHandler.py        # Centralna obsługa wyjątków
│   ├── read_log.py                # Główna funkcja wczytująca logi
│   ├── sort_log.py                # Funkcja sortująca
│   └── ...                        # Inne moduły analityczne
├── README.md                      # Dokumentacja projektu
└── requirements.txt               # Lista bibliotek
```

## INSTRUKCJA URUCHOMIENIA PROJEKTU
```
1. WYMAGANIA:
   - Zainstalowany Python (wersja 3.7+ ze względu na zachowanie kolejności w słownikach).

2. KROKI INSTALACJI:
   - Sklonuj repozytorium na swój komputer:
     git clone <ADRES_REPOZYTORIUM>

   - Przejdź do folderu projektu:
     cd Lista3

   - Utwórz lokalne środowisko wirtualne:
     python -m venv venv

   - Aktywuj środowisko wirtualne:
     * WINDOWS:       venv\Scripts\activate
     * macOS/Linux:   source venv/bin/activate

   - Zainstaluj wymagane biblioteki:
     pip install -r requirements.txt

3. URUCHOMIENIE PROGRAMU (PRZYKŁADY):
   Wszystkie skrypty należy uruchamiać z głównego katalogu projektu (`Lista3`).

   - Zliczanie najczęstszych URI:
     (Windows): data\http_first_100k.log < python src\get_top_uris.py
     (Linux):   data/http_first_100k.log < python src/get_top_uris.py

```

## 📝 Podsumowanie pracy i Podział obowiązków

| Członek Zespołu | Zakres obowiązków i wykonane zadania                                                                                                                                                                                                                      |
| :--- |:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Paweł Goliński** | Przygotowanie struktury katalogów <br> Implementacja funkcji nr. 1-10|
| **Mateusz Zadrozny** | Przygotowanie dokumentacji projektu (README)<br> Implementacja funkcji nr. 11-20 |

---

## ⚠️ Napotkane problemy
* **Złożoność obliczeniowa:** Pierwsze wersje funkcji zliczających (np. get_top_uris) miały złożoność O(N^2) z powodu użycia metody .count() w pętli. Zostało to zoptymalizowane do O(N) poprzez użycie słownika i metody .get().

---

## 🎓 Czego się nauczyliśmy?
* **Efektywne wykorzystanie słowników**, list, krotek i zbiorów do rozwiązywania realnych problemów analitycznych.
* **Złożoność algorytmiczna:** Zrozumienie, jak wybór struktur danych i algorytmów (np. list.count() vs dict.get()) wpływa na wydajność programu przy dużych zbiorach danych.
* **Struktura kodu:** zastosowanie Enumów do eliminacji "magicznych stringów" i lambd do zwięzłego sortowania.