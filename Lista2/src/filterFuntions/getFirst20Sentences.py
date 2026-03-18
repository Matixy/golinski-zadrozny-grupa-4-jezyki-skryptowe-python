import sys
from src.utils.textTools import generateSentences

def getFirst20Sentences(stream) -> str:
  """Funkcja wypisująca pierwszych 20 zdań tekstu"""
  
  res: str = ""
  generator = generateSentences(stream) # drugi argument oznacza jaka wartosc generator ma zwrocic gdy potok sie skonczy
  
  counter: int = 0
  sentence = next(generator, None)
  while counter < 20 and sentence != None:    
    res += sentence + "\n"
    
    counter += 1
    sentence = next(generator, None) # drugi argument oznacza jaka wartosc generator ma zwrocic gdy potok sie skonczy
  
  return res

def main():
  #ustawienie kodowania na utf-8
  sys.stdin.reconfigure(encoding='utf-8')
  
  result: str = getFirst20Sentences(sys.stdin)
  print(result)

if __name__ == '__main__':
  main()