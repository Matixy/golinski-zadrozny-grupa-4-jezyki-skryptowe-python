from read_log import read_log
from log_to_dict import log_to_dict 
from count_by_method import count_by_method
from count_status_classes import count_status_classes
from get_top_ips import get_top_ips
from collections import Counter
from enums.http_log_keys import HTTP_LOG_KEYS


def print_dict_entry_dates(log_dict: dict):
  """function which printing data about session"""
  for uid, logs in log_dict.items():
    sorted_logs: list = sorted(logs, key=lambda log: log[HTTP_LOG_KEYS.TS.value]) # logs sorted by timeStamp
    
    # colleting data
    ips: dict = {log[HTTP_LOG_KEYS.ID_ORIG_H.value] for log in sorted_logs} # provides unique ip 
    num_requests: int = len(sorted_logs)
    first_req: float = sorted_logs[0][HTTP_LOG_KEYS.TS.value]
    last_req: float = sorted_logs[-1][HTTP_LOG_KEYS.TS.value]
    
    succes_codes_num: int = 0
    method_counts: dict = {}
    for log in sorted_logs:
      method: str = log[HTTP_LOG_KEYS.METHOD.value]
      method_counts[method] = method_counts.get(method, 0) + 1
      
      if 200 <= log[HTTP_LOG_KEYS.STATUS_CODE.value] < 300:
        succes_codes_num += 1
    
    # creating result to print
    print(f'\n--- session uid: {uid} ---')
    print(f'Hosts: {', '.join(ips)}')
    print(f'request number: {num_requests}')
    print(f'First request: {first_req}')
    print(f'Last request: {last_req}')
    
    for method, count in method_counts.items():
      print(f'{method}: {((count / num_requests) * 100):.2f}%')
      
    print(f'2xx codes ratio: {((succes_codes_num / num_requests) * 100):.2f}%')
      

def main():
  data: list = read_log()
  log_dict: dict = log_to_dict(data)
  
  
  print_dict_entry_dates(log_dict)

if __name__ == "__main__":
  main()