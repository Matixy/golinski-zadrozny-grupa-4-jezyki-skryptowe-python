import read_log
from get_top_ips import get_top_ips
from get_top_uris import get_top_uris
from count_by_method import count_by_method
from count_status_classes import count_status_classes


FREQUENT_IP_KEY: str = 'freq_ip'
FREQUENT_URI_KEY: str = 'freq_uri'
METHODS_DISTRIBUTION_KEY: str = 'methods_distribution'
ERROR_COUNT_KEY: str = 'error_count'
TOTAL_REQUESTS_KEY: str = 'req_total'
PERCENT_SUCCESSESS_2XX_KEY: str = '2xx_percent_ratio'

def analyze_log(log: list) -> dict:
  """returns raport of log as dict"""
  # if log is empty return {}
  if not log:
    return {}
  
  # most frequent ip
  top_ip: str = get_top_ips(log, 1)
  freq_ip: str = top_ip[0][0] if top_ip else None # get top ip from tuple
  
  # most frequent uri
  top_uri: str = get_top_uris(log, 1)
  freq_uri: str = top_uri[0][0] if top_uri else None # get top uri from tuple
  
  # methods distribution
  methods_distribution: dict = count_by_method(log)
  
  # number of error requests (4xx and 5xx codes)
  status_classes: dict = count_status_classes(log)
  error_count: int = status_classes.get('4xx', 0) + status_classes.get('5xx', 0)
  
  # total requests
  req_total: int = len(log)
  
  # percent of success request (codes 2xx)
  success_count: int = status_classes.get('2xx', 0)
  success_ratio: float = round((success_count / req_total * 100), 2) if req_total > 0 else 0.0 # round succes ratio to .2f format
  
  return prepare_analyze_log_structure(freq_ip=freq_ip, freq_uri=freq_uri, methods_dist=methods_distribution, error_count=error_count, req_total=req_total, succes_2xx_ratio=success_ratio)
  
def prepare_analyze_log_structure(freq_ip: str, freq_uri: str, methods_dist: dict, error_count: int, req_total: int, succes_2xx_ratio: float) -> dict:
  """returns prepared analyzed log dict based on params"""
  return {
    FREQUENT_IP_KEY: freq_ip,
    FREQUENT_URI_KEY: freq_uri,
    METHODS_DISTRIBUTION_KEY: methods_dist,
    ERROR_COUNT_KEY: error_count,
    TOTAL_REQUESTS_KEY: req_total,
    PERCENT_SUCCESSESS_2XX_KEY: succes_2xx_ratio
  }

def main():
  data: list = read_log.read_log()
  analyzed_log: dict = analyze_log(data)
  
  print(analyzed_log)

if __name__ == "__main__":
  main()