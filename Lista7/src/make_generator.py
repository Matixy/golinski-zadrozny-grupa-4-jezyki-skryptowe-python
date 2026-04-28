from typing import Callable, Generator

#Domknięcia- sytuacja, gdy funkcja wewnątrz innej funkcji pamięta zmienne ze swojego otoczenia, nawet gdy zewnętrzna zakończy działanie

def make_generator(func: Callable[[int], any]) -> Generator:
  def inner_generator():
    n = 1
    while True:
      yield func(n)
      n += 1

  return inner_generator()

def fib(n: int) -> int:
  if n <= 2:
    return 1
  return fib(n - 1) + fib(n - 2)

if __name__ == "__main__":
  fib_gen = make_generator(fib)
  for _ in range(40):
    print(next(fib_gen))
  print()
  
  geom_gen = make_generator(lambda n: 2 ** n)
  for _ in range(5):
    print(next(geom_gen))
  print()
  
  pow_gen = make_generator(lambda n: n ** 2)
  for _ in range(5):
    print(next(pow_gen))
  print()