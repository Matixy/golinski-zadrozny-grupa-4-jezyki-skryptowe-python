#Preambułę (zaczyna się na początku i kończy co najmniej dwoma pustymi wierszami, jesli 10 piewrszych linii nie konczy preambuly to znaczy ze takowej nie bylo)
#Informację o wydaniu (zaczyna się od linii mającej pięć myślników -----
import sys
import os
from utils.textTools import cleanLine

# Wymuszenie kodowania UTF-8 dla wejścia i wyjścia
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

def extractTextFromBook(stream, outputFunction):
    """Funckja ktora zwraca tylko tekst ksiazki pomijajac Preambule i Informacje o wydaniu z pliku txt podanego na wejsciu
    Argument output_func to funkcja, która zajmie się 'odebraniem' gotowej linii."""
    endOfBookTextSymbol = False #flaga czy byl juz symbol "-----"
    stillInPreambula = True     #flaga czy nadal jestesmy w preambule
    emptyLineCounter = 0        #licznik pustych linii do sprawdzania preambuly
    currentLine = ""
    buffer = ""                 #potrzebny w przypadku gdy Brak Preambuly
    bufferLineCounter = 0       #Liczy do 10 (sprzawdzanie gdy brak Preambuly)
    bookTextStarted = False     #flaga do ignorowania pustych linii po preambule
    orderedEmptyLinesCounter = 0       #licznik pustych linii do "odroczonego" wypisania


    while not endOfBookTextSymbol:
        currChar = stream.read(1)

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
                            outputFunction(cleanedLine) #Wyowalnie przekazanej funkcji wyjsciowej ktora obsluzy wyjscie
                            # print(cleanedLine)  #Wyswietlamy gotowa linie jestli to nie jest preambula
                    else:                       #Jesli ksiazka juz wystartowala to sprawdzamy czy to nie ostatnie puste linie przed "-----", jesli tak to je iminiemy, jesli nie to wyswietlimy odpowiednia ilosc pominietych pustych wierszy aby zachowac spojnosc z akapitami
                        if cleanedLine == "":
                            orderedEmptyLinesCounter += 1
                        else:
                            while orderedEmptyLinesCounter > 0:
                                outputFunction(cleanedLine)
                                # print("")
                                orderedEmptyLinesCounter -= 1
                            outputFunction(cleanedLine)
                            # print(cleanedLine)

                else:
                    buffer += cleanedLine + '\n'
                    bufferLineCounter += 1

                    if emptyLineCounter >= 2:  # Sprawdzamy czy nadal w preambule, dopiero tutaj bo w ten sposob nie wypiszemy pustego wiersza
                        stillInPreambula = False
                        buffer = ""
                    elif bufferLineCounter >= 10:
                        stillInPreambula = False
                        bookTextStarted = True
                        outputFunction(buffer.strip("\n")) #wysylamy bufor ale bez ostatniego \n bo print go doda sam na koncu
                        # print(buffer, end="")
                        buffer = ""

                currentLine = ""        #wyczyszczenie linii
        else:
            currentLine += currChar



def main():
    """Główna funkcja programu sterujaca przekazywanym tekstem"""
    try:
        extractTextFromBook(sys.stdin, print)   #Przekazujemy sys.stdin jako źródło i print jako funkcje odbierajaca dane

        sys.stdout.flush() #Wypychamy recznie dane aby wywolac blad BrokenPipe ktory zostanie zlapany przez except

    except ValueError as e: #Ten blok łapie błąd, który rzuciliśmy wyżej
        print(e, file=sys.stderr) # Wypisze na ekran, ale nie do potoku
        sys.exit(1) #Zamykamy program z kodem błędu 1 (co oznacza awarię)
    except (BrokenPipeError): #Znalezione roziwazanie na ciche wyjście przy pękniętym potoku jesli Funkcja nie przetworzy calego wejscia
        try:
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, sys.stdout.fileno())
        except:
            pass
        sys.exit(0) #Zamyka program z kodem 0 (oznacza ze wszystko zadzialalo poprawnie)

    except Exception as e:  #Ten blok złapie wszystkie inne nieprzewidziane awarie
        print(e, file=sys.stderr) # Wypisze na ekran, ale nie do potoku
        sys.exit(1) # Zamykamy program z kodem błędu 1 (co oznacza awarię)



if __name__ == "__main__":
    main()