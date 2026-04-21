import typer
from pathlib import Path
import random
import statistics
import csv_parser
from group_measurement_files_by_key import group_measurement_files_by_key
from enums.measurements_keys import MEASUREMENTS_KEYS
from enums.metadata_keys import METADATA_KEYS
from datetime import datetime


#inicjalizacja typera
app = typer.Typer(help="Narzędzie CLI (Wersja Typer)")

MEASUREMENTS_DIR = Path("./data/measurements")
STATIONS_FILE = Path("./data/stacje.csv")

#dozwolone wartosci potrzebne do walidacji
try:
    FILES = group_measurement_files_by_key(MEASUREMENTS_DIR)
    ALLOWED_POLLUTANTS = {k[1] for k in FILES.keys()}
    ALLOWED_FREQS = {k[2] for k in FILES.keys()}
except Exception: #zabezpieczenie gdyby nie bylo plikow
    ALLOWED_POLLUTANTS = set()
    ALLOWED_FREQS = set()



#Walidacja (data nie wymaga bo waliduje ja Typer)
def validate_pollutant(value: str):
    """Checks if inserted pollutant exist in pollutants"""
    if value not in ALLOWED_POLLUTANTS:
        raise typer.BadParameter(f"Nieprawidłowa wielkość: '{value}'. \nDozwolone: {', '.join(ALLOWED_POLLUTANTS)}")
    return value

def validate_frequency(value: str):
    """Checks if inserted frequency exist in frequencies"""
    if value not in ALLOWED_FREQS:
        raise typer.BadParameter(f"Nieprawidłowa częstotliwość: '{value}'. \nDozwolone: {', '.join(ALLOWED_FREQS)}")
    return value


def get_filtered_data(pollutant: str, frequency: str, start: datetime, end: datetime):
    """"Returns this measurements data rows bettwen start and end date"""
    year = str(start.year)
    path = FILES.get((year, pollutant, frequency))
    if not path:
        typer.echo(typer.style(f"BŁĄD: Brak danych dla roku {year} i parametrów {pollutant}/{frequency}", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    
    measurements = csv_parser.parse_measurements(path)
    filtered_measurements = []
    for measure in measurements:
        if start <= measure[MEASUREMENTS_KEYS.DATE.value] <= end:
            filtered_measurements.append(measure)

    if not filtered_measurements:
        typer.echo(typer.style("UWAGA: Brak pomiarów w wybranym zakresie dat.", fg=typer.colors.YELLOW))

    return filtered_measurements



#KOMENDY
@app.command()
def losowa_stacja(
    wielkosc: str = typer.Option(..., "--wielkosc", callback=validate_pollutant, help="Mierzona wielkosc"),
    czestotliwosc: str = typer.Option(..., "--czestotliwosc", callback=validate_frequency, help="Częstotliwosc"),
    start: datetime = typer.Option(..., "--start", formats=["%Y-%m-%d"], help="Początek (RRRR-MM-DD)"),
    koniec: datetime = typer.Option(..., "--koniec", formats=["%Y-%m-%d"], help="Koniec (RRRR-MM-DD)")
):
    """Prints random station name and address which measure inserted pollution and frequency"""

    data = get_filtered_data(wielkosc, czestotliwosc, start, koniec)
    if not data: 
        return

    #wybor losowego kodu stacji
    station_codes = set()
    for measurement in data:
        station_codes.add(measurement[MEASUREMENTS_KEYS.STATION_CODE.value])
    
    random_code = random.choice(list(station_codes))

    #pobieranie danych stajci
    stations_metadata = csv_parser.parse_metadata(STATIONS_FILE)
    station_info = stations_metadata.get(random_code)

    if station_info:
        typer.echo(typer.style(f"\nWYLOSOWANA STACJA", fg=typer.colors.CYAN, bold=True))
        typer.echo(f"Nazwa: {station_info.get(METADATA_KEYS.STATION_NAME.value)}")
        typer.echo(f"Adres: {station_info.get(METADATA_KEYS.ADDRESS.value)}")
    else:
        typer.echo(f"Kod stacji:{random_code} brak info w pliku stacje.csv")


@app.command()
def statystyki(
    station_code: str = typer.Argument(..., help="Kod stacji (np. DsBialka)"),
    wielkosc: str = typer.Option(..., "--wielkosc", callback=validate_pollutant),
    czestotliwosc: str = typer.Option(..., "--czestotliwosc", callback=validate_frequency),
    start: datetime = typer.Option(..., "--start", formats=["%Y-%m-%d"]),
    koniec: datetime = typer.Option(..., "--koniec", formats=["%Y-%m-%d"]),
):
    """Calculates mean and std dev for station"""

    data = get_filtered_data(wielkosc, czestotliwosc, start, koniec)

    #wyciaganie wartosci pomiarow dla danej stacji
    values = []
    for measurement in data:
        if measurement[MEASUREMENTS_KEYS.STATION_CODE.value] == station_code:
            values.append(measurement[MEASUREMENTS_KEYS.VALUE.value])

    if not values:
        typer.echo(typer.style(f"Błąd: Brak danych dla stacji {station_code} w tym zakresie.", fg=typer.colors.RED))
        return


    typer.echo(typer.style(f"\nSTATYSTYKI STACJI: {station_code}", fg=typer.colors.GREEN, bold=True))
    typer.echo(f"Liczba pomiarów: {len(values)}")
    typer.echo(f"Średnia: {statistics.mean(values):.3f}")

    if len(values) > 1:
        typer.echo(f"Odchylenie standardowe: {statistics.stdev(values):.3f}")
    else:
        typer.echo("Odchylenie standardowe: brak danych (wymagane min. 2 pomiary)")


#odpalenie aplikacji
if __name__ == "__main__":
    app()


# @app.command() - powoduje ze funkcja staje sie komenda w terminualu
# typer.Option() - powoduje ze to ma byc opcja np. --wielkosc i dziek temu wymagany jest zapis --wielkosc PM10
# typer.Option(... , ) - kropki powoduja ze to jest obowiazkowy/wymgany argument
# callback - uruchamia funckje przy wczytaniu argumentu, w tym przypadku funkcje walidujaca
# datetime - typer automatycnzie zamienia string na obiekt daty, wymuszamy akceptacje tylko format: 2024-01-30
# typer.Argument() - powoduje ze to musi byc argument, wtedy kolejnosc jest wazna, bez "--"

#Argparse: Wymagał klasy LoggingArgumentParser, ręcznego wyciągania parametrów z Namespace 
# przez getattr i lstrip oraz dlugiego systemu subparserów


#TESTY
#python src/cli_typer.py losowa-stacja --wielkosc PM10 --czestotliwosc 24g --start 2023-01-01 --koniec 2023-01-31

#python src/cli_typer.py statystyki DsJelGorSoko --wielkosc PM10 --czestotliwosc 24g --start 2023-01-01 --koniec 2023-01-31 

#python src/cli_typer.py --help 
