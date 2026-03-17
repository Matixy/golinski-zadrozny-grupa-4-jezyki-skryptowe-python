
def countSentences(stream, readSize: int = 1):
  """Funkcja zliczająca zdania w tekscie"""
  count: int = 0
  char: chr = stream.read(readSize)
  
  while char != "":
    if char == "." or char == "?" or char == "!":
      count += 1
  
    char = stream.read(readSize)
  
  return count