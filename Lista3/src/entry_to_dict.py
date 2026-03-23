import read_log

HTTP_LOG_KEYS = [
  "ts", 
  "uid", 
  "ip",
  "id.orig_p", 
  "id.resp_h", 
  "id.resp_p", 
  "method", 
  "host", 
  "uri", 
  "status_code"
]

def entry_to_dict(entry: tuple) -> dict:
  """function which convert http log tuple to http log dict"""
  if len(entry) != len(HTTP_LOG_KEYS):
    raise f"Błąd: niepopwna długość krotki danych!"
  
  dictionary: dict = {}
  for i in range(len(entry)):
    dictionary[HTTP_LOG_KEYS[i]] = entry[i]
  
  return dictionary

def main():
  data: list = read_log.read_log(1)
  dictionary: list = entry_to_dict(data[0])
  
  print(dictionary)

if __name__ == "__main__":
  main()