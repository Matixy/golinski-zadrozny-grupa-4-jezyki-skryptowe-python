import os
import pathlib
from datetime import datetime
import json
import sys

def get_converted_dir() -> pathlib.Path:
    """Returns the destination directory for converted files, creating it if necessary."""
    
    env_dir_location = os.environ.get("CONVERTED_DIR") #proba pobrania zmiennej srodowiskowej
    
    if env_dir_location:
        target_location = pathlib.Path(env_dir_location)
    else:
        target_location = pathlib.Path.cwd() / 'converted'  #w biezacym katalogu roboczym dodajemy folder 'converted'
        
    target_location.mkdir(exist_ok=True) #tworzymy katalog w podajen sciezce, nie wyrzuci bledu jesli juz istnial wczesniej
    
    return target_location


def rename_output_file(orginal_file: pathlib.Path, target_format: str) -> str:
    """Generates a timestamped filename, e.g., 20260404-video123.webm"""
    
    timestamp = datetime.now().strftime("%Y%m%d") #data w formacie RRRRMMDD
    orginal_name = orginal_file.stem #nazwa bez rozszerzenia
    
    if not target_format.startswith("."):
        target_format = f".{target_format}" #dodanie '.' na poczatku formatu np. mp4 -> .mp4
    
    res_filename = f"{timestamp}-{orginal_name}{target_format}"
    return res_filename



def log_to_json(target_path: pathlib.Path, orginal_path: pathlib.Path, output_format: str, output_path: pathlib.Path, tool_used: str) -> None:
    """Saves conversion history to a JSON file."""
    log_file = target_path / "history.json"
    history_data = []
    
    if log_file.exists():   #jesli plik istnieje to wczytujemy obecna zawartosc
        with open(log_file, mode='r', encoding='utf-8') as file:    #with open() .... automatycznie zamyka plik
            try:
                history_data = json.load(file)
            except json.JSONDecodeError:
                print(f"Blad: Plik {log_file} jest uszkodzony lub pusty.", file=sys.stderr)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_log = {
        "data i godzina": timestamp,
        "oryginalna sciezka": str(orginal_path),
        "format wyjsciowy": output_format,
        "sciezka_wynikowa": str(output_path),
        "program": tool_used
    }
    
    history_data.append(new_log) #dodanie nowego wpisu do danych
    
    with open(log_file, mode="w", encoding="utf-8") as file:
        json.dump(history_data, file, indent=4, ensure_ascii=False) #indent - ladnie formatuje tekst w pliku "4" to liczba spacji, ensure-ascii - zachowa polskie znaki
    
    




# def main():
#     print(datetime.now().strftime("%Y%m%d"))
#     print(rename_output_file(pathlib.Path("test.mp4"), "mp4"))
    

# if __name__ == "__main__":
#     main()
    