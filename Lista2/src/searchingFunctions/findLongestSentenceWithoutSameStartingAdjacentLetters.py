import sys
from src.utils.textTools import generateSentences, findLongestSentence, configureSysInOutUtf8
from src.utils.errorHandler import runFuncWithExceptionHandling

def isValidSentenceWithoutSameStartingAdjacentLetters(sentence):
    """Sprawdza, czy żadne dwa sąsiadujące słowa nie zaczynają się na tę samą literę. Zgodnie z wymogami, analizujemy zdanie znak po znaku bez użycia list."""

    lastFirstLetter = ""
    isInWord = False

    for char in sentence:
        # Wyraz to ciąg znaków alfabetu
        if char.isalpha():
            if not isInWord:    #Jesli wczesniej nie bylismy w wyrazie to znaczy ze teraz musimy zapamietac litere
                currentFirstLetter = char.lower()   #To jest pierwsza litera nowego słowa

                if currentFirstLetter == lastFirstLetter:   #Porównanie z pierwszą literą poprzedniego słowa
                    return False

                lastFirstLetter = currentFirstLetter
                isInWord = True
        else:
            isInWord = False    #Znaki interpunkcyjne lub spacje oddzielają wyrazy

    return True


def main():
    configureSysInOutUtf8()

    resultSentence = findLongestSentence(sys.stdin, isValidSentenceWithoutSameStartingAdjacentLetters)
    print(resultSentence)


if __name__ == "__main__":
    runFuncWithExceptionHandling(main)