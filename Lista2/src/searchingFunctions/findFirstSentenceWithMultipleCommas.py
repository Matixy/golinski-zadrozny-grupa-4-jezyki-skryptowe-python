import sys
from src.utils.textTools import generateSentences

def findFirstComplexSentence(stream):
    """Funkcja wyszukujaca pierwsze zdanie ktore ma wiecej niz jedno zdanie podrzedne (na podstawie przecinkow)"""
    for sentence in generateSentences(stream):
        commaCounter = 0

        for char in sentence:       #Iterujemy znak po znaku, aby policzyć przecinki
            if char == ',':
                commaCounter += 1

        if commaCounter > 1:        #Jesli wiecej niz 1 przecinek to zwracamy
            return sentence
    raise ValueError("W tekście nie znaleziono zdania z więcej niż jednym przecinkiem")


def main():
    try:
        sys.stdin.reconfigure(encoding='utf-8')
        resultSentence = findFirstComplexSentence(sys.stdin)    # Pobieramy dane ze stdin (przekazane potokiem)
        print(resultSentence)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()