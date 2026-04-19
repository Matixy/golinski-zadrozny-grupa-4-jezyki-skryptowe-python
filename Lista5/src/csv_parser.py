import csv
from csv import DictReader
import pathlib
from pathlib import Path
from datetime import datetime, date
from enums.measurements_keys import MEASUREMENTS_KEYS
from enums.metadata_keys import METADATA_KEYS

METADATA_DELIMITER: str = ","

MEASUREMENTS_DELIMITER: str = ","
MEASUREMENTS_NUM_ROWS_ATTRIBUTES_DATA: int = 6 # provides how many first rows of measurement file is not HOURS but others attributes like freq, station_code, etc.
MEASUREMENTS_STATION_CODES_ROW_NUM: int = 1 # on this row index in csv file is station code
MEASUREMENTS_UNITS_ROW_NUM: int = 4 # on this row index in csv file is unit
MEASUREMENTS_STAND_ID_ROW_NUM: int = 5 # on this row index in csv file is stand id

def parse_metadata(path: Path) -> dict:
  """"
  Reads data from stacje.csv file of each station returns dict where key is STATION_CODE and value is data of station
  
  DATA FORMAT OF EACH STATION:
  {
    "Nr": "1",\n
    "Kod stacji": "DsBialka",\n
    "Kod międzynarodowy": "",\n
    "Nazwa stacji": "Białka",\n
    "Stary Kod stacji (o ile inny od aktualnego)": "",\n
    "Data uruchomienia": "1990-01-03",\n
    "Data zamknięcia": "2005-12-31",\n
    "Typ stacji": "przemysłowa",\n
    "Typ obszaru": "podmiejski",\n
    "Rodzaj stacji": "kontenerowa stacjonarna",\n
    "Województwo": "DOLNOŚLĄSKIE",\n
    "Miejscowość": "Białka",\n
    "Adres": "",\n
    "WGS84 φ N": "51.197783",\n
    "WGS84 λ E": "16.117390"\n
  }
  """
  
  stations_data: dict = {}
  
  with open(path, mode='r', encoding='utf-8-sig') as file: # utf-8-sig- provides BOM (hidden mark at start of file which can do errors)
    reader: DictReader[str] = csv.DictReader(file, delimiter=METADATA_DELIMITER) # dict reader reads first row and do keys based from it for dictionary
    
    for row in reader:
      station_code: str = row.get(METADATA_KEYS.STATION_CODE.value) # get station code from dict
      
      if not station_code:
        continue # skip if station_code is empty
      
      stations_data[station_code] = row # not clearing/converting data because task 4 is for that

  return stations_data

def parse_measurements(path: Path) -> list[dict]:
  """"
    Reads single measurement file, returns list of dicts each dict is one measurment data from specific date
    
    DATA FORMAT OF EACH MEASURE:
    {
      "rok": "2023",\n
      "wielkosc": "BjF(PM10)",\n
      "czestotliwosc": "24g",\n
      "kod_stacji": "DsOsieczow21",\n
      "kod_stanowiska": "DsOsieczow21-BjF(PM10)-24g",\n
      "data": datetime.datetime(2023, 12, 30, 12, 0),\n    
      "wartosc": 0.15\n
    }
    
    returns list of thats measurments
  """
  
  filename: str = path.stem # get filename
  parts: list[str] = filename.split('_') # split filename from '_'
  
  # check if filename is correckt
  if len(parts) != 3:
    return[]

  year, pollutant, frequency = parts # get data from file name

  # read file
  measurements: list = []
  with open(path.resolve(), mode='r', encoding='utf-8-sig') as file: # utf-8-sig- provides BOM (hidden mark at start of file which can do errors)
    reader = csv.reader(file, delimiter=MEASUREMENTS_DELIMITER)

    header_rows = []
    try:
      for i in range(MEASUREMENTS_NUM_ROWS_ATTRIBUTES_DATA):
        header_rows.append(next(reader))
    except StopIteration:
      return[] # worng file return empty list
    
    # getting data from header rows
    STATION_codes: list[str] = header_rows[MEASUREMENTS_STATION_CODES_ROW_NUM][1:] # skip first column- attribute name
    units: list[str] = header_rows[MEASUREMENTS_UNITS_ROW_NUM][1:]
    stand_ids: list[str] = header_rows[MEASUREMENTS_STAND_ID_ROW_NUM][1:]
    
    # reading real data of each row
    for row in reader:
      if not row or not row[0].strip():
        continue # skip empty lines
      
      try:
        date: datetime = datetime.strptime(row[0], "%m/%d/%y %H:%M") # convert str date from csv to datetime
      except ValueError:
        continue # skip if date is wrong
      
      # read data from each cell in current row
      for col_idx, value_str in enumerate(row[1:]): # enumerate provides column indexes
        value_str: str = value_str.strip()
        
        if not value_str:
          continue # if cell is empty skip it
        
        try:
          value: float = float(value_str)
        except ValueError:
          continue # if could not convert value skip this cell
        
        measure: dict = prepare_measurement_dict(year, pollutant, frequency, STATION_codes[col_idx], stand_ids[col_idx], units[col_idx], date, value)
        measurements.append(measure)
        
  return measurements

def prepare_measurement_dict(year: str, pollutant: str, frequency: str, station_code: str, stand_id: str, unit: str, date: datetime, value: float) -> dict:
  """"Returns single formated measurment dict"""
  return {
    MEASUREMENTS_KEYS.YEAR.value: year,
    MEASUREMENTS_KEYS.POLLUTANT.value: pollutant,
    MEASUREMENTS_KEYS.FREQUENCY.value: frequency,
    MEASUREMENTS_KEYS.STATION_CODE.value: station_code,
    MEASUREMENTS_KEYS.STAND_ID.value: stand_id,
    MEASUREMENTS_KEYS.UNIT.value: unit,
    MEASUREMENTS_KEYS.DATE.value: date,
    MEASUREMENTS_KEYS.VALUE.value: value
  }

def main():
  res = parse_measurements(pathlib.Path(".\\data\\measurements\\2023_BkF(PM10)_24g.csv")) # example for test
  for i in res:
    print(i)
    
  # res = parse_metadata(pathlib.Path(".\\data\\stacje.csv")) # example for test
  # for key,val in res.items():
  #   print(f'{key}= {val}')

if __name__ == "__main__":
  main()