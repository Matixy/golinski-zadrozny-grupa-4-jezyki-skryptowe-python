import read_log
from log_to_dict import log_to_dict
from print_dict_entry_dates import get_dict_entry_dates
from enums.session_log_keys import SESSION_LOG_KEYS


def get_most_active_session(sessions_logs: dict) -> str:
  """returns the most active session uid"""
  # empty logs do not have active session
  if not sessions_logs:
    return None
  
  # get session (uid) logs values and return this with highest request number
  most_active_session_stats = max(
        sessions_logs.values(), 
        key=lambda session: session[SESSION_LOG_KEYS.REQUEST_NUMBER.value]
    )
  
  return most_active_session_stats[SESSION_LOG_KEYS.UID.value] # get uid from session which higest request number
  

def main():
  data: list = read_log.read_log()
  log_dict: dict = log_to_dict(data)
  sessions_logs: dict = get_dict_entry_dates(log_dict)
  most_active_session_uid: dict = get_most_active_session(sessions_logs)
  
  print(most_active_session_uid)

if __name__ == "__main__":
  main()