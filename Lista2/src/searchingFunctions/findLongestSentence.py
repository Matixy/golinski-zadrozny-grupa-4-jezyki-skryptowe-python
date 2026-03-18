import sys
from src.utils.textTools import generateSentences

def findLongestSentence(stream):
    """Funkcja wypisująca najdłuższe zdanie w książce (kryterium – liczba znaków)."""
    longestSentence = ""
    maxSentenceLength = 0

    for sentence in generateSentences(stream):
        currentSentenceLength = len(sentence)
        if currentSentenceLength > maxSentenceLength:
            longestSentence = sentence
            maxSentenceLength = currentSentenceLength

    if not longestSentence:
        raise ValueError("Nie znaleziono zadnych zdan w podanym tekscie")

    return longestSentence

def main():
    try:
        sys.stdin.reconfigure(encoding='utf-8')
        resultSentence = findLongestSentence(sys.stdin)
        print(resultSentence)

    except ValueError as e:
        print(e, file=sys.stderr)
    except Exception as e:
        print(e, file=sys.stderr)

if __name__ == "__main__":
    main()