import os
import read_log
from entry_to_dict import entry_to_dict
from enums.http_log_keys import HTTP_LOG_KEYS

def get_extension_stats(log: list) -> dict:
  """returns number of occurrences of each extension in log"""
  extension_stats: dict = {}
  for l in log:
    log_dict: dict = entry_to_dict(l) # convert single log to dictonary
    path: str = log_dict[HTTP_LOG_KEYS.URI.value]
    
    
    clean_path: str = path.split('?')[0] # delete html params which are not path
    last_slash_index: int = clean_path.rfind('/') # finding last slash
    file_name: str = clean_path[last_slash_index + 1:]
    dot_index: int = file_name.rfind('.')
    
    # if filename exists increment extension_stats
    if dot_index != -1 and dot_index < len(file_name) - 1: #check if dot exists in filename and if dot is not the last char in filename
      extension: str = file_name[dot_index + 1:].lower()
      
      # validation- extension need to be alphanumeric (only digits and letters)
      if extension.isalnum():
        extension_stats[extension] = extension_stats.get(extension, 0) + 1
    
  return extension_stats

def main():
  data: list = read_log.read_log()
  extension_stats: list = get_extension_stats(data)
  
  print(extension_stats)

if __name__ == "__main__":
  main()