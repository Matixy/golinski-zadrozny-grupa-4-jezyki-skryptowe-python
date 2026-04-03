def sort_dict(dictionary: dict, reverse: bool = False) -> dict:
  """Return a new dictionary sorted by keys."""
  
  return dict(sorted(dictionary.items(), reverse=reverse))


def get_filtered_dict(dictionary: dict, filtered_keys: list) -> dict:
  """Return a case-insensitive filtered dict with keys containing any of the given substrings"""
  
  res_dict: dict = {}
  
  # normalize filter keys to lowercase for case-insensitive comparison
  lower_filters: list = [key.lower() for key in filtered_keys]
  
  # iterate through all dictionary items
  for key, value in dictionary.items():
    lower_dict_key: str = key.lower()
    
    # for each key, check if it contains any of the filter substrings
    for filter_key in lower_filters:
      # if a match is found, add original key-value pair to result and stop checking further filters
      if any(filter_key in lower_dict_key for filter_key in lower_filters):
        res_dict[key] = value
    
  return res_dict