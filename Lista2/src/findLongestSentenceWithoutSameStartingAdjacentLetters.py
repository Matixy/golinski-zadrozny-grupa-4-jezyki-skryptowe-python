import sys
from utils.textTools import generateSentences

def isValidSentenceWithoutSameStartingAdjacentLetters(sentence):
    """Sprawdza, czy żadne dwa sąsiadujące słowa nie zaczynają się na tę samą literę. Zgodnie z wymogami, analizujemy zdanie znak po znaku bez użycia list."""

    lastFirstLetter = ""
    isInWord = False

    for char in sentence:
        # Wyraz to ciąg znaków alfabetu
        if char.isalpha():
            if not isInWord:
                # To jest pierwsza litera nowego słowa
                currentFirstLetter = char.lower()

                # Porównanie z pierwszą literą poprzedniego słowa
                if currentFirstLetter == lastFirstLetter:
                    return False

                lastFirstLetter = currentFirstLetter
                isInWord = True
        else:
            # Znaki interpunkcyjne lub spacje oddzielają wyrazy
            isInWord = False

    return True


def findLongestValidSentence(stream):
    """Logika wyszukiwania najdłuższego zdania spełniającego warunek literowy."""
    longestSentence = ""
    maxLength = 0

    for sentence in generateSentences(stream):
        if isValidSentenceWithoutSameStartingAdjacentLetters(sentence):
            currentLength = len(sentence)
            if currentLength > maxLength:
                maxLength = currentLength
                longestSentence = sentence

    if maxLength == 0:
        raise ValueError("Nie znaleziono zdania spełniającego kryteria zadania.")

    return longestSentence


def main():
    sys.stdin.reconfigure(encoding='utf-8')
    try:
        resultSentence = findLongestValidSentence(sys.stdin)
        print(resultSentence)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()