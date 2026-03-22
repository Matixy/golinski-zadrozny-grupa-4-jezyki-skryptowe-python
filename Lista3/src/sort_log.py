import sys
import read_log


def sort_log(log_list, index, is_reverse=False):
    """Sorting function. Sorts logs by tuple index. 
    Parameters: log_list (data), index (number of index that is a sorting key), is_reverse (default False, if True order will be reversed)
    Returns sorted list of tuples"""

    try:
        sorted_list = sorted(log_list, key=lambda tuple: tuple[index], reverse=is_reverse)
        return sorted_list

    except IndexError:  #blad gdy podany zly index
        print(f"Błąd: Niepoprawny indeks {index}.")
        return log_list #zwraca orginal aby nie przerwac pracy programu
    except TypeError: #błąd, gdy dane pod tym indeksem nie są porównywalne
        print(f"Błąd: Nie można sortować danych pod indeksem {index}.")
        return log_list
    
    

def main():
    data = read_log.read_log(10)
    sorted_data = sort_log(data, 1)

    for tuple in sorted_data:
        print(tuple)


if __name__ == "__main__":
    main()


