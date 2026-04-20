from enums.metadata_keys import METADATA_KEYS
import csv_parser
import pathlib
import re
from re import Match, Pattern
from enums.metadata_keys import METADATA_KEYS
import utils.regex_tools as regex_tools

####### DO USUNIECIA
# def convert_dates(stations: dict) -> None:
#   for station in stations.values():
#     station[METADATA_KEYS.START_DATE.value] = regex_tools.format_date(station.get(METADATA_KEYS.START_DATE.value, ""))
#     station[METADATA_KEYS.END_DATE.value] = regex_tools.format_date(station.get(METADATA_KEYS.END_DATE.value, ""))

def extract_dates_to_dict(stations: dict) -> dict[str, dict[str,str]]:
  result: dict[str, dict[str,str]] = {}
  pattern: Pattern[str] = re.compile(r"^\d{4}-\d{2}-\d{2}$")

  for station_code, station_data in stations.items():
    start_date = station_data.get(METADATA_KEYS.START_DATE.value, "").strip()
    end_date = station_data.get(METADATA_KEYS.END_DATE.value, "").strip()
    
    station_dict = {}
    if pattern.search(start_date):
      station_dict[METADATA_KEYS.START_DATE.value] = start_date 
    
    if pattern.search(end_date):
      station_dict[METADATA_KEYS.END_DATE.value] = end_date

    if station_dict:
      result[station_code] = station_dict
  
  return result

def convert_coordinates(station: dict) -> None:
  station[METADATA_KEYS.LONGITUDE.value] = regex_tools.format_coordinate(station.get(METADATA_KEYS.LONGITUDE.value, ""))
  station[METADATA_KEYS.LATITUDE.value] = regex_tools.format_coordinate(station.get(METADATA_KEYS.LATITUDE.value, ""))

def extract_coordinates(stations: dict) -> dict:
  """"
  Extract and converting cooradinates from stations returns dict with station code as key and dict of coordinates as value
  
  Data format:
  {
    WpOstrowWlkp.25103: {'WGS84 φ N': '-999', 'WGS84 λ E': '-999'}
  }
  """
  
  stations_coordinates: dict = {}
  
  for station in stations.values():
    convert_coordinates(station)
    stations_coordinates[station[METADATA_KEYS.STATION_CODE.value]] = {
      METADATA_KEYS.LONGITUDE.value: station[METADATA_KEYS.LONGITUDE.value],
      METADATA_KEYS.LATITUDE.value: station[METADATA_KEYS.LATITUDE.value]
    }
  
  return stations_coordinates

def get_two_part_name_stations(stations: dict) -> dict:
  res_stations: dict = {}
  
  for key, station in stations.items():
    station_name_tuple: tuple = regex_tools.has_two_part_name(station.get(METADATA_KEYS.STATION_NAME.value, ""))
    
    if station_name_tuple:
      res_stations[key] = station
      
  return res_stations

def normalize_station_name(stations: dict) -> None:
  for station in stations.values():
    station[METADATA_KEYS.STATION_NAME.value] = regex_tools.normalize_str(station.get(METADATA_KEYS.STATION_NAME.value, ""))

def check_mobile_stations(stations: dict) -> bool:
  for station in stations.values():
    station_code: str = station.get(METADATA_KEYS.STATION_CODE.value, "")
    if regex_tools.has_suffix(station_code, "MOB"):
      if not station[METADATA_KEYS.STATION_KIND.value] == "mobilna":
        return False
      
  return True

def get_three_part_named_stations(stations: dict) -> list:
  res_stations: dict = {}
  
  for key, station in stations.items():
    station_name_tuple: tuple = regex_tools.has_three_part_name(station.get(METADATA_KEYS.STATION_NAME.value, ""))
    
    if station_name_tuple:
      res_stations[key] = station
      
  return res_stations

def get_street_or_alley_in_name_stations(stations: dict) -> list:
  res_stations: dict = {}
  
  for key, station in stations.items():    
    if regex_tools.has_street_or_alley_in_name(station.get(METADATA_KEYS.STATION_NAME.value, "")):
      res_stations[key] = station
      
  return res_stations



def main():
  path = pathlib.Path("data") / "stacje.csv"
  stations: dict = csv_parser.parse_metadata(path)
  for station in stations.values():
    print(station)
    break

  # convert_dates(stations) # 4a
  print("\n4a)")
  stations_dates = extract_dates_to_dict(stations) #4a test
  for station_code, station_dates in stations_dates.items():
    print(f"{station_code} -> {station_dates}")
    break

  # 4b
  station_coordinates: dict = extract_coordinates(stations)
  print("\n4b")
  for station_code, coords in station_coordinates.items():
    print(f'{station_code} -> {coords}')
    break
  
  normalize_station_name(stations) # 4d
  
  # 4c
  print("\n4c")
  two_part_named_stations: dict = get_two_part_name_stations(stations) 
  for station in two_part_named_stations.values():
    print(station)
    break

  print("\n4e")
  print(check_mobile_stations(stations)) # 4e False- Nr 48

  # # 4f
  print("\n4f")
  three_part_named_stations: list = get_three_part_named_stations(stations)
  for station in three_part_named_stations.values():
    print(station)
    break
    
  # # 4g
  print("\n4g")
  street_or_alley_stations: list = get_street_or_alley_in_name_stations(stations)
  for station in street_or_alley_stations.values():
    print(station)
    break

if __name__ == "__main__":
  main()