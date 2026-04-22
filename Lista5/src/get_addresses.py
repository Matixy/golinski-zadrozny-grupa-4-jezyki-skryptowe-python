import re
from re import Pattern, Match
import pathlib
from pathlib import Path
from enums.metadata_keys import METADATA_KEYS
import csv_parser

def get_addresses(path: Path, city: str) -> list[tuple[str, str, str, str]]:
  """"
  Functions returns list of tuple with adress of station from .csv file if city match with argument
  if address is not provided on station returns NONE in tuple
  
  DATA FORMAT:
  [
    ('DOLNOŚLĄSKIE', 'Głogów', 'Norwida', '3')
    ('DOLNOŚLĄSKIE', 'Głogów', 'Orzechowa', None)
    ('DOLNOŚLĄSKIE', 'Brzeg Głogowski', None, None)
    ('DOLNOŚLĄSKIE', 'Świdnica', 'Karola Marcinkowskiego', '4-6')
  ]
  """
  
  stations_data: dict = csv_parser.parse_metadata(path)
  addresses: list[tuple[str, str, str, str]] = []
  
  city_pattern = re.compile(rf"^{re.escape(city)}$", re.IGNORECASE) # f- provides that regex can contain python variables, re.escape(city)- get city variable into regex including special signs which regex using like "() ." etc.
  
  # regex:
  # (?:ul. )? - match standard ul. prefix (? at end means this group is optional)
  # .*?- any character- ., repeated zero or more times- *, ?- matches as little as possible
  # ?:- non-capturing group (used only for grouping), \s- any whitespace, + - one or more whitespace
  # \d- digit, + - one or more
  # [a-zA-Z] - any letter, ? - zero or one letter (optional)
  # (?:- non-capturing group for optional second part, [/-] - "/" or "-", \d+ - one or more digits
  # [a-zA-Z]? - optional letter suffix
  # ? at the ends means that each group is optional
  address_pattern: Pattern = re.compile(r"^(?:ul. )?(?P<street>.*?)(?:\s+(?P<number>\d+[a-zA-Z]?(?:[/-]\d+[a-zA-Z]?)?))?$")
  
  for station in stations_data.values():
    region: str = station.get(METADATA_KEYS.REGION.value, "").strip()
    station_city: str = station.get(METADATA_KEYS.CITY.value, "").strip()
    address: str = station.get(METADATA_KEYS.ADDRESS.value, "").strip()
    
    if city_pattern.match(station_city):
      street: str = None
      house_number = None
      
      # if address exist check it
      if address:
        address_match: Match[str] = address_pattern.match(address)
        if address_match:
          street = address_match.group("street")
          house_number = address_match.group("number")
      
      addresses.append((region, station_city, street, house_number))
        
  return addresses

def main():
  p = Path("data") / "stacje.csv"
  res = get_addresses(p, "Świdnica")
  for i in res:
    print(i)

if __name__ == "__main__":
    main()