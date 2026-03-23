from read_log import read_log
from log_to_dict import log_to_dict 
from enums.http_log_keys import HTTP_LOG_KEYS
from enums.session_log_keys import SESSION_LOG_KEYS

def get_dict_entry_dates(log_dict: dict) -> dict:
  """function returns data about session"""
  sessions_data: dict = {}
  
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
    
    # countg methods ratio
    method_ratio: dict = {}
    for method, count in method_counts.items():
      method_ratio[method] = (count / num_requests) * 100
      
    # adding session to res dict
    sessions_data[uid] = prepare_session_data(uid, ips, num_requests, first_req, last_req, method_ratio, (succes_codes_num / num_requests) * 100)
    
  return sessions_data

def prepare_session_data(uid: str, ips: set, num_requests: int, first_req: float, last_req: float, method_ratio: float, succes_method_ratio: float) -> dict:
  return {
      SESSION_LOG_KEYS.UID.value: uid,
      SESSION_LOG_KEYS.HOSTS.value: ips,
      SESSION_LOG_KEYS.REQUEST_NUMBER.value: num_requests,
      SESSION_LOG_KEYS.REQUEST_FIRST.value: first_req,
      SESSION_LOG_KEYS.REQUEST_LAST.value: last_req,
      SESSION_LOG_KEYS.METHODS_RATIO.value: method_ratio,
      SESSION_LOG_KEYS.SUCCES_METHODS_RATIO.value: succes_method_ratio
      }

def print_dict_entry_dates(log_dict: dict):
  """function which printing data about session"""
  session_logs: dict = get_dict_entry_dates(log_dict)
  
  for uid, logs_data in session_logs.items():
    # creating result to print
    print(f'\n--- session uid: {uid} ---')
    print(f'Hosts: {', '.join(logs_data[SESSION_LOG_KEYS.HOSTS.value])}')
    print(f'request number: {logs_data[SESSION_LOG_KEYS.REQUEST_NUMBER.value]}')
    print(f'First request: {logs_data[SESSION_LOG_KEYS.REQUEST_FIRST.value]}')
    print(f'Last request: {logs_data[SESSION_LOG_KEYS.REQUEST_LAST.value]}')
    
    for method, ratio in logs_data[SESSION_LOG_KEYS.METHODS_RATIO.value].items():
      print(f'{method}: {ratio:.2f}%')
      
    print(f'2xx codes ratio: {logs_data[SESSION_LOG_KEYS.SUCCES_METHODS_RATIO.value]:.2f}%')
      

def main():
  data: list = read_log()
  log_dict: dict = log_to_dict(data)
  
  
  print_dict_entry_dates(log_dict)

if __name__ == "__main__":
  main()