import sys
from utils.textTools import generateSentences

READ_STDIN_SIZE: int = 1

def getMax4WordsSentences(stream, readSize: int = READ_STDIN_SIZE) -> str:
  """Funkcja wypisująca tylko zdania zawierające co najwyżej 4 wyrazy"""
  
  res: str = ""
  
  for sentence in generateSentences(stream):
    
  
  return res

def main():
  #ustawienie kodowania na utf-8
  sys.stdin.reconfigure(encoding='utf-8')
  
  result: str = getMax4WordsSentences(sys.stdin)
  print(result)

if __name__ == '__main__':
  main()