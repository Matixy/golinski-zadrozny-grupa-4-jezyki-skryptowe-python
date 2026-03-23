import read_log
from log_to_dict import log_to_dict
from print_dict_entry_dates import get_dict_entry_dates
from enums.http_log_keys import HTTP_LOG_KEYS


def get_session_paths(log: list) -> dict:
  """returns paths sorted by time of each uid"""
  # empty logs do not have paths
  log_dict: dict = log_to_dict(log)
  
  if not log_dict:
    return {}
  
  session_paths: dict = {}
  for uid, logs in log_dict.items():
    sorted_logs_by_data = sorted(logs, key=lambda log: log[HTTP_LOG_KEYS.TS.value]) # sort logs by time to recreate path
    
    paths: list = [log[HTTP_LOG_KEYS.URI.value] for log in sorted_logs_by_data] # get path from each logs in this uid
    
    session_paths[uid] = paths
  
  return session_paths
  

def main():
  data: list = read_log.read_log()
  session_paths: dict = get_session_paths(data)
  
  print(session_paths)

if __name__ == "__main__":
  main()