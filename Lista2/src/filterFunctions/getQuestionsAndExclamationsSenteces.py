import sys
from src.utils.textTools import generateSentences

def getQuestionsAndExclamationsSenteces(stream) -> str:
  """Funkcja, która wypisuje na wyjściu tylko zdania, które są pytaniami lub wykrzyknieniami"""
  
  res: str = ""
  
  for sentence in generateSentences(stream):
    if sentence[len(sentence)-1] == "!" or sentence[len(sentence)-1] == "?":
      res += sentence + "\n"
  
  return res

def main():
  #ustawienie kodowania na utf-8
  sys.stdin.reconfigure(encoding='utf-8')
  sys.stdout.reconfigure(encoding='utf-8')
  
  result: str = getQuestionsAndExclamationsSenteces(sys.stdin)
  print(result)

if __name__ == '__main__':
  main()