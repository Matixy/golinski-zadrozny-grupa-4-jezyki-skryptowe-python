import sys
from utils.textTools import generateSentences

READ_STDIN_SIZE: int = 1

def includeProperName(sentence: str) -> bool:
  """Funckja zwracajaca czy zdanie zawiera przynajmniej jedna nazwe wlasna"""
  isFirstWord: bool = True
  isInWord: bool = False
  
  for char in sentence:
    if char.isalpha():
      if not isInWord:
        isInWord = True
        
        if char.isupper() and not isFirstWord: # znaleziono nazwe wlasna
          return True 
        
    else:
      if isInWord:
        isInWord = False
        isFirstWord = False
        
  return False
            
def countPercentProperNames(stream, readSize: int = READ_STDIN_SIZE) -> float:
  """
  Funkcja licząca procent zdań, które zawierają przynajmniej jedną nazwę własną (niech
  nazwą własną będzie każdy wyraz napisany wielką literą, nie będący pierwszym
  wyrazem w zdaniu)
  """
  
  countSentences: int = 0;
  sentencesWithProperNames: int = 0;
  
  for sentence in generateSentences(stream):
    if includeProperName(sentence):
      sentencesWithProperNames += 1
      
    countSentences += 1

  return 0 if countSentences == 0 else (sentencesWithProperNames / countSentences) * 100

def main():
  #ustawienie kodowania na utf-8
  sys.stdin.reconfigure(encoding='utf-8')
  
  result: int = countPercentProperNames(sys.stdin)
  print(result)

if __name__ == "__main__":
 main()