import sys
from src.utils.textTools import findLongestSentence, configureSysInOutUtf8
from src.utils.errorHandler import runFuncWithExceptionHandling

def main():
    configureSysInOutUtf8()

    resultSentence = findLongestSentence(sys.stdin)
    print(resultSentence)


if __name__ == "__main__":
    runFuncWithExceptionHandling(main)