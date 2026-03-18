import sys
from utils.textTools import generateSentences

def getSelectedSentences(stream) -> str:
  """
  Funkcja wypisująca tylko zdania, które zawierają co najmniej dwa wyrazy z
  następujących: „i”, „oraz”, „ale”, „że”, „lub”
  """
  
  res: str = ""
  
  
  
  
  return res

def main():
  #ustawienie kodowania na utf-8
  sys.stdin.reconfigure(encoding='utf-8')
  
  result: str = getSelectedSentences(sys.stdin)
  print(result)

if __name__ == '__main__':
  main()