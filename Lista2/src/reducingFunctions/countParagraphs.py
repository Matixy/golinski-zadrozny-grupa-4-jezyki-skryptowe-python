import sys

READ_STDIN_SIZE: int = 1

def countParagraphs(stream, readSize: int = 1):
  """Funkcja zliczająca akapity w tekście (akapit jest oddzielony pustą linią)"""
  
  count: int = 0
  char: chr = sys.stdin.read(READ_STDIN_SIZE)
  
  while char != "":
    if char == "\n":
      count += 1
  
    char = sys.stdin.read(READ_STDIN_SIZE)
  
  return count

def main():
  result: int = countParagraphs()
  print(result)

if __name__ == "__main__":
 main()