#Preambułę (zaczyna się na początku i kończy co najmniej dwoma pustymi wierszami, jesli 10 piewrszych linii nie konczy preambuly to znaczy ze takowej nie bylo)
#Informację o wydaniu (zaczyna się od linii mającej pięć myślników -----

#Napisz program, który wypisuje tylko treść książki, ignorując preambułę i informację owydaniu.
#- Program musi działać potokowo, usuwając zbędne spacje wewnątrz linii i oczyszczając białe znaki na początku i końcu każdej linii. Po odczytaniu EOF, niech zakończy działanie.
#- Struktura akapitów (puste linie) musi zostać zachowana.

import sys
from utils.textTools import cleanLine

# Wymuszenie kodowania UTF-8 dla wejścia i wyjścia
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

def main():
    """Glowna funckja ktora zwraca tylko tekst ksiazki pomijajac Preambule i Informacje o wydaniu z pliku txt podanego na wejsciu"""
    endOfBookTextSymbol = False #flaga czy byl juz symbol "-----"
    stillInPreambula = True     #flaga czy nadal jestesmy w preambule
    emptyLineCounter = 0        #licznik pustych linii do sprawdzania preambuly
    currentLine = ""
    buffer = ""                 #potrzebny w przypadku gdy Brak Preambuly
    bufferLineCounter = 0       #Liczy do 10 (sprzawdzanie gdy brak Preambuly)
    bookTextStarted = False     #flaga do ignorowania pustych linii po preambule
    orderedEmptyLinesCounter = 0       #licznik pustych linii do "odroczonego" wypisania


    try:
        while not endOfBookTextSymbol:
            currChar = sys.stdin.read(1)

            if currChar == '':      #zabezpieczenie jestli nie byloby "-----" w pliku
                if not endOfBookTextSymbol:
                    raise ValueError("Błąd formatu: Nie znaleziono znaku końca książki (-----).")   #Rzucamy nasz własny błąd
                break


            if currChar == '\n':                #Jesli koniec lini to sprawdzamy co mamy w tej lini
                cleanedLine = cleanLine(currentLine)

                if(cleanedLine.startswith('-----')):
                    endOfBookTextSymbol = True
                else:
                    if(cleanedLine == ''):
                        emptyLineCounter += 1
                    else:
                        emptyLineCounter = 0

                    if not stillInPreambula:
                        if not bookTextStarted:     #Ignorujemy puste linie, dopóki nie zacznie się faktyczna treść
                            if cleanedLine != "":
                                bookTextStarted = True
                                print(cleanedLine)  #Wyswietlamy gotowa linie jestli to nie jest preambula
                        else:                       #Jesli ksiazka juz wystartowala to sprawdzamy czy to nie ostatnie puste linie przed "-----", jesli tak to je iminiemy, jesli nie to wyswietlimy odpowiednia ilosc pominietych pustych wierszy aby zachowac spojnosc z akapitami
                            if cleanedLine == "":
                                orderedEmptyLinesCounter += 1
                            else:
                                while orderedEmptyLinesCounter > 0:
                                    print("")
                                    orderedEmptyLinesCounter -= 1
                                print(cleanedLine)

                    else:
                        buffer += cleanedLine + '\n'
                        bufferLineCounter += 1

                        if emptyLineCounter >= 2:  # Sprawdzamy czy nadal w preambule, dopiero tutaj bo w ten sposob nie wypiszemy pustego wiersza
                            stillInPreambula = False
                            buffer = ""
                        elif bufferLineCounter >= 10:
                            stillInPreambula = False
                            bookTextStarted = True
                            print(buffer, end="")
                            buffer = ""

                    currentLine = ""        #wyczyszczenie linii
            else:
                currentLine += currChar

    except ValueError as e: #Ten blok łapie błąd, który rzuciliśmy wyżej
        print(e, file=sys.stderr) # Wypisze na ekran, ale nie do potoku
        sys.exit(1) #Zamykamy program z kodem błędu 1 (co oznacza awarię)
    except Exception as e:  #Ten blok złapie wszystkie inne nieprzewidziane awarie
        print(e, file=sys.stderr) # Wypisze na ekran, ale nie do potoku
        sys.exit(1) # Zamykamy program z kodem błędu 1 (co oznacza awarię)



if __name__ == "__main__":
    main()