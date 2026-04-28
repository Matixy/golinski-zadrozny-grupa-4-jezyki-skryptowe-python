from collections.abc import Callable, Iterable
from typing import Any

def forall(pred: Callable[[Any], bool], iterable: Iterable) -> bool:
    for elem in iterable:
        if not pred(elem):
            return False
        
    return True



def exists(pred: Callable[[Any], bool], iterable: Iterable) -> bool:
    for elem in iterable:
        if pred(elem):
            return True
        
    return False


def atleast(n: int, pred: Callable[[Any], bool], iterable: Iterable) -> bool:
    counter=0
    for elem in iterable:
        if pred(elem):
            counter+=1
            if counter >= n:
                return True
    
    return False


def atmost(n: int, pred: Callable[[Any], bool], iterable: Iterable) -> bool:
    counter=0
    for elem in iterable:
        if pred(elem):
            counter+=1
            if counter > n:
                return False

    return True        




def main():
    print(f"A) {forall(lambda x: x%2==0, [2,58])}")
    
    print(f"B) {exists(lambda x: x%2==0, [1,1,1,1])}")

    print(f"C) {atleast(5, lambda x: x%2==0, [2,2,2,2,2,7,7])}")

    print(f"D) {atmost(5, lambda x: x%2==0, [2,2,2,2,2,7,7,2])}")


if __name__ == "__main__":
    main()