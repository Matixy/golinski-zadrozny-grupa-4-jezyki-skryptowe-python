import read_log
def count_by_method(log_list):
    """Counts the occurrences of each HTTP method and returns a dictionary."""
    method_counts = {}

    for tuple in log_list:
        method = tuple[6] #w krotke na indexie 6 sa metody HTTP
        
        if method in method_counts: #jeśli metoda jest już w słowniku, zwiększamy licznik
            method_counts[method] += 1
        else:
            method_counts[method] = 1
            
    return method_counts


def main():
    data_log_list = read_log.read_log()  
    dict = count_by_method(data_log_list)

    for method, count in dict.items():
        print(method, " ", count)


if __name__ == "__main__":
    main()