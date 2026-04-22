import re
import pathlib
from pathlib import Path

# ^- start
# ?P<year> - strip value provides form regex and create group named year which can be used latter
# \d- digit, {4}- exactly 4 digits
# .- take all chars, +- one or more
# \w- take letters or digits or _
# \.- means "."
MEASUREMENT_FILE_NAME_REGEX: re = r"^(?P<year>\d{4})_(?P<pollutant>.+)_(?P<frequency>\w+)\.csv$"

def group_measurement_files_by_key(path: Path) -> dict[tuple[str, str, str], Path]:
  """"
  Functions search files in path folder and returns paths to this files which is correct with measurement keys, searching don't includes subfolders
  
  DATA FORMAT:
  {
    (2023, BkF(PM10), 24g): "Lista5\data\measurements\\2023_BkF(PM10)_24g.csv"\n
  }
  """
  
  files_dict: dict[tuple[str, str, str], Path] = {}
  
  #check if path is directory
  if not path.is_dir():
    return files_dict
  
  pattern = re.compile(MEASUREMENT_FILE_NAME_REGEX)
  
  for file_path in path.iterdir():
    if not file_path.is_file():
      continue # skip this if path is directory
    
    match = pattern.match(file_path.name)
    if match:
      year: str = match.group("year")
      pollutant: str = match.group("pollutant")
      frequency: str = match.group("frequency")

      key: tuple = (year, pollutant, frequency)
      
      files_dict[key] = file_path

  return files_dict

def main():
  p = Path("data") / "measurements"
  res = group_measurement_files_by_key(p)
  for key,val in res.items():
    print(f'{key} = {val}')

if __name__ == "__main__":
    main()