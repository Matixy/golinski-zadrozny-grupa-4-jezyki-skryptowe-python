import sys
from src.utils.textTools import configureSysInOutUtf8
from src.utils.errorHandler import runFuncWithExceptionHandling

READ_STDIN_SIZE: int = 1

def countParagraphs(stream, readSize: int = READ_STDIN_SIZE) -> int:
  """Funkcja zliczająca akapity w tekście (akapit jest oddzielony pustą linią)"""
  
  count: int = 0
  isFirstParagraph: bool = True
  wasLastCharNewline: bool = False
  
  char: chr = stream.read(readSize)
  
  while char != "":

    if not isFirstParagraph:
      if char != "\n" and wasLastCharNewline:
        count += 1
        wasLastCharNewline = False
      elif char == "\n" and not wasLastCharNewline:
        wasLastCharNewline = True
    else: # warunek sprawdzajacy czy tekst nie zaczyna sie od pustych enterow
      if char != "\n": # znalezienei pierwszeo akapitu
        isFirstParagraph = False
        count += 1
      
    char = stream.read(readSize)
    
  
  return count

def main():
  configureSysInOutUtf8()
  
  result: int = countParagraphs(sys.stdin)
  print(result)

if __name__ == "__main__":
 runFuncWithExceptionHandling(main)