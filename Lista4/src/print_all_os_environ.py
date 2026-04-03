import sys
import os

import utils.dict_tools as dict_tools

def print_environ_dict(dictionary: dict) -> None:
  """"Function which pretty print environ dictionary line after line"""
  for key, value in dictionary.items():
    print(f'{key}: {value}')

def print_sorted_os_environ() -> None:
  sorted_environ_dict: dict = dict_tools.sort_dict(os.environ) # sort os.environ dict by key
  print_environ_dict(sorted_environ_dict)

def print_sorted_filtered_os_environ()-> None:
  filtered_dict: dict = dict_tools.get_filtered_dict(os.environ, sys.argv[1:]) # skip first arg- path running source python file 
  sorted_filtered_dict: dict = dict_tools.sort_dict(filtered_dict) # sort filtered dict
  
  print_environ_dict(sorted_filtered_dict)

def main():
  if len(sys.argv) == 1:
    print_sorted_os_environ()
  else:
    print_sorted_filtered_os_environ()

if __name__ == "__main__":
    main()