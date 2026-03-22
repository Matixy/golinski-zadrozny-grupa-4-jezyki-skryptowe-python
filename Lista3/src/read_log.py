import sys
import datetime

def read_log(line_limit = -1):
    """Function reads from standard input. Return List of tuples with devided data 
    Parameters: By default line_limit = -1 which means that all input will be readed, change line_limit to read less lines"""

    log_tuples_list = []    #Lista zwracana
    line_counter = 0
    for line in sys.stdin:
        if line_limit != -1 and line_counter >= line_limit: #ograniczenie odnosnie czytania konkretnej ilosci linii z wejscia
            break

        cleaned_line = line.strip() #wyczyszczenie linii

        if cleaned_line == "":      #pominiecie jesli jest pusta
            continue

        list_from_line = cleaned_line.split("\t")   #rozdzielanie na podstawie tabulatora
        #print(list_from_line)

        if len(list_from_line) != 27:    #sprawdzenie czy jest zgodna linia, zeby pominac bledne linie
            continue

        try:
            #Konwersja typow
            timestamp = datetime.datetime.fromtimestamp(float(list_from_line[0]))
            orig_p = int(list_from_line[3])
            resp_p = int(list_from_line[5])
            status_code = int(list_from_line[14])


            currTuple = (timestamp, list_from_line[1], list_from_line[2], orig_p, list_from_line[4], resp_p, list_from_line[7], list_from_line[8], list_from_line[9], status_code) 
            log_tuples_list.append(currTuple)

            line_counter+=1

        except (ValueError, IndexError):    #Zabezpieczenie przed bledami konwersji i indeksow
            continue

    
    return log_tuples_list  #zwraca listy krotek



def main():
    data_log_list = read_log(10)    #Ograniczenie do wyswietlanai tylko 10 linii na potyrzeby testow
    for tuple in data_log_list:
        print(tuple)



if __name__ == "__main__":
    main()

