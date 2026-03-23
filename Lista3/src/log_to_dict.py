import read_log
from enums.http_log_keys import HTTP_LOG_KEYS
from entry_to_dict import entry_to_dict

def log_to_dict(log: list) -> dict:
  """function which returns dict logs grouped by uid"""  
  log_by_id: dict = {}
  
  for row in log:
    row_dict: dict = entry_to_dict(row)
    uid: str = row_dict[HTTP_LOG_KEYS.UID.value]
    
    # if log in this id is empty create list as value
    if uid not in log_by_id:
      log_by_id[uid] = []
      
    log_by_id[uid].append(row_dict)
    
  
  return log_by_id

def main():
  data: list = read_log.read_log(10)
  log_by_id: dict = log_to_dict(data)
  
  print(log_by_id)

if __name__ == "__main__":
  main()