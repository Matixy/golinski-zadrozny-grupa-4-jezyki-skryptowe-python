#Preambułę (zaczyna się na początku i kończy co najmniej dwoma pustymi wierszami, jesli 10 piewrszych linii nie konczy preambuly to znaczy ze takowej nie bylo)
#Informację o wydaniu (zaczyna się od linii mającej pięć myślników -----

#Napisz program, który wypisuje tylko treść książki, ignorując preambułę i informację owydaniu.
#- Program musi działać potokowo, usuwając zbędne spacje wewnątrz linii i oczyszczając
#białe znaki na początku i końcu każdej linii. Po odczytaniu EOF, niech zakończy działanie.
#- Struktura akapitów (puste linie) musi zostać zachowana.

import sys
from utils.textTools import cleanLine

# Wymuszenie kodowania UTF-8 dla wejścia i wyjścia
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

def main():
    """Glowna funckja ktora zwraca tylko tekst ksiazki pomijajac Preambule i Informacje o wydaniu z pliku txt podanego na wejsciu"""
    endOfBookTextSymbol = False
    stillInPreambula = True
    emptyLineCounter = 0
    currentLine = ""
    buffer = ""     #potrzebny w przypadku gdy Brak Preambuly
    bufferLineCounter = 0   #Liczy do 10 (sprzawdzanie Preambuly)

    try:
        while not endOfBookTextSymbol:
            currChar = sys.stdin.read(1)

            if currChar == '':      #zabezpieczenie jestli nie byloby "-----" w pliku
                if not endOfBookTextSymbol:
                    raise ValueError("Błąd formatu: Nie znaleziono znaku końca książki (-----).")   # zucamy nasz własny błąd
                break


            if currChar == '\n':                #Jesli koniec lini to sprawdzamy co mamy w tej lini
                cleanedLine = cleanLine(currentLine)

                if(cleanedLine.startswith('-----')):
                    endOfBookTextSymbol = True
                else:
                    if(cleanedLine.strip() == ''):
                        emptyLineCounter += 1
                    else:
                        emptyLineCounter = 0

                    if (not stillInPreambula):  #Wyswietlamy gotowa linie jestli to nie jest preambula
                        print(cleanedLine)
                    else:
                        buffer += cleanedLine + '\n'
                        bufferLineCounter += 1

                        if emptyLineCounter >= 2:  # Sprawdzamy czy nadal w preambule, dopiero tutaj bo w ten sposob nie wypiszemy pustego wiersza
                            stillInPreambula = False
                            buffer = ""
                        elif bufferLineCounter >= 10:
                            stillInPreambula = False
                            print(buffer, end="")
                            buffer = ""

                    currentLine = ""        #wyczyszczenie linii
            else:
                currentLine += currChar

    except ValueError as e: #Ten blok łapie błąd, który rzuciliśmy wyżej
        print(e)
        sys.exit(1) #Zamykamy program z kodem błędu 1 (co oznacza awarię)
    except Exception as e:  #Ten blok złapie wszystkie inne nieprzewidziane awarie
        print(e)
        sys.exit(1) # Zamykamy program z kodem błędu 1 (co oznacza awarię)



if __name__ == "__main__":
    main()