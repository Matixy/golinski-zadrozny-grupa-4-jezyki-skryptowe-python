import read_log
from entry_to_dict import entry_to_dict
from enums.http_log_keys import HTTP_LOG_KEYS

def get_extension_stats(log: list) -> dict:
  """returns number of occurrences of each extension in log"""
  extension_stats: dict = {}
  for l in log:
    log_dict: dict = entry_to_dict(l) # convert single log to dictonary
    print(log_dict)
    
    

def main():
  data: list = read_log.read_log()
  for d in data:
    print(d)
  extension_stats: list = get_extension_stats(data)
  
  print(extension_stats)

if __name__ == "__main__":
  main()