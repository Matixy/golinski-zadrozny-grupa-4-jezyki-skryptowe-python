import sys
from utils.textTools import generateSentences, countWords

def getMax4WordsSentences(stream) -> str:
  """Funkcja wypisująca tylko zdania zawierające co najwyżej 4 wyrazy"""
  
  res: str = ""
  
  for sentence in generateSentences(stream):
    if countWords(sentence) <= 4:
      res += sentence + "\n" # dodanie zdania do wyniku i nowej lini po dodanym zdaniu
  
  return res

def main():
  #ustawienie kodowania na utf-8
  sys.stdin.reconfigure(encoding='utf-8')
  
  result: str = getMax4WordsSentences(sys.stdin)
  print(result)

if __name__ == '__main__':
  main()