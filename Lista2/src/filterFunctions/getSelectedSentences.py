import sys
from src.utils.textTools import generateSentences, getWord

def getSelectedSentences(stream) -> str:
  """
  Funkcja wypisująca tylko zdania, które zawierają co najmniej dwa wyrazy z
  następujących: „i”, „oraz”, „ale”, „że”, „lub”
  """
  
  res: str = ""
  
  for sentence in generateSentences(stream):
    counterSelectedWords: int = 0
    
    while sentence != "":
      word: str = getWord(sentence)
      print(word)
      
      if word == "i" or word == "oraz" or word == "ale" or word == "że" or word == "lub":
        print(word)
        
      sentence = sentence[:sentence.find(word)]
  
  return res

def main():
  #ustawienie kodowania na utf-8
  sys.stdin.reconfigure(encoding='utf-8')
  sys.stdout.reconfigure(encoding='utf-8')
  
  result: str = getSelectedSentences(sys.stdin)
  print(result)

if __name__ == '__main__':
  main()