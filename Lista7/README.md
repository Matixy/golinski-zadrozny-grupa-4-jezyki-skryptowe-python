# 🚀 Lista 7: " Elementy programowania funkcyjnego w Python"

---

## 👥 Skład zespołu

- Paweł Goliński
- Mateusz Zadrozny

---

## 🎯 Cel projektu
1. Zapoznanie z elementami programowania funkcyjnego w Python.
2. Zapoznanie z tworzeniem iteratorów i generatorów.
3. Zapoznanie z tworzeniem dekoratorów.


---

## 🛠️ Funkcjonalności programu

---

## 📂 Struktura projektu
```text
Lista5/
├── data/                          # Pliki wejściowe (stacje.csv, measurements/*.csv)
├── docs/                          # Specyfikacja zadań
├── src/                           # Kod źródłowy aplikacji
│   ├── utils/                     # Narzędzia pomocnicze
│   │   └── ...
│   ├── make_generator.py          # generator leniwie zwracający kolejne wartości funkcji f podanej w parametrze
│   ├── ...
├── README.md                      # Dokumentacja projektu
└── requirements.txt               # Lista bibliotek
```

## INSTRUKCJA URUCHOMIENIA PROJEKTU
```Bash
  # 1. Przygotowanie środowiska
  python -m venv venv
  source venv/bin/activate # lub venv\Scripts\activate na Windows

  #DOPISAC PRZYKLADY UZYCIA DLA POSZCZEGOLNYCH ZADAN 
```

## 📝 Podsumowanie pracy i Podział obowiązków
| Członek Zespołu | Zakres obowiązków i wykonane zadania                                                                                                                                                                                                                      |
| :--- |:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Paweł Goliński** | Implementacja funkcji z zadania 1 nie wykorzystując imperatywnych instrukcji for, while, if <br/> Implementacja funkcji wyższego rzędu z zadania 2 przyjmujących predykat pred i iterable (obiekt po którym mona iterować) <br/> Implementacja dekoratora log
| **Mateusz Zadrozny** | Implementacja klasy PasswordGenerator  <br/> Implementacja funkcji make_generator <br/> memoizacja funkcji przy wykorzystaniu napisanej funkcji make_generator_mem

---

## ⚠️ Napotkane problemy

---

## 🎓 Czego się nauczyliśmy?
