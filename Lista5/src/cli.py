import argparse
from argparse import ArgumentParser, Namespace
import pathlib
from pathlib import Path
from datetime import datetime
import sys
import random
import statistics

import utils.regex_tools as regex_tools
from group_measurement_files_by_key import group_measurement_files_by_key
from enums.cli_keys import CLI_KEYS
import csv_parser
from enums.measurements_keys import MEASUREMENTS_KEYS
from enums.metadata_keys import METADATA_KEYS

from utils.logger_setup import logger
import utils.exceptions

from anomaly_finder import find_anomalies

MEASUREMENTS_DIRECTORY_PATH: Path = pathlib.Path(".\\data\\measurements")
METADATA_DIRECTORY_PATH: Path = pathlib.Path(".\\data\\stacje.csv")

def validate_date_argparse(date: str):
  """"validate date for argparse in format YYYY-MM-DD"""
  
  if regex_tools.validate_date(date):
    return date
  
  raise argparse.ArgumentTypeError(CLI_KEYS.WRONG_DATE_ERROR.value)


class LoggingArgumentParser(argparse.ArgumentParser):
  """Our parser, which saves errors to app.log"""
  
  def error(self, message):
    #przechwytujemy błąd z argparse i wpisujemy go do logera, bez tej klasy argparse sam lapal bledy i nie mozna bylo logowach ich w logach
    logger.error(f"Nieprawidłowe użycie komend (argparse): {message}")
    #wywołujemy oryginalną funkcję error, żeby program zakończył się poprawnie (jak oczekuje CLI)
    super().error(message)


def create_argument_parser() -> ArgumentParser:
  """"Creates arguments parser from user input converting and validating given arguments"""
  
  parser: ArgumentParser = LoggingArgumentParser()
  files_by_key = group_measurement_files_by_key(MEASUREMENTS_DIRECTORY_PATH)
    
  allowed_pollutants = {key[1] for key in files_by_key.keys()} # get pollutants values from measurement keys in filenames, on index 1 is pollutant value
  allowed_frequencies = {key[2] for key in files_by_key.keys()} # get frequencies values from measurement keys in filenames, on index 2 is frequency value
  
  #parse given arguments to argparse object
  parser.add_argument(CLI_KEYS.POLLUTANT_ARGUMENT.value, type=str, required=True, choices=allowed_pollutants, help=CLI_KEYS.POLLUTANT_ARGUMENT_DESCRIPTION.value)
  
  parser.add_argument(CLI_KEYS.FREQUENCY_ARGUMENT.value, type=str, required=True, choices=allowed_frequencies, help=CLI_KEYS.FREQUENCY_ARGUMENT_DESCRIPTION.value)
  
  parser.add_argument(CLI_KEYS.START_DATE_ARGUMENT.value, type=validate_date_argparse, required=True, help=CLI_KEYS.START_DATE_ARGUMENT_DESCRIPTION.value)
  
  parser.add_argument(CLI_KEYS.END_DATE_ARGUMENT.value, type=validate_date_argparse, required=True, help=CLI_KEYS.END_DATE_ARGUMENT_DESCRIPTION.value)
  
  # add subparsers for subcommands
  subparsers = parser.add_subparsers(dest=CLI_KEYS.SUB_COMMANDS_ARGUMENT.value, required=True, help=CLI_KEYS.SUB_COMMANDS_ARGUMENT_DESCRIPTION.value)
  
  # parser for printing random station data subcommand
  parser_random_station: ArgumentParser = subparsers.add_parser(CLI_KEYS.RANDOM_STATION_ARGUMENT.value, help=CLI_KEYS.RANDOM_STATION_ARGUMENT_DESCRIPTION.value)
  
  # parser for stats from specific measure subcommand
  parser_stat: ArgumentParser = subparsers.add_parser(CLI_KEYS.STATS_ARGUMENT.value, help=CLI_KEYS.STATS_ARGUMENT_DESCRIPTION.value)
  
  # this subcommand requires station name
  parser_stat.add_argument(CLI_KEYS.STATION_ARGUMENT.value, type=str, required=True, help=CLI_KEYS.STATION_ARGUMENT_DESCRIPTION.value)
  
  parser_anomalies: ArgumentParser = subparsers.add_parser("anomalie", help="Analizuje dane pod kątem błędów i nietypowych zjawisk") #anomalies parser

  return parser



