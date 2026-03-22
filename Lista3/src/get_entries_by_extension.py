import read_log
def get_entries_by_extension(log_list, ext):
    """Function returns logs by extension"""

    if ext.startswith("."):    #Oczyszczanie podanego rozszerzenia z kropki jesli uzytkownik podal je z kropka
        cleaned_ext = ext[1:]    
    else:
        cleaned_ext = ext

    filtered_log = []

    for tuple in log_list:
        uri = tuple[8]

        cleaned_path = uri.split("?")[0]    #dzielimy uri na czesci i bierzemy czesc przed " ? "
        if cleaned_path.lower().endswith(f".{cleaned_ext.lower()}"):    #sprawdzamy czy konczy sie na .ext, uzywamy lower aby ujednolicic
            filtered_log.append(tuple)
    
    return filtered_log



def main():
    data = read_log.read_log()
    filtered_logs = get_entries_by_extension(data, ".jpg")
    for tuple in filtered_logs:
        print(tuple)


if __name__ == "__main__":
    main()