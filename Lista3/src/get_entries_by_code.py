import read_log
def get_entries_by_code(log_list, code):
    """Filtering funciton by HTTP code"""

    try:
        code_int = int(code)    #Sprawdzamy czy kod jest liczbą całkowitą
        if not (100 <= code_int <= 599):    #sprawdzamy, czy kod mieści się w zakresie kodow HTTP (100-599) 
            print(f"Błąd walidacji: {code_int} nie jest prawidłowym kodem HTTP.")
            return []
    except (ValueError, TypeError):
        print(f"Błąd walidacji: '{code}' nie jest poprawny.")
        return []

    filtered_log = []
    for tuple in log_list:
        if tuple[9] == code:
            filtered_log.append(tuple)
    
    return filtered_log


def main():
    data_log_list = read_log.read_log()    #Ograniczenie do wyswietlanai tylko 10 linii na potyrzeby testow
    filtered_log = get_entries_by_code(data_log_list, 404)

    for tuple in filtered_log:
        print(tuple)


if __name__ == "__main__":
    main()