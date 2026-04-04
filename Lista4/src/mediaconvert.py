import sys
from utils import mediacovert_utils
import subprocess
import pathlib
import shutil

ALLOWED_EXTENSIONS: set[str] = {'.mp4', '.mkv', '.avi', '.mov', '.mp3', '.wav'} #zbior rozszerzen plikow ktore mozna konwertowac

def convert_media_files(input_dir_path: pathlib.Path, target_format: str) -> None:
    """Main function with converting logic"""
    
    if not input_dir_path.exists():
        raise FileNotFoundError(f"[Error] Path does not exist: {input_dir_path}")
    
    if not input_dir_path.is_dir():
        raise NotADirectoryError(f"[Error] This is not a directory: {input_dir_path}")
    
    target_dir = mediacovert_utils.get_converted_dir() #uzyskanie docelowego katalogu za pomoca pomocniczej funckji
    converted_counter = 0 #licznik konwertowanych plikow
    
    for object in input_dir_path.iterdir():
        if not object.is_file() or object.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue
        
        print(f"Curr file: {object.name}")
        new_filename = mediacovert_utils.rename_output_file(object, target_format) #tworzenie nowej nazwy pliku
        output_path = target_dir / new_filename #tworzenie sciezki wyjsciowej 

        
        normalized_target = target_format if target_format.startswith('.') else f".{target_format}" #normalizacja rozszerzenia docelowego
        if object.suffix.lower() == normalized_target.lower(): #zabezpieczenie aby nie konwertowac na ten sam format np mp4 -> mp4, w tym przypadku po prostu kopiujemy
            shutil.copy2(object, output_path)   #kopiowanie pliku 
            mediacovert_utils.log_to_json(target_dir, object, target_format, output_path)
            continue    #skopiowalismy to przechodzimy dalej aby nie konwertowac niepotrzebnie
        
        
        #polecenie do subprocess
        ffmpeg_command = ["ffmpeg", "-y", "-i", str(object), str(output_path)] #-y pozwaala nadpisywac plik pomijajac pytania programu
        
        try:
            subprocess.run(ffmpeg_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) #check=True rzuci blad jesli bedzie wyjatek
            mediacovert_utils.log_to_json(target_dir, object, target_format, output_path)   #Zapisujemy log jako json
            print(f"Success: Converted to {new_filename}")
            converted_counter+=1
            
        except subprocess.CalledProcessError:
            #wyjątek łapie sytuację, w której program zewnętrzny (FFmpeg) zakończył się błędem
            print(f"[Error] File {object.name} not converted.", file=sys.stderr)
        except FileNotFoundError:
             #wyjątek poleci, jeśli system w ogóle nie znajdzie zainstalowanego programu ffmpeg
             raise FileNotFoundError("[Error] FFmpeg not found")
    
    print(f"\nDone. Converted files: {converted_counter}")
    
    
    
    

def main():    
    if len(sys.argv) < 3:
        print("Use: python mediaconvert.py <source_dir> <output_format>")
        print("Example: python mediaconvert.py ./films avi")
        return
    
    input_dir = pathlib.Path(sys.argv[1])
    target_format = sys.argv[2]
    

    try:
        convert_media_files(input_dir, target_format)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(e, file=sys.stderr)
    except Exception as e:
        print(f"[Error] Something went wrong: {e}", file=sys.stderr)
        
        
        
        
if __name__ == "__main__":
    main()