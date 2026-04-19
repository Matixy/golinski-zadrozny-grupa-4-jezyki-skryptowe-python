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

MEASUREMENTS_DIRECTORY_PATH: Path = pathlib.Path(".\\data\\measurements")
METADATA_DIRECTORY_PATH: Path = pathlib.Path(".\\data\\stacje.csv")

def validate_date_argparse(date: str):
  """"validate date for argparse in format YYYY-MM-DD"""
  
  if regex_tools.validate_date(date):
    return date
  
  raise argparse.ArgumentTypeError(CLI_KEYS.WRONG_DATE_ERROR.value)

def create_argument_parser() -> ArgumentParser:
  """"Creates arguments parser from user input converting and validating given arguments"""
  
  parser: ArgumentParser = argparse.ArgumentParser()
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
  
  return parser

def get_filtered_measurements_by_date(start_date: datetime.datetime, end_date: datetime.datetime, path: Path) -> list:
  measurements: list = csv_parser.parse_measurements(path)
  
  filtered_measurements: list = []
  
  for measure in measurements:
    if start_date <= measure[MEASUREMENTS_KEYS.DATE.value] <= end_date:
      filtered_measurements.append(measure)
      
  return filtered_measurements

def get_random_station(filtered_measurements: list, stations: dict) -> dict:
  unique_sation_codes: list = []
  
  for measurement in filtered_measurements:
    unique_sation_codes.append(measurement[MEASUREMENTS_KEYS.STATION_CODE.value])
    
  random_station_code = random.choice(unique_sation_codes)
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

def get_station_values(station_code: str, measurements: dict) -> list:
  values: list = []
  
  for measurement in measurements:
    if measurement[MEASUREMENTS_KEYS.STATION_CODE.value] == station_code:
      values.append(measurement[MEASUREMENTS_KEYS.VALUE.value])
      
  return values
  
def print_stats_from_station_values(station_code: dict, station_values: list) -> None:
  if len(station_values) == 0:
    print(CLI_KEYS.NO_STATION_VALUES_ERROR.value)
  else:
    print(station_code)
    print(CLI_KEYS.STAT_NUM_OF_MEASUREMENTS.value + str(len(station_values)))
    print(CLI_KEYS.STAT_STATION_MEAN_INFO.value + str(statistics.mean(station_values)))
    
    if len(station_values) > 1:
        print(CLI_KEYS.STAT_STATION_STD_DEV.value + f"{statistics.stdev(station_values):.2f}")
    else:
        print(CLI_KEYS.STAT_STATION_STD_DEV.value + CLI_KEYS.TO_FEW_VALUES_ERROR.value)
  
def main():
  # preparing primary data
  parser: ArgumentParser = create_argument_parser()
  args: Namespace = parser.parse_args()
  choosed_subcommand = getattr(args, CLI_KEYS.SUB_COMMANDS_ARGUMENT.value)
  
  # getting atributes from parser
  pollutant: str = getattr(args, CLI_KEYS.POLLUTANT_ARGUMENT.value.lstrip("-"))
  frequency: str = getattr(args, CLI_KEYS.FREQUENCY_ARGUMENT.value.lstrip("-"))
  start_date_str: str = getattr(args, CLI_KEYS.START_DATE_ARGUMENT.value.lstrip("-"))
  end_date_str: str = getattr(args, CLI_KEYS.END_DATE_ARGUMENT.value.lstrip("-"))
  year: str = start_date_str[:4] # getting year from 0 to 4 index in format YYYY-MM-DD
  
  # convert str dates to datetime
  start_date: datetime = datetime.strptime(start_date_str, "%Y-%m-%d")
  end_date: datetime = datetime.strptime(end_date_str, "%Y-%m-%d")
  
  #searching and loading right measurement file 
  files_by_keys: dict = group_measurement_files_by_key(MEASUREMENTS_DIRECTORY_PATH)
  filter_key: tuple = (year, pollutant, frequency)
  
  # if key not exist in files print error and end programe
  if filter_key not in files_by_keys:
    print(CLI_KEYS.WRONG_KEYS_ERROR.value)
    sys.exit(1)
    
  path_to_measurenents: dict = files_by_keys[filter_key] # get path to filtered measure
  
  # parse searched path
  stations: dict = csv_parser.parse_metadata(METADATA_DIRECTORY_PATH)
  filtered_measurements: list = get_filtered_measurements_by_date(start_date, end_date, path_to_measurenents)
  
  if not filtered_measurements:
    print(CLI_KEYS.WRONG_MEASUREMENT_DATE_ERROR.value)
    sys.exit(0)
  
  
  if choosed_subcommand == CLI_KEYS.RANDOM_STATION_ARGUMENT.value:
    # example of usage py src\cli.py --wielkosc As(PM10) --czestotliwosc 24g --start 2023-01-01 --koniec 2023-01-31 losowa_stacja
    print(CLI_KEYS.CHOOSED_RANDOM_STATION_COMMAND_INFO.value)
    random_station: dict = get_random_station(filtered_measurements, stations)
    print_random_station(random_station)
  elif choosed_subcommand == CLI_KEYS.STATS_ARGUMENT.value:
    # example of usage py src\cli.py --wielkosc As(PM10) --czestotliwosc 24g --start 2023-01-01 --koniec 2023-01-31 statystyki --stacja "SlGodGliniki"
    print(CLI_KEYS.CHOOSED_STATS_COMMAND_INFO.value)
    station_code_from_parser: str = getattr(args, CLI_KEYS.STATION_ARGUMENT.value.lstrip("-"))
    station_values: list = get_station_values(station_code_from_parser, filtered_measurements)
    print_stats_from_station_values(station_code_from_parser, station_values)

if __name__ == "__main__":
  main()