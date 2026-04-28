import string
import random

class PasswordGenerator:
  DEFAULT_CHARSET: str = string.ascii_letters + string.digits
  
  def __init__(self, length: int, charset: str, count: int):
    if length <= 0:
      raise ValueError("length must be greater than 0")
    
    if count <= 0:
      raise ValueError("count must be greather than 0")
        
    # if charset is None or len == 0- set default value all chars and numbers
    if not charset:
      self.charset: str = self.DEFAULT_CHARSET
    else:
      self.charset: str = charset
      
    self.length: int = length
    self.count: int = count
    self.generated: int = 0
      
  def __iter__(self):
    return self
  
  def __next__(self):
    if self.generated >= self.count:
      raise StopIteration # signals "the end"
    
    self.generated += 1
    
    return "".join(random.choice(self.charset) for _ in range(self.length))
  
  
if __name__ == "__main__":
  passwordGenerator: PasswordGenerator = PasswordGenerator(3, None, 5)
  passwordGenerator2: PasswordGenerator = PasswordGenerator(5, "a2cx", 2)
  passwordGenerator3: PasswordGenerator = PasswordGenerator(4, "ab", 3)
  
  for password in passwordGenerator:
    print(password)
  print()
    
  for password in passwordGenerator2:
    print(password)
  print()
  
  try:
    password: str = next(passwordGenerator3)
    while password:
      print(password)
      password = next(passwordGenerator3)
  except StopIteration as e:
    print(e)
    
  try:
    passwordGenerator4: PasswordGenerator = PasswordGenerator(-3, None, 5)
  except ValueError as e:
    print(e)
    
  try:
    passwordGenerator5: PasswordGenerator = PasswordGenerator(3, None, -5)
  except ValueError as e:
    print(e)