def get_filtered_measurements_by_date(start_date: datetime.datetime, end_date: datetime.datetime, path: Path) -> list:
  """"Returns this measurements data rows bettwen start and end date"""
  
  measurements: list = csv_parser.parse_measurements(path)
  
  filtered_measurements: list = []
  
  for measure in measurements:
    if start_date <= measure[MEASUREMENTS_KEYS.DATE.value] <= end_date:
      filtered_measurements.append(measure)
      
  return filtered_measurements



def get_random_station(filtered_measurements_by_date: list, stations: dict) -> dict:
  """Returns a random station that has measurements in the filtered dataset"""
  
  station_codes: set = set() # set to give unique stations to provide equal chance of random station
  
  for measurement in filtered_measurements_by_date:
    station_codes.add(measurement[MEASUREMENTS_KEYS.STATION_CODE.value])
    
  random_station_code: str = random.choice(list(station_codes))
  station: dict = stations.get(random_station_code)
  
  return station
    


def print_random_station(station: dict) -> None:
  if station:
    name: str = station.get(METADATA_KEYS.STATION_NAME.value, CLI_KEYS.NOT_FOUND_STATION_NAME_ERROR.value)
    address: str = station.get(METADATA_KEYS.ADDRESS.value, CLI_KEYS.NOT_FOUND_STATION_ADDRESS_ERROR.value)
    print(CLI_KEYS.CHOOSED_RANDOM_STATION_NAME_INFO.value + name)
    print(CLI_KEYS.CHOOSED_RANDOM_STATION_ADDRESS_INFO.value + address)
  else:
    print(CLI_KEYS.NOT_FOUND_STATION_IN_DIR_ERROR.value)
    raise utils.exceptions.StationNotExist(CLI_KEYS.NOT_FOUND_STATION_IN_DIR_ERROR.value)



def get_station_values(station_code: str, filtered_measurements_by_date: dict) -> list:
  values: list = []
  
  for measurement in filtered_measurements_by_date:
    if measurement[MEASUREMENTS_KEYS.STATION_CODE.value] == station_code:
      values.append(measurement[MEASUREMENTS_KEYS.VALUE.value])
      
  return values
  


def print_stats_from_station_values(station_code: dict, station_values: list) -> None:
  if len(station_values) == 0:
    logger.warning(f"{CLI_KEYS.NO_STATION_VALUES_ERROR.value} {station_code}") #6c iii
    #print(CLI_KEYS.NO_STATION_VALUES_ERROR.value)
  else:
    print(station_code)
    print(CLI_KEYS.STAT_NUM_OF_MEASUREMENTS.value + str(len(station_values)))
    print(CLI_KEYS.STAT_STATION_MEAN_INFO.value + str(statistics.mean(station_values)))
    
    if len(station_values) > 1:
      print(CLI_KEYS.STAT_STATION_STD_DEV.value + f"{statistics.stdev(station_values):.2f}")
    else:
      #print(CLI_KEYS.STAT_STATION_STD_DEV.value + CLI_KEYS.TO_FEW_VALUES_ERROR.value)
      logger.warning(f"Zbyt mała liczba danych ({len(station_values)}) dla stacji {station_code}, aby obliczyć odchylenie.")
 


def extract_cli_parameters(args: Namespace) -> dict:
  """Extracts, parse and format arguments from CLI to dict"""
  
  start_date_str: str = getattr(args, CLI_KEYS.START_DATE_ARGUMENT.value.lstrip("-"))
  end_date_str: str = getattr(args, CLI_KEYS.END_DATE_ARGUMENT.value.lstrip("-"))
  
  return {
    "subcommand": getattr(args, CLI_KEYS.SUB_COMMANDS_ARGUMENT.value),
    "pollutant": getattr(args, CLI_KEYS.POLLUTANT_ARGUMENT.value.lstrip("-")),
    "frequency": getattr(args, CLI_KEYS.FREQUENCY_ARGUMENT.value.lstrip("-")),
    "year": start_date_str[:4],
    "start_date": datetime.strptime(start_date_str, "%Y-%m-%d"),
    "end_date": datetime.strptime(end_date_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59) # set end of day to include end date day to
  }



def get_measurement_file_path(year: str, pollutant: str, frequency: str) -> Path | None:
  """"Retruns path to measurements files based on keys if files dont exist return None"""
  files_by_keys: dict = group_measurement_files_by_key(MEASUREMENTS_DIRECTORY_PATH)
  filter_key: tuple = (year, pollutant, frequency)
  
  return files_by_keys.get(filter_key)
  

