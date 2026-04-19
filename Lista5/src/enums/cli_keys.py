from enum import Enum

class CLI_KEYS(Enum):
  # ARGPARSE ARGUMENTS NAMES AND HELP INFO VALUES
  POLLUTANT_ARGUMENT: str = "--wielkosc"
  POLLUTANT_ARGUMENT_DESCRIPTION: str = "Mierzona wielkość"
  
  FREQUENCY_ARGUMENT: str = "--czestotliwosc"
  FREQUENCY_ARGUMENT_DESCRIPTION: str = "Częstotliwość pomiarów"
  
  START_DATE_ARGUMENT: str = "--start"
  START_DATE_ARGUMENT_DESCRIPTION: str = "Początek przedziału czasowego (RRRR-MM-DD)"
  
  END_DATE_ARGUMENT: str = "--koniec"
  END_DATE_ARGUMENT_DESCRIPTION: str = "Koniec przedziału czasowego (RRRR-MM-DD)"
  
  SUB_COMMANDS_ARGUMENT: str = "podkomenda"
  SUB_COMMANDS_ARGUMENT_DESCRIPTION: str = "Dostępne operacje podkomend"
  
  RANDOM_STATION_ARGUMENT: str = "losowa_stacja"
  RANDOM_STATION_ARGUMENT_DESCRIPTION: str = "Wypisuje losową stację mierzącą zadaną wielkość"
  
  STATS_ARGUMENT: str = "statystyki"
  STATS_ARGUMENT_DESCRIPTION: str = "Oblicza średnią i odchylenie dla stacji"
  
  STATION_ARGUMENT: str = "--stacja"
  STATION_ARGUMENT_DESCRIPTION: str = "Nazwa stacji"
  
  #ERRORS INFO VALUES
  WRONG_DATE_ERROR: str = "Nieprawidłowy formaty daty. Wymagany: RRRR-MM-DD"
  WRONG_KEYS_ERROR: str = "Nie znaleziono danych dla podanych kluczy"
  WRONG_MEASUREMENT_DATE_ERROR: str = "Brak pomiarów w danym przedziale czsowym"
  NOT_FOUND_STATION_IN_DIR_ERROR: str = "Znaleziono kod stacji, ale brak jej w pliku stacje.csv"
  NOT_FOUND_STATION_NAME_ERROR: str = "Brak nazwy"
  NOT_FOUND_STATION_ADDRESS_ERROR: str = "Brak adresu"
  NO_STATION_VALUES_ERROR: str = "Brak pomiarów dla stacji w danym okresie"
  TO_FEW_VALUES_ERROR: str = "Zbyt mało pomiarów do obliczenia odchylenia"
  
  #REST INFO VALUES
  CHOOSED_RANDOM_STATION_COMMAND_INFO: str = "Wybrano akcje: LOSOWA STACJA"
  CHOOSED_STATS_COMMAND_INFO: str = "Wybrano akcje: STATYSTYKI DLA STACJI"
  CHOOSED_RANDOM_STATION_NAME_INFO: str = "Wylosowana stacja: "
  CHOOSED_RANDOM_STATION_ADDRESS_INFO: str = "Adres wylosowanej stacji: "
  STAT_NUM_OF_MEASUREMENTS: str = "Liczba pomiarów: "
  STAT_STATION_MEAN_INFO: str = "Średnia: "
  STAT_STATION_STD_DEV: str = "Odchylenie standardowe: "

  