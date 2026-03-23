import read_log
from utils.get_logs_by_ip import get_logs_by_ip
from enums.http_log_keys import HTTP_LOG_KEYS

DEFAULT_THRESHOLD_NUM_REQ: int = 10
DEFAULT_THRESHOLD_404_ERRORS_NUM: int = 10

def detect_sus(log: list, threshold: int = DEFAULT_THRESHOLD_NUM_REQ) -> list:
  """returns ip with high request frequency and high ammount 404 erros"""
  logs_by_ip: dict = get_logs_by_ip(log) # get logs grouped by ip's
  sus_ips: set = set()
  
  # analyzing logs for each ip
  for ip, logs in logs_by_ip.items():
    # checking number of request 
    if len(logs) > threshold:
      sus_ips.add(ip)
      continue # ip was flagged by sus- other conditions should not be checked
  
    # checking number of 404 errors
    errors_404_sum: int = 0
    for log in logs:
      errors_404_sum += 1 if log[HTTP_LOG_KEYS.STATUS_CODE.value] == 404 else 0

    if errors_404_sum > DEFAULT_THRESHOLD_404_ERRORS_NUM:
      sus_ips.add(ip)

  return sus_ips

def main():
  data: list = read_log.read_log()
  sus_ips: list = detect_sus(data)
  
  print(sus_ips)

if __name__ == "__main__":
  main()