def print_anomalies_info(anomalies_info_list: list) -> None:
  if not anomalies_info_list:
    print("Nie wykryto żadnych anomalii w wybranym zbiorze danych.")
  else:
    logger.warning(f"Wykryto {len(anomalies_info_list)} anomalii!")
    for anomaly in anomalies_info_list:
      print(f"[!] {anomaly}")


def handle_random_station_command(filtered_measurements_by_date: list, stations: dict) -> None:
  print(CLI_KEYS.CHOOSED_RANDOM_STATION_COMMAND_INFO.value)
  random_station: dict = get_random_station(filtered_measurements_by_date, stations)
  print_random_station(random_station)
  

def handle_stats_command(args: Namespace, filtered_measurements_by_date: list) -> None:
  print(CLI_KEYS.CHOOSED_STATS_COMMAND_INFO.value)
  station_code_from_parser: str = getattr(args, CLI_KEYS.STATION_ARGUMENT.value.lstrip("-")) # get station code from input
  station_values: list = get_station_values(station_code_from_parser, filtered_measurements_by_date)
  print_stats_from_station_values(station_code_from_parser, station_values)


def handle_anomalies_command(filtered_measurements_by_date: list) -> None:
  print("Analiza Anomalii")
  found_anomalies = find_anomalies(filtered_measurements_by_date)
  print_anomalies_info(found_anomalies)


def main():
  logger.info("Uruchomiono program")
  try:
    # preparing primary data
    parser: ArgumentParser = create_argument_parser()
    args: Namespace = parser.parse_args()
    params: dict = extract_cli_parameters(args)
      
    #searching and loading right measurement file 
    path_to_measurements = get_measurement_file_path(params["year"], params["pollutant"], params["frequency"])
    logger.info(f"Parametry wejściowe: Wielkość={params['pollutant']}, Częstotliwość={params['frequency']}, Start={params['start_date'].date()}, Koniec={params['end_date'].date()}, Subkomenda={params['subcommand']}")

    # if files not exist print error and end programe
    if not path_to_measurements:
      #print(CLI_KEYS.WRONG_KEYS_ERROR.value)
      logger.warning(f"Użytkownik podał wielkość ({params['pollutant']}) lub częstotliwość ({params['frequency']}), która nie występuje w bazie danych.")
      raise utils.exceptions.DataNotFoundError(CLI_KEYS.WRONG_KEYS_ERROR.value)
      
      

    # parse and filter data
    stations: dict = csv_parser.parse_metadata(METADATA_DIRECTORY_PATH)
    filtered_measurements_by_date: list = get_filtered_measurements_by_date(params["start_date"], params["end_date"], path_to_measurements) # all subcommands based only on mesaurements bettwen given timestamp
    
    if not filtered_measurements_by_date:
      logger.warning(f"{CLI_KEYS.WRONG_MEASUREMENT_DATE_ERROR.value} (od {params['start_date'].date()} do {params['end_date'].date()})")  #6c ii
      
    
    logger.info(f"Pomyślnie załadowano {len(filtered_measurements_by_date)} pomiarów.")

    # choosing right subcommand
    if params["subcommand"] == CLI_KEYS.RANDOM_STATION_ARGUMENT.value:
      # example of usage py src\cli.py --wielkosc As(PM10) --czestotliwosc 24g --start 2023-01-01 --koniec 2023-01-31 losowa_stacja
      handle_random_station_command(filtered_measurements_by_date, stations)
    elif params["subcommand"] == CLI_KEYS.STATS_ARGUMENT.value:
      # example of usage py src\cli.py --wielkosc As(PM10) --czestotliwosc 24g --start 2023-01-01 --koniec 2023-01-31 statystyki --stacja "SlGodGliniki"
      handle_stats_command(args, filtered_measurements_by_date)
    elif params["subcommand"] == "anomalie":
      # example of usage py src\cli.py --wielkosc As(PM10) --czestotliwosc 24g --start 2023-01-01 --koniec 2023-12-31 anomalie
      handle_anomalies_command(filtered_measurements_by_date)

    logger.info("Program zakończył działanie bez błędów.")

  except utils.exceptions.CliAppError as e:
    logger.error(f"Zatrzymano z powodu błędu aplikacji: {str(e)}")
    #print(f"\n[BŁĄD]: {str(e)}")

  except Exception as e:
    logger.critical(f"Nieoczekiwany błąd: {str(e)}", exc_info=True) #exec_info=True add more data about error 
    #print(f"\n[KRYTYCZNY BŁĄD]: Wystąpił nieoczekiwany problem. Sprawdź plik app.log.")

if __name__ == "__main__":
  main()

