import sys
from src.utils.textTools import generateSentences, getWord, configureSysInOutUtf8

APPEARANCES_SELECTED_SIGNS: int = 2

def getSelectedSentences(stream, appearances: int) -> str:
  """
  Funkcja wypisująca tylko zdania, które zawierają co najmniej dwa wyrazy z
  następujących: „i”, „oraz”, „ale”, „że”, „lub”
  """
  
  res: str = ""
  
  for sentence in generateSentences(stream):
    counterSelectedWords: int = 0
    tempSentence: str = sentence
    word: str = getWord(tempSentence)
    
    while word != "":
      wordToCheck: str = word.lower() # standaryzacja liter gdyby wyraz byly na poczatku zdania
      
      if (
        wordToCheck == "i" 
        or wordToCheck == "oraz" 
        or wordToCheck == "ale" 
        or wordToCheck == "że" 
        or wordToCheck == "lub"):
        counterSelectedWords += 1
        
      wordStartIndexInSentence: int = tempSentence.find(word)
      wordEndIndexInSentence: int = wordStartIndexInSentence + len(word)
      
      tempSentence = tempSentence[wordEndIndexInSentence:] # uciecie zdania o sprawdzony wyraz
      word: str = getWord(tempSentence) # przejscie do kolejnego wyrazu
  
    if counterSelectedWords >= appearances:
      res += sentence + "\n"
      
  return res

def main():
  #ustawienie kodowania na utf-8
  configureSysInOutUtf8()
  
  result: str = getSelectedSentences(sys.stdin, APPEARANCES_SELECTED_SIGNS)
  print(result)

if __name__ == '__main__':
  main()