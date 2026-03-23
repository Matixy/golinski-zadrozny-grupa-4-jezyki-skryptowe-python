from entry_to_dict import entry_to_dict
from enums.http_log_keys import HTTP_LOG_KEYS

def get_logs_by_ip(log: list)-> dict:
  """returns logs grouped by ip """
  logs_by_ip: dict = {}
  for row in log:
    entry: dict = entry_to_dict(row) # get session dict
    ip: str = entry[HTTP_LOG_KEYS.ID_ORIG_H.value]
    
    if ip not in logs_by_ip:
      logs_by_ip[ip] = []
    
    logs_by_ip[ip].append(entry)
    
  return logs_by_ip