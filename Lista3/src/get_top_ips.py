import read_log
def get_top_ips(log_list, n=10):
    """Function returns list with n most common client IP addresses """
    ip_counts = {} #slownik z adresami ip

    #zliczanie wystapien ip
    for tuple in log_list:
        ip = tuple[2]   #ip klienta
        if ip in ip_counts:
            ip_counts[ip] += 1
        else:
            ip_counts[ip] = 1

    sorted_ip_addresses = sorted(ip_counts.items(), key=lambda tuple: tuple[1], reverse=True) #sortowanie po wartosciach, items wyciaga krotki ('192.168.0.1",5) wiec bierzemy wartosc z indexu [1]

    return sorted_ip_addresses[:n]  #do n-tego elementu ale bez niego

def main():
    n = 5
    data = read_log.read_log()
    top_ip_addresses = get_top_ips(data, n)
    print(f"Ranking TOP {n} adresów IP:")
    for ip, count in top_ip_addresses:
        print(f"{ip}: {count} zapytań")

if __name__ == "__main__":
    main()