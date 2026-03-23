import read_log
import sort_log

TOP_URI_TO_RETURN: int = 10
URI_INDEX: int = 8

def get_top_uris(log: list, n: int = 10) -> list:
  """returns the n most frequently occurring URIs"""
  uri_occurences: dict = {}
  for row in log:
    uri = row[URI_INDEX]
    uri_occurences[uri] = uri_occurences.get(uri, 0) + 1
  
  uris_occurences_sorted: list = sort_log.sort_log(list(uri_occurences.items()), 1, True)
  n_uris: list = []
  
  for item in uris_occurences_sorted[:n]:
    n_uris.append(item[0])
  
  return n_uris

def main():
  data: list = read_log.read_log()    
  top_uris: list = get_top_uris(data, TOP_URI_TO_RETURN)
  
  for i in top_uris:
    print(i)

if __name__ == "__main__":
  main()