import sys
from utils.textTools import generateSentences

def getFirst20Sentences(stream) -> str:
  """Funkcja wypisująca pierwszych 20 zdań tekstu"""
  
  res: str = ""
  generator = generateSentences(stream)
  counter: int = 0
  
  while counter != 19:
    try:
      sentence = next(generator)
      res += sentence + "\n"
      counter += 1
    except StopIteration: # teskt ma mniej niz 20 zdan zakoncz petle
      break;
  
  return res

def main():
  #ustawienie kodowania na utf-8
  sys.stdin.reconfigure(encoding='utf-8')
  
  result: str = getFirst20Sentences(sys.stdin)
  print(result)

if __name__ == '__main__':
  main()