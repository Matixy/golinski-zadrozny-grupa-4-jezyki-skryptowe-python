🚀 Lista 3: "Podstawowe struktury danych Pythona"
👥 Skład zespołu
Paweł Goliński
Mateusz Zadrozny
🎯 Cel projektu
Praktyczne wykorzystanie list, krotek i słowników do przetwarzania danych.
Parsowanie i konwersja typów w nieustrukturalizowanych danych tekstowych (logi HTTP).
Implementacja funkcji do filtrowania, sortowania i agregacji dużych zbiorów danych.
Analiza logów sieciowych w celu wyciągnięcia użytecznych statystyk.
🛠️ Funkcjonalności programu
Projekt składa się z zestawu modułów analitycznych, które przetwarzają logi serwera HTTP w formacie Zeek/Bro. Główne funkcjonalności obejmują:
✅ Wczytywanie i Parsowanie Danych
Dynamiczne wczytywanie ze stdin: Program czyta logi strumieniowo, co pozwala na pracę z plikami o dowolnym rozmiarze bez obciążania pamięci RAM.
Konwersja typów: Automatyczna konwersja pól tekstowych na odpowiednie typy danych (np. datetime, int), z obsługą brakujących wartości (-).
Strukturyzacja: Każdy wpis logu jest konwertowany na krotkę, a następnie na słownik, co ułatwia dostęp do danych po nazwie pola.
✅ Filtrowanie i Sortowanie
Sortowanie logów po dowolnej kolumnie (np. znaczniku czasu, adresie IP).
Filtrowanie wpisów na podstawie kodu statusu HTTP, adresu IP czy rozszerzenia pliku w URI.
✅ Agregacja i Analiza Danych
Grupowanie po sesji (uid): Tworzenie słownika, w którym kluczami są unikalne identyfikatory sesji, a wartościami listy wszystkich żądań w danej sesji.
Statystyki sesji: Obliczanie i wyświetlanie kluczowych metryk dla każdej sesji, takich jak liczba żądań, unikalne adresy IP, czas trwania, rozkład metod HTTP i stosunek udanych zapytań (2xx).
Rankingi: Wyszukiwanie "top N" najczęściej występujących adresów IP oraz URI.
Analiza kodów HTTP: Grupowanie kodów statusu w klasy (2xx, 3xx, 4xx, 5xx) i zliczanie ich wystąpień.
📂 Struktura projektu
code
Text
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
│   ├── entry_to_dict.py           # Konwersja krotki na słownik
│   ├── log_to_dict.py             # Grupowanie logów w sesje
│   ├── print_session_stats.py     # Obliczanie i wyświetlanie statystyk sesji
│   └── ...                        # Inne moduły analityczne
├── tests/                         # Testy jednostkowe i integracyjne
│   └── test_log_analysis.py
├── README.md                      # Dokumentacja projektu
└── requirements.txt               # Lista bibliotek
INSTRUKCJA URUCHOMIENIA PROJEKTU
code
Code
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
   Wszystkie skrypty należy uruchamiać z głównego katalogu projektu (`Lista3`), używając potoków.

   - Zliczanie najczęstszych URI:
     (Windows): type data\http_first_100k.log | python -m src.get_top_uris
     (Linux):   cat data/http_first_100k.log | python -m src.get_top_uris

   - Wyświetlanie statystyk sesji:
     (Windows): type data\http_first_100k.log | python -m src.print_session_stats
     (Linux):   cat data/http_first_100k.log | python -m src.print_session_stats
📝 Podsumowanie pracy i Podział obowiązków
Członek Zespołu	Zakres obowiązków i wykonane zadania
Paweł Goliński	Implementacja funkcji do filtrowania logów (po adresie IP, rozszerzeniu, zakresie czasu), analiza błędnych żądań (4xx, 5xx), odtwarzanie ścieżek sesji oraz implementacja zadań analitycznych.
Mateusz Zadrozny	Stworzenie architektury projektu (moduły read_log, entry_to_dict, log_to_dict), implementacja funkcji sortującej, funkcji agregujących (rankingi IP/URI, rozkład kodów, statystyki sesji) oraz przygotowanie testów.
⚠️ Napotkane problemy
Złożoność obliczeniowa: Pierwsze wersje funkcji zliczających (np. get_top_uris) miały złożoność O(N^2) z powodu użycia metody .count() w pętli. Zostało to zoptymalizowane do O(N) poprzez użycie słownika i metody .get() lub collections.Counter.
Obsługa brakujących danych: Pliki logów zawierały myślniki (-) w miejscach, gdzie brakowało danych (np. kodu statusu). Wymagało to dodania warunków w funkcji read_log, aby uniknąć błędów ValueError podczas konwersji na int i nie tracić poprawnych wpisów.
🎓 Czego się nauczyliśmy?
Struktury danych w praktyce: Efektywne wykorzystanie słowników, list, krotek i zbiorów do rozwiązywania realnych problemów analitycznych.
Złożoność algorytmiczna: Zrozumienie, jak wybór struktur danych i algorytmów (np. list.count() vs dict.get()) wpływa na wydajność programu przy dużych zbiorach danych.
Czysty kod: Zastosowanie Enumów do eliminacji "magicznych stringów" i lambd do zwięzłego sortowania.
Testowanie jednostkowe: Tworzenie testów z pytest do weryfikacji poprawności logiki analitycznej.