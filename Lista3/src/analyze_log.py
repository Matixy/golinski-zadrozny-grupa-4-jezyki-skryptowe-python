import read_log
from enums.http_log_keys import HTTP_LOG_KEYS

def analyze_log(log: list) -> dict:
  """function which convert http log tuple to http log dict"""
  

def main():
  data: list = read_log.read_log()
  analyzed_log: dict = analyze_log(data)
  
  print(analyzed_log)

if __name__ == "__main__":
  main()