import read_log
from log_to_dict import log_to_dict
from print_dict_entry_dates import get_dict_entry_dates
from enums.http_log_keys import HTTP_LOG_KEYS


def detect_sus(log: list, threshold) -> list:
  """returns ip with high request frequency in short time"""
  
  

def main():
  data: list = read_log.read_log()
  
  print(detect_sus)

if __name__ == "__main__":
  main()