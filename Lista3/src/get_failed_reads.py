import read_log
def get_failed_reads(log_list, merge=False):
    """Function creates log list with 4xx and 5xx failures code. List can be merged into one if you set merge=True as a parameter"""
    error4_list = []
    error5_list = []

    for tuple in log_list:
        if tuple[9] >= 400 and tuple[9] <= 499:
            error4_list.append(tuple)
        elif tuple[9] >= 500 and tuple[9] <= 599:
            error5_list.append(tuple)

    if merge:
        return error4_list+error5_list
    else:
        return error4_list, error5_list


def main():
    data = read_log.read_log(500)

    listy_bledow = get_failed_reads(data)
    print(f"Liczba błędów 4xx: {len(listy_bledow[0])}")
    print(f"Liczba błędów 5xx: {len(listy_bledow[1])}")

    # Opcja 2: Pobieramy jedną wspólną listę
    wszystkie_bledy = get_failed_reads(data, merge=True)
    print(f"Suma wszystkich błędów: {len(wszystkie_bledy)}")


if __name__ == "__main__":
    main()
