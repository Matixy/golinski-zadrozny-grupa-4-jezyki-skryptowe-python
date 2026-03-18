import sys
from src.utils.errorHandler import runFuncWithExceptionHandling
from src.utils.textTools import generateSentences, countWords, configureSysInOutUtf8

def getMax4WordsSentences(stream) -> str:
  """Funkcja wypisująca tylko zdania zawierające co najwyżej 4 wyrazy"""
  
  res: str = ""
  
  for sentence in generateSentences(stream):
    if countWords(sentence) <= 4:
      res += sentence + "\n" # dodanie zdania do wyniku i nowej lini po dodanym zdaniu
  
  return res

def main():
  #ustawienie kodowania na utf-8
  configureSysInOutUtf8()
  
  result: str = getMax4WordsSentences(sys.stdin)
  print(result)

if __name__ == '__main__':
  runFuncWithExceptionHandling(main)