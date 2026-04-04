import sys
from utils import mediacovert_utils
import subprocess
import pathlib
import shutil

ALLOWED_VIDEO_EXTENSIONS: set[str] = {'.mp4', '.mkv', '.avi', '.mov', '.mp3', '.wav', '.webm'} #zbior rozszerzen plikow ktore mozna konwertowac
ALLOWED_IMG_EXTENSIONS: set[str] = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff'}

def convert_media_files(input_dir_path: pathlib.Path, target_format: str) -> None:
    """Main function with converting logic"""
    
    if not input_dir_path.exists():
        raise FileNotFoundError(f"[Error] Path does not exist: {input_dir_path}")
    
    if not input_dir_path.is_dir():
        raise NotADirectoryError(f"[Error] This is not a directory: {input_dir_path}")
    
    target_dir = mediacovert_utils.get_converted_dir() #uzyskanie docelowego katalogu za pomoca pomocniczej funckji
    converted_counter = 0 #licznik konwertowanych plikow
    
    
    normalized_target = target_format if target_format.startswith('.') else f".{target_format}" #normalizacja rozszerzenia docelowego
    target_is_video = normalized_target.lower() in ALLOWED_VIDEO_EXTENSIONS
    target_is_img = normalized_target.lower() in ALLOWED_IMG_EXTENSIONS
    
    if not target_is_video and not target_is_img:   #zabezpieczenie przed zlym formatem
        raise ValueError(f"[Error] Unsupported target format: {target_format}")
    
    
    for object in input_dir_path.iterdir():
        if not object.is_file(): # sprawdzenie czy to plik          or object.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue
        
        #sprawdzenie czy to ktorys z obslugiwanych formatow i czy podany format koncowy tez jest zgodny, dostosowanie programu do wywolania
        if object.suffix.lower() in ALLOWED_VIDEO_EXTENSIONS and target_is_video:
            tool_name = 'ffmpeg'
        elif object.suffix.lower() in ALLOWED_IMG_EXTENSIONS and target_is_img:
            tool_name = "magick"
        else:
            continue
        
        print(f"Curr file: {object.name}")
        new_filename = mediacovert_utils.rename_output_file(object, target_format) #tworzenie nowej nazwy pliku
        output_path = target_dir / new_filename #tworzenie sciezki wyjsciowej 

        if object.suffix.lower() == normalized_target.lower(): #zabezpieczenie aby nie konwertowac na ten sam format np mp4 -> mp4, w tym przypadku po prostu kopiujemy
            shutil.copy2(object, output_path)   #kopiowanie pliku 
            mediacovert_utils.log_to_json(target_dir, object, target_format, output_path, "None (copied)")
            continue    #skopiowalismy to przechodzimy dalej aby nie konwertowac niepotrzebnie
        
        if tool_name == "ffmpeg":    
            #polecenie do subprocess
            command = ["ffmpeg", "-y", "-i", str(object), str(output_path)] #-y pozwaala nadpisywac plik pomijajac pytania programu
        else: #magick
            command = ["magick", str(object), str(output_path)]
        
            
        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) #check=True rzuci blad jesli bedzie wyjatek
            mediacovert_utils.log_to_json(target_dir, object, target_format, output_path, tool_name)   #Zapisujemy log jako json
            print(f"Success: Converted to {new_filename}")
            converted_counter+=1
            
        except subprocess.CalledProcessError:
            #wyjątek łapie sytuację, w której program zewnętrzny (FFmpeg) zakończył się błędem
            print(f"[Error] File {object.name} not converted.", file=sys.stderr)
        except FileNotFoundError:
             #wyjątek poleci, jeśli system w ogóle nie znajdzie zainstalowanego programu ffmpeg lub magick
             raise FileNotFoundError(f"[Error] Tool {tool_name} not found")
    
    print(f"\nDone. Converted files: {converted_counter}")
    
    
    
    

def main():    
    if len(sys.argv) < 3:
        print("Use: python mediaconvert.py <source_dir> <output_format>")
        print("Example1: python mediaconvert.py ./films avi")
        print("Example2: python mediaconvert.py ./images png")
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