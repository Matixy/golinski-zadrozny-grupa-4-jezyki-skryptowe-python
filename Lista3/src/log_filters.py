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



def is_valid_ip(ip_addr):
    """Heper function for checking ip address validity in dot-decimal format"""
    addr_parts = ip_addr.split(".")
    if len(addr_parts) != 4:    #sprawedzamy czy skalda sie z 4 czesci
        return False
    for part in addr_parts:
        try:
            intVal = int(part)
            if intVal < 0 or intVal > 255:  #sprawdzamy czy w zakresie 0-255
                return False
        except ValueError:
            return False
        
    return True

def get_entries_by_addr(log_list, addr):
    """Filtering funciton by host address or host name"""
    addr_parts = addr.split('.')    #sprawdzanie czy to moze byc adres ip
    if len(addr_parts) == 4:
        if not is_valid_ip(addr):
            print(f"Błąd walidacji: '{addr}' nie jest poprawnym adresem IP.")
            return[]
        
    filtered_log_list = []
    for tuple in log_list:
        if tuple[2] == addr or tuple[7] == addr:
            filtered_log_list.append(tuple)
    
    return filtered_log_list




def main():
    data_log_list = read_log.read_log()    #Ograniczenie do wyswietlanai tylko 10 linii na potyrzeby testow
    filtered_log = get_entries_by_code(data_log_list, 404)
    filtered_log2 = get_entries_by_addr(data_log_list, "192.168.22.252")

    for tuple in filtered_log:
        print(tuple)

    print("\n \n ========================= \n \n")

    for tuple in filtered_log2:
        print(tuple)


if __name__ == "__main__":
    main()