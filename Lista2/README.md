# 🚀 Lista 2: "Podstawy Pythona. Praca z funkcjami. Wejście/wyjście standardowe"

---

## 👥 Skład zespołu

 - **Paweł Goliński**  
 - **Mateusz Zadrozny** 



---

## 🎯 Cel projektu
- Zapoznanie z podstawowymi metodami budowania abstrakcji w Python 
- Zapoznanie z przetwarzaniem danych z wejścia standardowego
---

## 🛠️ Funkcjonalności programu
1. ✅ **Przetwarzanie wstępne (Cleaning)**<br>
-- **Automatyczna detekcja preambuły:** Program rozpoznaje początek właściwej treści książki na podstawie analizy pustych wierszy lub znaczników edytorskich. <br>
-- **Usuwanie metadanych wydawniczych:** Skrypt automatycznie ucina informacje o wydaniu (oznaczone symbolem `-----`), zwracając "czysty" tekst literacki. <br>
--**Normalizacja tekstu:** Usuwanie zbędnych spacji wewnątrz linii oraz czyszczenie białych znaków na końcach wierszy przy zachowaniu oryginalnej struktury akapitów. <br>
2. ✅ **Funkcje Wyszukujące** <br>
-- Funkcja wypisująca najdłuższe zdanie w książce (kryterium – liczba znaków)<br>
-- Funkcja wyszukująca najdłuższe zdanie, w którym żadne dwa sąsiadujące słowa nie
zaczynają się na tę samą literę <br>
-- Funkcja wyszukująca pierwsze zdanie, które ma więcej niż jedno zdanie podrzędne (na
podstawie przecinków).<br>
3. ✅ **Funkcje Redukujace**<br>
-- Funkcja zliczająca akapity w tekście (akapit jest oddzielony pustą linią).<br>
-- Funkcja zliczająca wszystkie znaki w tekście, z pominięciem białych znaków. <br>
-- Funkcja licząca procent zdań, które zawierają przynajmniej jedną nazwę własną  <br>
4. ✅ **Funkcje filtrujące**<br>
-- Funkcja wypisująca tylko zdania zawierające co najwyżej 4 wyrazy.<br>
-- Funkcja, która wypisuje na wyjściu tylko zdania, które są pytaniami lub wykrzyknieniami. <br>
-- Funkcja wypisująca pierwszych 20 zdań. <br>
-- Funkcja wypisująca tylko zdania, które zawierają co najmniej dwa wyrazy z następujących: „i”, „oraz”, „ale”, „że”, „lub”.
- ### **Wszystkie te funkcje umożliwiają przesyłanie potokowe danych pomiędzy sobą**

---

## 📂 Struktura projektu
```text
Lista2/
├── data/                          # Pliki wejściowe (teksty książek)
├── docs/                          # Dokumentacja i specyfikacja zadań
├── src/                           # Kod źródłowy aplikacji
│   ├── filterFunctions/           # Funkcje filtrujące
│   ├── reducingFunctions/         # Funkcje redukujące
│   ├── searchingFunctions/        # Funkcje wyszukujące
│   ├── utils/                     # Moduły pomocnicze i obsługa błędów
│   │   ├── errorHandler.py        # Centralna obsługa wyjątków strumieni
│   │   └── textTools.py           # Narzędzia do analizy i czyszczenia tekstu
│   └── readTextFromBook.py        # Ekstrakcja właściwej treści książki
├── tests/                         # Testy
├── README.md                      # Dokumentacja projektu
└── requirements.txt               # Lista bibliotek
```

##  INSTRUKCJA URUCHOMIENIA PROJEKTU
```
1. WYMAGANIA:
   - Zainstalowany Python (zalecana wersja 3.x).
   - Wszystkie skrypty należy uruchamiać z poziomu głównego katalogu projektu (`Lista2`).

2. KROKI INSTALACJI:
   - Sklonuj repozytorium na swój komputer:
     git clone <ADRES_REPOZYTORIUM>

   - Przejdź do folderu projektu:
     cd Lista2

   - Utwórz lokalne środowisko wirtualne:
     python -m venv venv

   - Aktywuj środowisko wirtualne:
     * WINDOWS:       venv\Scripts\activate
     * macOS/Linux:   source venv/bin/activate

   - Zainstaluj wymagane biblioteki (jeśli są obecne):
     pip install -r requirements.txt

3. URUCHOMIENIE PROGRAMU: (cat - Linux/Mac, type - Windows)
   Będąc w głównym folderze "Lista2" wywoujemy np.
   1) cat data/Andersen-brzydkie-kaczatko.txt | python3 src/readTextFromBook.py | python3 -m src.searchingFunctions.findLongestSentence
   2) cat data/Andersen-brzydkie-kaczatko.txt | python3 src/readTextFromBook.py | python3 -m src.searchingFunctions.findFirstSentenceWithMultipleCommas

```


## 📝 Podsumowanie pracy i Podział obowiązków

Poniżej znajduje się zestawienie ról oraz zadań zrealizowanych przez członków zespołu:

| Członek Zespołu | Zakres obowiązków i wykonane zadania                                                                                                                                                                                                                      |
| :--- |:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Paweł Goliński** | Przygotowanie dokumentacji projektu (README)<br>Implementacja głównego programu ekstraktującego tekst `readTextFromBook.py`<br>Implementacja funkcji wyszukujących<br>Przygotowanie plików wejściowych (Książek)<br>Rozwiązanie błędu przerwanego potoków |
| **Mateusz Zadrozny** | Implementacja funkcji redukujących <br> Implementacja funkcji filtrujących <br> Implementacja generatora zdań `generateSentences.py` <br> Implementacja funkcji obsugującej wyjatki podanej w parametrze funkcji `errorHandler.py`                        |

---

### ⚠️ Napotkane problemy
* **Błędy potoków (Broken Pipe):** Napotkano trudności związane z przerwaniami potoków. Rozwiązane poprzez niskopoziomowe przekierowanie wyjścia do os.devnull
* **Przetwarzanie bez list:** Realizacja wymogu nieużywania list przy analizie sąsiedztwa słów wymagała stworzenia algorytmu opartego na flagach stanu.
---

### 🎓 Czego się nauczyliśmy?
Udział w projekcie pozwolił nam na zdobycie praktycznej wiedzy w zakresie:
* **Współpracy zespołowej:** Efektywne wykorzystanie procesów **Pull Request** oraz **Code Review** do wspólnego budowania kodu.
* **Zarządzania projektem:** Obsługa i delegowanie zadań za pomocą narzędzia **GitHub Issues**.
* **Standardów Python:** Tworzenie przejrzystej struktury katalogów i zarządzanie zależnościami.
* **Analizy strumieniowej:** Efektywne wykorzystanie potoków systemowych oraz standardowych strumieni wejścia/wyjścia (stdin/stdout) do procesowania danych „w locie” bez obciążania pamięci RAM.
* **Architektury modułowej:** Tworzenie pakietów w Pythonie oraz zarządzanie ścieżkami wyszukiwania modułów w środowiskach wieloplatformowych.

---
