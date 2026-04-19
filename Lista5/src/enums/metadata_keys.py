from enum import Enum

class METADATA_KEYS(Enum):
  ID = "Nr"
  STATION_CODE = "Kod stacji"
  INTERNATIONAL_CODE = "Kod międzynarodowy"
  STATION_NAME = "Nazwa stacji"
  OLD_CODE = "Stary Kod stacji (o ile inny od aktualnego)"
  START_DATE = "Data uruchomienia"
  END_DATE = "Data zamknięcia"
  STATION_TYPE = "Typ stacji"
  AREA_TYPE = "Typ obszaru"
  STATION_KIND = "Rodzaj stacji"
  REGION = "Województwo"
  CITY = "Miejscowość"
  ADDRESS = "Adres"
  LATITUDE = "WGS84 φ N"
  LONGITUDE = "WGS84 λ E"