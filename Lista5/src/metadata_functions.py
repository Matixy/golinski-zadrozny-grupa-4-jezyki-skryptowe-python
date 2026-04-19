from enums.metadata_keys import METADATA_KEYS
import csv_parser
import pathlib

import utils.regex_tools as regex_tools

def convert_dates(stations: dict) -> None:
  for station in stations.values():
    station[METADATA_KEYS.START_DATE.value] = regex_tools.format_date(station.get(METADATA_KEYS.START_DATE.value, ""))
    station[METADATA_KEYS.END_DATE.value] = regex_tools.format_date(station.get(METADATA_KEYS.END_DATE.value, ""))

def convert_coordinates(stations: dict) -> None:
  for station in stations.values():
    station[METADATA_KEYS.LONGITUDE.value] = regex_tools.format_coordinate(station.get(METADATA_KEYS.LONGITUDE.value, ""))
    station[METADATA_KEYS.LATITUDE.value] = regex_tools.format_coordinate(station.get(METADATA_KEYS.LATITUDE.value, ""))

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
      if not station[METADATA_KEYS.STATION_TYPE.value] == "mobilna":
        return False
      
  return True

def get_three_part_named_stations(stations: dict) -> list:
  res_stations: dict = {}
  
  for key, station in stations.items():
    station_name_tuple: tuple = regex_tools.has_three_part_name(station.get(METADATA_KEYS.STATION_NAME.value, ""))
    
    if station_name_tuple:
      res_stations[key] = station
      
  return res_stations

def main():
  stations: dict = csv_parser.parse_metadata(pathlib.Path(".\\data\\stacje.csv"))
  convert_dates(stations) # 4a
  convert_coordinates(stations) # 4b
  normalize_station_name(stations) # 4d
  
  for station in stations.values():
    print(station)
    
  # 4c
  two_part_named_stations: dict = get_two_part_name_stations(stations) 
  for station in two_part_named_stations.values():
    print(station)

  print(check_mobile_stations(stations)) # 4e

  # 4f
  three_part_named_cities: list = get_three_part_named_stations(stations)
  for city in three_part_named_cities.values():
    print(city)

if __name__ == "__main__":
  main()