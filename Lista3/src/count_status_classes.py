import read_log
import sort_log

STATUS_CODE_INDEX: int = 9

def  count_status_classes(log: list) -> dict:
  """returns a dictionary with the status classes of HTML classes with the number of each class"""
  status_classes: dict = {}
  for row in log:
    status_code: int = row[STATUS_CODE_INDEX]
    status_code_class: str = f'{status_code // 100}xx'
    
    status_classes[status_code_class] = status_classes.get(status_code_class, 0) + 1
    
  return dict(sort_log.sort_log(status_classes.items(), 0))

def main():
  data: list = read_log.read_log()    
  staus_classes: dict = count_status_classes(data)
  
  print(staus_classes)

if __name__ == "__main__":
  main()