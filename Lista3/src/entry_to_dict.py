import read_log
from enums.http_log_keys import HTTP_LOG_KEYS

def entry_to_dict(entry: tuple) -> dict:
  """function which convert http log tuple to http log dict"""
  if len(entry) != len(HTTP_LOG_KEYS):
    raise ValueError(f'Error: length of log is incorrect!')
  
  dictionary: dict = {}
  for key_enum, value in zip(HTTP_LOG_KEYS, entry): #przyjmuje dowolne obiekty po ktorych mozna iterowac, bierze kolejno pierwszy elemetn z Enuma (TS) i pierwszy z krotki (timestamp), potem drugi i drugi itp tworzac pary
    dictionary[key_enum.value] = value
  
  return dictionary

def main():
  data: list = read_log.read_log(1)
  dictionary: dict = entry_to_dict(data[0])
  
  print(dictionary)

if __name__ == "__main__":
  main()