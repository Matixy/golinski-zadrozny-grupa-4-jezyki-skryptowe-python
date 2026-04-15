import sys
import pathlib
import subprocess
import json
from collections import Counter

#sceizka do pliku jar
JAR_PATH = "src/java/textAnalyzer/target/textAnalyzer-1.0-SNAPSHOT-jar-with-dependencies.jar"


def analyze_single_file(file_path: pathlib.Path, jar_path: str) -> dict | None:
    """Runs java file analyzer for single file. Returns dict with Results or None if file is invalid"""
    java_command = ["java", "-jar", jar_path]
    
    try:
        result = subprocess.run(java_command, input=f"{file_path.resolve()}\n", capture_output=True, text=True, check=True) #.resolve daj sciezke absolutna do pliku
        java_output = result.stdout.strip()
        if java_output:
            return json.loads(java_output)     #zwracamy slownik   
    
    except subprocess.CalledProcessError:
        print(f"Skipped file: {file_path.name} not txt file or not accesible")
    except json.JSONDecodeError:
        print(f"Error with parsing to JSON {file_path.name}", file=sys.stderr)
        
    return None


def process_directory(input_dir: pathlib.Path, jar_path: str) -> list[dict]:
    """Search in directory, analyze files and collets results to list. Returns list with collected data"""
    results_list = []
    for file in input_dir.iterdir():
        if not file.is_file():
            continue
        
        stats = analyze_single_file(file, jar_path)
        if stats:
            results_list.append(stats)
            print(f"Succes. Analyzed {file.name}")
    
    return results_list


def print_summary(results_list: list[dict]) -> None:
    """Prints summary about collected data"""
    
    if not results_list:
        print("No data to summarise")
        return
    
    file_number = len(results_list)
    char_sum = sum(stat['chars'] for stat in results_list) #ze slownikow sumujemy wartosci dla kluczy
    words_sum = sum(stat['words'] for stat in results_list)
    row_sum = sum(stat['lines'] for stat in results_list)

    all_most_frequent_char = [stat['mostFrequentChar'] for stat in results_list if stat.get('mostFrequentChar')] #lista najczestszych znakow z plikow, if stat.get() pozwala zabezpieczyc przed wrzuceniem pustych wartosci
    all_most_frequent_words = [stat['mostFrequentWord'] for stat in results_list if stat.get('mostFrequentWord')]

    most_freq_char = Counter(all_most_frequent_char).most_common(1) #most_common(1) zwraca listę z jedną krotką, np [('a', 3)]
    most_freq_word = Counter(all_most_frequent_words).most_common(1)
    
    res_char = most_freq_char[0][0] if most_freq_char else "No data" #wyciagamy znak z krotki i go zwracamy
    res_word = most_freq_word[0][0] if most_freq_word else "No data"
    
    print("\n" + "=" * 50)
    print("          PODSUMOWANIE ANALIZY")
    print("=" * 50)
    print(f"Liczba przeczytanych plików:   {file_number}")
    print(f"Sumaryczna liczba znaków:      {char_sum}")
    print(f"Sumaryczna liczba słów:        {words_sum}")
    print(f"Sumaryczna liczba wierszy:     {row_sum}")
    print(f"Znak występujący najczęściej:  '{res_char}'")
    print(f"Słowo występujące najczęściej: '{res_word}'")
    print("=" * 50)


def main():
    """Main function runs the script"""
    if len(sys.argv) < 2:
        print("Use: python analyzer_runner.py <dir_path>")
        print("Example: python analyzer_runner.py ./data")
        sys.exit(1)

    input_dir = pathlib.Path(sys.argv[1])

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"[Error] Path '{input_dir}' is not a dir or does not exist", file=sys.stderr)
        sys.exit(1)

    lista_wynikow = process_directory(input_dir, JAR_PATH)
    # print("============")
    # print(lista_wynikow)
    # print("============")

    print_summary(lista_wynikow)
    

if __name__ == "__main__":
    main()