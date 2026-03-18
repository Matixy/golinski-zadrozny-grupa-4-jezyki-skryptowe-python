import sys

def generateSentences(stream):
  """Funkcja czytajaca strumien i zwracajaca zdania w tekscie"""
  sentence: str = ""
  char: chr = stream.read(1)
  
  newlineCount: int = 0  # Licznik znaków nowej linii
  hasLetters: bool = False # flaga odnosnie czy w zdaniu jest znak alfabetu
  
  while char != "":
    
    # warunki dot. licznika lini i tworzenia zdania
    if char == "\n":
      newlineCount += 1 # zwiekszenie licznika lini
      sentence += " "
    else:
      sentence += char
      
      if not char.isspace():
        newlineCount = 0 # napotkano znak (niebedacy bialym znakiem)- reset
      
    # sprawdzenie flagi liter
    if char.isalpha():
      hasLetters = True
      
    # warunek dot. konca zdania normalnie i konca zdania przez akapit- min. 2 puste linie
    if char == "." or char == "?" or char == "!" or newlineCount >= 2:
      if hasLetters:
        yield sentence.strip() # zwrocenie wartosci i uspienie funkcji do kolejnego zadania
        
      sentence = ""
      newlineCount = 0 # reset licznika nowej lini
      hasLetters = False
  
    char = stream.read(1)
    
  # zabezpieczenie sprawdzajace czy plik skonczyl sie bez kropki- ale zostaly znaki
  if hasLetters:
    yield sentence.strip()

def cleanLine(lineToClean):
  """Funckja czyszczaca podana linie tekstu z nadmiarowych spacji w srodku i bialych znakow na poczatku i koncu """
  lineToClean = lineToClean.strip()  # Usuwamy z poczatku i konca
  cleanedLine = ""
  lastCharWasSpace = False

  for char in lineToClean:  # petla usuwajaca spacje
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
  """Funkcja zwracajaca pierwszy wyraz z zdania"""
  
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
  
  return word # jezeli wyraz byl na samym koncu stringa zwracany jest wyraz- jezeli nie bylo zwracane jest ""
        
def findLongestSentence(stream, predicateFunction=None):  #opcjonalna funckja filtrujaca
  """Funkcja wyszukujaca najdłuższe zdanie w książce (kryterium – liczba znaków). Obsluguje podanie predykatu do sprawdzenia przed porownanie dlugosci"""
  longestSentence = ""
  maxSentenceLength = 0

  for sentence in generateSentences(stream):
    if predicateFunction is None or predicateFunction(sentence):  #Jesli nie ma warunku lub jest spelniony porownujemy
      currentSentenceLength = len(sentence)
      if currentSentenceLength > maxSentenceLength:
        longestSentence = sentence
        maxSentenceLength = currentSentenceLength

  if not longestSentence:
    raise ValueError("Nie znaleziono zadnych zdan w podanym tekscie")

  return longestSentence

def configureSysInOutUtf8():
  """ustawienie kodowania potoku na utf-8 dla stdin i stdout"""
  
  sys.stdin.reconfigure(encoding='utf-8')
  sys.stdout.reconfigure(encoding='utf-8')