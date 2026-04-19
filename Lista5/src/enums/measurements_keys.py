from enum import Enum

class MEASUREMENTS_KEYS(Enum):
  # data form file name
  YEAR: str = "rok"
  POLLUTANT: str = "wielkość"
  FREQUENCY: str = "częstotliwość"
  
  # from file headers
  STATION_CODE: str = "kod_stacji"
  STAND_ID: str = "kod_stanowiska"
  UNIT: str = "jednostka"
  
  # from data
  DATE: str = "data"
  VALUE: str = "wartość"