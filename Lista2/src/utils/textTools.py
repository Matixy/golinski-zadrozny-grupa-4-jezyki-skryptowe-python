def generateSentences(stream, readSize: int = 1):
  """Funkcja czytajaca strumien i zwracajaca zdania w tekscie"""
  sentence: str = ""
  char: chr = stream.read(readSize)
  
  newlineCount: int = 0  # Licznik znaków nowej linii
  hasLetters: bool = False # flaga odnosnie czy w zdaniu jest znak alfabetu
  
  while char != "":
    
    # warunki dot. licznika lini
    if char == "\n":
      newlineCount += 1 # zwiekszenie licznika lini
    elif not char.isspace():
      newlineCount = 0 # napotkano znak - reset
      
    if char.isalpha():
      hasLetters = True
      
    # tworzenie zdania
    if char == "\n":
      sentence += " "
    else:
      sentence += char
      
    # warunek dot. konca zdania normalnie i konca zdania przez akapit- min. 2 puste linie
    if char == "." or char == "?" or char == "!" or newlineCount >= 2:
      if hasLetters:
        yield sentence.strip() # zwrocenie wartosci i uspienie funkcji do kolejnego zadania
        
      sentence = ""
      newlineCount = 0 # reset licznika nowej lini
      hasLetters = False
  
    char = stream.read(readSize)
    
  # zabezpieczenie sprawdzajace czy plik skonczyl sie bez kropki- ale zostaly znaki
  if hasLetters:
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

def countWords(text: str) -> int:
  """Funkcja liczaca wyrazy w tekscie"""
  wordsCount: int = 0
  isInWord: bool = False
  
  for char in text:
    if char.isalpha():
      if not isInWord:
        wordsCount += 1
        isInWord = True
    else:
      if isInWord:
        isInWord = False
      
  return wordsCount

def getWord(text: str) -> str:
  """Funkcja zwracajaca 1 wyraz z zdania"""
  
  word: str = ""
  isInWord: bool = False
  
  for char in text:
    if char.isalpha():
      if not isInWord:
        isInWord = True
        
      word += char
    else:
      if isInWord:
        return word
        