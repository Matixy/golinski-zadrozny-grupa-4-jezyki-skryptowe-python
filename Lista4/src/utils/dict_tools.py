def sort_dict(dictionary: dict, reverse: bool = False) -> dict:
  """Function which returns dict sorted by keys"""
  
  return dict(sorted(dictionary.items(), reverse=reverse))


def get_filtered_dict(dictionary: dict, *args) -> dict:
  """Case-insensitive function which returns dict contains only keys in arguments"""
  
  # get dict lower case keys
  dict_keys: list = [key.lower() for key in dictionary.keys()]
  
  for arg in args: 
    if arg.lower() == di
    
    
  return {}