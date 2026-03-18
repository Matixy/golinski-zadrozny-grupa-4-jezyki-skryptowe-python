import sys
from src.utils.textTools import findLongestSentence

def main():
    try:
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')

        resultSentence = findLongestSentence(sys.stdin)
        print(resultSentence)

    except ValueError as e:
        print(e, file=sys.stderr)
    except Exception as e:
        print(e, file=sys.stderr)

if __name__ == "__main__":
    main()