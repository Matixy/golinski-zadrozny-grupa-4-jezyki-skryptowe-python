#Preambułę (zaczyna się na początku i kończy co najmniej dwoma pustymi wierszami, jesli 10 piewrszych linii nie konczy preambuly to znaczy ze takowej nie bylo)
#Informację o wydaniu (zaczyna się od linii mającej pięć myślników -----
import sys
import os
from src.utils.textTools import cleanLine, configureSysInOutUtf8
from src.utils.errorHandler import runFuncWithExceptionHandling

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
                raise ValueError("Błąd formatu: Nie znaleziono znaku końca książki (-----).") #Rzucamy blad gdy nie bedzie symbolu konca
            break


        if currChar == '\n':    #Jesli koniec lini to sprawdzamy co mamy w tej lini
            cleanedLine = cleanLine(currentLine)    #oczyszczenie obecnej linii za pomoca funkcji oczyszczajacej

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
                            outputFunction(cleanedLine)#print(cleanedLine)  #Wyswietlamy gotowa linie jestli to nie jest preambula
                    else:  #Jesli ksiazka juz wystartowala to sprawdzamy czy to nie ostatnie puste linie przed "-----", jesli tak to je ominiemy, jesli nie to wyswietlimy odpowiednia ilosc pominietych pustych wierszy aby zachowac spojnosc z akapitami
                        if cleanedLine == "":
                            orderedEmptyLinesCounter += 1
                        else:
                            while orderedEmptyLinesCounter > 0:
                                outputFunction("")      #print(cleanedLine)
                                orderedEmptyLinesCounter -= 1
                            outputFunction(cleanedLine) #print(cleanedLine)

                else:   #Jesli jestesmy nadal w Preambule
                    buffer += cleanedLine + '\n'    #Obsluga kontroli pierwszych 10 lniii w wypadku gdyby tekst nie zawieral preambuly
                    bufferLineCounter += 1

                    if emptyLineCounter >= 2:   #Sprawdzamy czy nadal w preambule
                        stillInPreambula = False
                        buffer = ""
                    elif bufferLineCounter >= 10:
                        stillInPreambula = False
                        bookTextStarted = True
                        outputFunction(buffer.strip("\n")) #wysylamy bufor ale bez ostatniego \n bo print go doda sam na koncu
                        buffer = ""

                currentLine = ""        #wyczyszczenie linii

        else:   #Jesli odczytany znak nie jest koncem linii dodajemy go do reszty
            currentLine += currChar



def main():
    """Główna funkcja programu sterujaca przekazywanym tekstem"""
    configureSysInOutUtf8() #ustawienie kodowania na utf-8

    extractTextFromBook(sys.stdin, print)   #Przekazujemy sys.stdin jako źródło i print jako funkcje odbierajaca dane
    sys.stdout.flush() #Wypychamy recznie dane aby wywolac blad BrokenPipe ktory zostanie zlapany przez except


if __name__ == "__main__":
    runFuncWithExceptionHandling(main)