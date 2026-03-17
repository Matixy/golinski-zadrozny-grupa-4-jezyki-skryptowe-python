import sys

def countSentences(stream, readSize: int = 1):
  """Funkcja zliczająca zdania w tekscie"""
  count: int = 0
  char: chr = sys.stdin.read(readSize)
  
  while char != "":
    if char == "." or char == "?" or char == "!":
      count += 1
  
    char = sys.stdin.read(readSize)
  
  return count