def generateSentences(stream, readSize: int = 1):
  """Funkcja czytajaca strumien i zwracajaca zdania w tekscie"""
  sentence: str = ""
  char: chr = stream.read(readSize)
  
  while char != "":
    sentence += char
    
    if char == "." or char == "?" or char == "!":
      yield sentence.strip() # zwrocenie wartosci i uspienie funkcji do kolejnego zadania
      sentence = ""
  
    char = stream.read(readSize)
    
  # zabezpieczenie sprawdzajace czy plik skonczyl sie bez kropki- ale zostaly znaki
  if sentence.strip() != "":
    yield sentence.strip()

def cleanLine(lineToClean):
  """Funckja czyszczaca podana linie tekstu z nadmiarowych spacji w srodku i bialych znakow na poczatku i koncu """
  lineToClean = lineToClean.strip()  # Usuwamy z poczatku i konca
  cleanedLine = ""
  lastCharWasSpace = False

  for char in lineToClean:  # petla usuwajaca spacje ###WYDZIELIC DO FUNKCJI
    if char == " ":
      if lastCharWasSpace:
        continue
      else:
        lastCharWasSpace = True
        cleanedLine += char
    else:
      lastCharWasSpace = False
      cleanedLine += char

  return cleanedLine