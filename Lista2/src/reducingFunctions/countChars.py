import sys
from src.utils.textTools import configureSysInOutUtf8
from src.utils.errorHandler import runFuncWithExceptionHandling

READ_STDIN_SIZE: int = 1

def countChars(stream, readSize: int = READ_STDIN_SIZE) -> int:
  """Funkcja zliczająca wszystkie znaki w tekście, z pominięciem białych znaków"""
  
  count: int = 0
  char: chr = stream.read(readSize)
  
  while char != "":
    if not char.isspace():
      count += 1
      
    char = stream.read(readSize)
  
  return count

def main():
  #ustawienie kodowania na utf-8
  configureSysInOutUtf8()
  
  result: int = countChars(sys.stdin)
  print(result)

if __name__ == '__main__':
  runFuncWithExceptionHandling(main)