import sys

READ_STDIN_SIZE: int = 1

def countChars():
  """Funkcja zliczająca wszystkie znaki w tekście, z pominięciem białych znaków"""
  
  count: int = 0
  char: chr = sys.stdin.read(READ_STDIN_SIZE)
  
  while char != "":
    if not char.isspace():
      count += 1
      
    char = sys.stdin.read(READ_STDIN_SIZE)
  
  return count

def main():
  result: int = countChars()
  print(result)

if __name__ == '__main__':
  main()