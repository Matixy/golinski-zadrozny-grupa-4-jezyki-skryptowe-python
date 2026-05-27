import datetime
from dataclasses import dataclass

@dataclass
class LogEntry:
    timestamp: datetime.datetime
    uid: str
    orig_h: str
    orig_p: int
    resp_h: str
    resp_p: int
    method: str
    host: str
    uri: str
    status: int
    user_agent: str
    resp_body_len: int
    resp_mime_types: str
    referrer: str


def read_log(filepath: str) -> list[LogEntry]:
    """Function reads from file. Return List of LogEntry objects which contains log data"""
    log_list = []    #Lista zwracana

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            cleaned_line = line.strip() #wyczyszczenie linii
            if cleaned_line == "":      #pominiecie jesli jest pusta
                continue

            list_from_line = cleaned_line.split("\t")   #rozdzielanie na podstawie tabulatora
            if len(list_from_line) != 27:    #sprawdzenie czy jest zgodna linia, zeby pominac bledne linie
                continue

            try:
                #konwersja typow
                ts= datetime.datetime.fromtimestamp(float(list_from_line[0]))
                orig_p = int(list_from_line[3])
                resp_p = int(list_from_line[5])
                status_code = int(list_from_line[14])
                
                body_len_str = list_from_line[13]
                
                user_agent = list_from_line[11].split(" ")[0] if list_from_line[11] != '-' else None
                resp_body_len = int(body_len_str) if body_len_str != '-' else 0
                resp_mime = list_from_line[26] if list_from_line[26] != '-' else None
                referrer = list_from_line[10] if list_from_line[10] != '-' else None

                #tworzenie obiektu
                entry = LogEntry(
                    timestamp = ts,
                    uid=list_from_line[1],
                    orig_h=list_from_line[2],
                    orig_p=orig_p,
                    resp_h=list_from_line[4],
                    resp_p=resp_p,
                    method=list_from_line[7],
                    host=list_from_line[8],
                    uri=list_from_line[9],
                    status=status_code,
                    user_agent= user_agent,
                    resp_body_len= resp_body_len,
                    resp_mime_types= resp_mime,
                    referrer= referrer 
                )
                log_list.append(entry)

            except (ValueError, IndexError):    #Zabezpieczenie przed bledami konwersji i indeksow
                continue
            
        print(log_list[11])
    return log_list 


def filter_logs_by_date(logs_list: list[LogEntry], start_date_str: str, end_date_str: str) -> list[LogEntry]:
    """Function filters logs by start and end dates"""
    start_date = None
    end_date = None

    #przegladarka wysylane w formacie ISO 2022-05-21T14:30:15 dlatego specjalna metoda fromisoformat()
    if start_date_str:
        start_date = datetime.datetime.fromisoformat(start_date_str)
    if end_date_str:
        end_date = datetime.datetime.fromisoformat(end_date_str)

    if not start_date and not end_date:
        return logs_list   
    
    filtered = []
    for log in logs_list:
        if start_date and log.timestamp < start_date:
            continue
        if end_date and log.timestamp > end_date:
            continue
        filtered.append(log)
    
    return filtered

