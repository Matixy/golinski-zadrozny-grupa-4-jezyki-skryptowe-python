import read_log
import datetime
def get_entries_in_time_range(log_list, start, end):
    """Returns entries whose timestamp ts is in the range [start, end)"""
    filtered_log = []
    for tuple in log_list:
        ts = tuple[0]
        if start <= ts and ts < end:
            filtered_log.append(tuple)

    return filtered_log

def main():
    data_log_list = read_log.read_log()   
    start_date = datetime.datetime(2012, 3, 16, 15, 35, 11)
    end_date = datetime.datetime(2012, 3, 16, 15, 35, 12)
    filtered_log = get_entries_in_time_range(data_log_list, start_date, end_date)

    for tuple in filtered_log:
        print(tuple)


if __name__ == "__main__":
    main()