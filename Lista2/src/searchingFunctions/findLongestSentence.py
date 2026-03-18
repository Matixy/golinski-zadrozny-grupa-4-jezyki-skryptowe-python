import sys
from src.utils.textTools import findLongestSentence, configureSysInOutUtf8

def main():
    try:
        configureSysInOutUtf8()

        resultSentence = findLongestSentence(sys.stdin)
        print(resultSentence)

    except ValueError as e:
        print(e, file=sys.stderr)
    except Exception as e:
        print(e, file=sys.stderr)

if __name__ == "__main__":
    main()