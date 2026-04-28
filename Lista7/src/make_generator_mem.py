from typing import Callable, Generator
import functools
from make_generator import make_generator, fib

#Domknięcia- sytuacja, gdy funkcja wewnątrz innej funkcji pamięta zmienne ze swojego otoczenia, nawet gdy zewnętrzna zakończy działanie

def make_generator_mem(func: Callable[[int], any]) -> Generator:
  memoized_func = functools.cache(func) # creates dict which rembers func results
  return make_generator(memoized_func)

@functools.cache # <- decorator which provides memoization
def fib_fast(n: int) -> int: 
    if n <= 2: return 1
    return fib_fast(n - 1) + fib_fast(n - 2)

if __name__ == "__main__":
  fib_gen_fast = make_generator_mem(fib_fast)
  for _ in range(40):
    print(next(fib_gen_fast))
  print()
  
  # fib_gen = make_generator_mem(fib)
  # for _ in range(40):
  #   print(next(fib_gen))
  # print()