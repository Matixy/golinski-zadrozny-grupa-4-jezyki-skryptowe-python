import re
from datetime import datetime
from re import Match, Pattern

POLISH_LETTERS: dict[str, str] = {
  "ą": "a", 
  "ć": "c", 
  "ę": "e", 
  "ł": "l",
  "ń": "n", 
  "ó": "o", 
  "ś": "s", 
  "ź": "z", 
  "ż": "z",
  "Ą": "A", 
  "Ć": "C", 
  "Ę": "E", 
  "Ł": "L",
  "Ń": "N", 
  "Ó": "O", 
  "Ś": "S", 
  "Ź": "Z", 
  "Ż": "Z",
}

def format_date(date: str) -> str:
  """"Function returns from date DD/MM/YY HH:MM str to YYYY-MM-DD using regex - if date is not in right format return given date"""
  pattern: Pattern[str] = re.compile(r"^(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{2})\s(?P<hour>\d{2}):(?P<minute>\d{2})$") # regex groupping data in format DD/MM/YY HH:MM- "01/04/23 12:00"
  
  date_match: Match[str] = pattern.match(date)
  if date_match:
    day: str = date_match.group("day")
    month: str = date_match.group("month")
    year: int = int(date_match.group("year"))
    
    current_year = datetime.now().year % 100
    if year > current_year:
      year += 1900
    else:
      year += 2000
        
    return str(year) + "-" + month + "-" + day
  
  return date

def format_coordinate(coordinate: str):
  """"Function returns converted coordinate as float with X.XXXXXX (6 digits after ".") if str is empty return empty str"""
  pattern: Pattern[str] = re.compile(r"^(?P<integer_part>\d+)\.?(?P<fractional_part>\d{6})$") # regex- before dot minimum one digit, after must be 6
  
  coordinate_match: Match[str] = pattern.match(coordinate)
  if coordinate_match:
    integer_part: str = coordinate_match.group("integer_part")
    fractional_part: str = coordinate_match.group("fractional_part")
    return float(f"{integer_part}.{fractional_part}")
  
  return coordinate

def has_two_part_name(txt: str) -> tuple:
  """"Returns tuple if txt has two part name- contain '-' else return None"""
  pattern: Pattern[str] = re.compile(r"^(?P<first_part>[^-]+)-(?P<second_part>[^-]+)$") # regex- before and after - must be something [^-] means everything except '-'
  
  txt_match: Match[str] = pattern.match(txt)
  if txt_match:
    first_part: str = txt_match.group('first_part').strip()
    second_part: str = txt_match.group('second_part').strip()
    return (first_part, second_part)
  
  return None

def normalize_str(txt: str) -> str:
  """"normalizes string by converting space symbols to '_' and polish signs to latin"""
  txt = re.sub(r"\s+", "_", txt) # replace space to '_'
  
  pattern: Pattern[str] = re.compile("|".join(POLISH_LETTERS.keys())) # build ą|ć|ę|ł regex
  txt = pattern.sub(lambda letter: POLISH_LETTERS[letter.group()], txt) # change each letter to value from dict
  
  return txt

def has_suffix(txt: str, suffix: str) -> bool:
  """"checks if txt string has given suffix"""
  pattern: Pattern[str] = re.compile(re.escape(suffix) + r"$") # re.escape protect for special regex signs like "() ." etc. + r"$" means end of regex
  txt_match: Match[str] = pattern.search(txt) # search going from all string not only from start
  
  return bool(txt_match)

def has_three_part_name(txt: str):
  """"Returns tuple if txt has three part name- contain '-' else return None"""
  pattern: Pattern[str] = re.compile(r"^(?P<first_part>[^-]+)-(?P<second_part>[^-]+)-(?P<third_part>[^-]+)$") # regex- before and after - must be something 
  
  txt_match: Match[str] = pattern.match(txt)
  if txt_match:
    first_part: str = txt_match.group('first_part').strip()
    second_part: str = txt_match.group('second_part').strip()
    third_part: str = txt_match.group('third_part').strip()
    return (first_part, second_part, third_part)
  
  return None
  
def has_street_or_alley_in_name(txt: str) -> bool:
  """"checks if txt string has comma and then street or alley prefix- 'ul.'/'al'"""
  
  #regex explanation- checking in string if exist comma and alley or street prefix no matter by order- "ul. Chopina 35, Bogatynia" / "Wrocław, ul. Bartnicza"
  # (?=)- only checking if given pattern exist in str but not taking it
  # .*- any chars
  # \b- letter border to out "bul" only "al"/"ul"
  pattern: Pattern[str] = re.compile(r"^(?=.*,)(?=.*\b(?:ul|al)\.)")
  
  txt_match: Match[str] = pattern.match(txt)
  
  if txt_match:
    return True
  
  return False