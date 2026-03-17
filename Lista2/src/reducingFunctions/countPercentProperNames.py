import sys

READ_STDIN_SIZE: int = 1

def countPercentProperNames():
  """
  Funkcja licząca procent zdań, które zawierają przynajmniej jedną nazwę własną (niech
  nazwą własną będzie każdy wyraz napisany wielką literą, nie będący pierwszym
  wyrazem w zdaniu)
  """
  
  count: int = 0
  char: chr = sys.stdin.read(READ_STDIN_SIZE)
  
  while char != "":
    if char == "\n":
      count += 1
  
    char = sys.stdin.read(READ_STDIN_SIZE)
  
  return count

def main():
  result: int = countPercentProperNames()
  print(result)

if __name__ == "__main__":
 main()