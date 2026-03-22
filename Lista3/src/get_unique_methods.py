import read_log
def get_unique_methods(log_list):
    """Function returns unique list of all http methods names from logs"""
    unique_http_methods = set()
    for tuple in log_list:
        method = tuple[6]
        unique_http_methods.add(method)

    return list(unique_http_methods) #konwertujemy set na liste


def main():
    data = read_log.read_log()
    unique_methods = get_unique_methods(data)

    for method in unique_methods:
        print(method)


if __name__ == "__main__":
    main()
