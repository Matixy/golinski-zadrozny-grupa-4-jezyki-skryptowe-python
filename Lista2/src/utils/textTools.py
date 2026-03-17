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
  
def countSentences(stream, readSize: int = 1):
  """Funckcja zwracajaca liczbe zdan w tekscie"""
  
  count: int = 0;
  
  for sentence in generateSentences(stream):
    count += 1
    
  return count