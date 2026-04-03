import os
import sys
import pathlib

#print(f"PATH = {os.environ['PATH']}") #Mozna podejrzec jak wyglada path

def __get_list_of_path_elements() -> list:
    """Private function - Returns list of folders in PATH"""
    splited_path: list = os.environ['PATH'].split(os.pathsep) #os.pathsep - automatycznie dostosowuje separator w zaleznosci od systemu
    return splited_path

def __get_unique_valid_folders(path_list: list) -> list:
    """Private function - Returns list of unique, existing directories from PATH"""
    unique_folders = set()
    
    for elem in path_list:
        path_obj = pathlib.Path(elem)
        if path_obj.is_dir():       #sprawdzenie czy istniejacy katalog
            unique_folders.add(elem)
            
    return list(unique_folders)

# def __get_list_of_path_folders(pathList: list) -> list:
#     """Private function - Returns list of folders in PATH"""
#     path_elements_occured_set: set = set()
#     for elem in pathList:
#         folders: tuple = pathlib.Path(elem).parts #krotka z podzielona sciezka na foldery
#         path_elements_occured_set.update(folders) #dodanie wszystkich elem z folders do seta
#     return list(path_elements_occured_set)

def __get_files_from_directory(directory_path: str) -> list:
    """Private function - Returns list of executable files in a given directory"""
    executable_files = []
    directory = pathlib.Path(directory_path)
    
    try:    #zabezpiczenie przed problemem z otwarcie problemu
        iterator = directory.iterdir()
    except PermissionError:
        print(f"[Ostrzeżenie: Brak uprawnień do wejścia do katalogu {directory}]", file=sys.stderr)
        return []
    
    for item in directory.iterdir():
        try:
           if item.is_file(): #sprawdzenie czy plik
                if os.name == 'nt': #sprawdzamy czy system Windows
                    if item.suffix.lower() in ['.exe', '.bat', '.cmd']:  #sprawddzenie czy wykonywalny zgodnie z windowsem
                        executable_files.append(item.name)
                else:   #sprawdzenie czy (Linux, macOS)
                    if os.access(item, os.X_OK): #sprawdzenie czy wykonywalny zgodnie z linux/macos
                        executable_files.append(item.name)
           
        except PermissionError:
            print(f"[Ostrzeżenie: Nie udalo sie odczytac pliku {item.name}]", file=sys.stderr)

    return executable_files
        

def print_folders_and_files(folders_list: list) -> None:
    """Function to print all folders and their executable files"""
    folders_list.sort()
    for folder in folders_list:
        print(folder)
        
        files_in_folder = __get_files_from_directory(folder)
        files_in_folder.sort()
        for file in files_in_folder:
            print("- ", file)


def print_sorted_folders(folders_list: list) -> None:
    folders_list.sort()
    for folder in folders_list:
        print(folder)
    



def path_operator() -> None:
    """Function handling parameters and logic of printing path elements"""
    path_list: list = __get_list_of_path_elements()
    path_folders: list = __get_unique_valid_folders(path_list)
    
    if len(sys.argv) < 2:
        print("Choose FLAG: \n'--folders' to print all folders in PATH \n'--all' to print files and folders in PATH")
        return #przerywamy działanie funkcji, jeśli nie ma argumentu
    
    if(sys.argv[1] == "--folders"):
        print_sorted_folders(path_folders)
    elif(sys.argv[1] == "--all"):
        print_folders_and_files(path_folders)  
    else:
        print(f"Unknown FLAG: {sys.argv[1]}\nChoose '--folders' or '--all'")




def main():
    path_operator()
    
if __name__ == "__main__":
  main()