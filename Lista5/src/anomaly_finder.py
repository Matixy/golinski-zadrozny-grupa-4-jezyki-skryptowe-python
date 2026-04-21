import datetime
from utils.logger_setup import logger
from enums.measurements_keys import MEASUREMENTS_KEYS
import csv_parser
from pathlib import Path

def find_anomalies(measurements: list) -> list:
    """Analyze measurements list, finds and returns detected anomalies"""

    if not measurements:
        return []

    anomalies = [] #return list

    ALARM_THRESHOLDS = {"PM10": 500.0}
    FAST_CHANGE_THRESHOLD = 100.0


    all_stations_data = {}
    for measurement in measurements:    #group measurements by station, make a list with measurements data for every station
        code = measurement[MEASUREMENTS_KEYS.STATION_CODE.value]
        if code not in all_stations_data:
            all_stations_data[code] = []
        all_stations_data[code].append(measurement)


    for station_code, measure_list in all_stations_data.items():
        measure_list.sort(key=lambda x: x[MEASUREMENTS_KEYS.DATE.value]) #sorted by date 
        prev_val = None
        zero_count = 0

        for m in measure_list:
            val = m[MEASUREMENTS_KEYS.VALUE.value]
            date = m[MEASUREMENTS_KEYS.DATE.value]
            pollutant = m[MEASUREMENTS_KEYS.POLLUTANT.value]
            frequency = m[MEASUREMENTS_KEYS.FREQUENCY.value]

            if val < 0:
                anomalies.append(f"STACJA {station_code}: [{date}] Wartość ujemna ({val}). Możliwa awaria czujnika.")

            if val == 0:    #count zero values in row
                zero_count += 1
            else:
                zero_count = 0 

            if zero_count >= 5:
                anomalies.append(f"STACJA {station_code}: [{date}] Wykryto serię wartości zerowych.")
                zero_count = 0

            #Value higher than alarm threshold 
            threshold = ALARM_THRESHOLDS.get(pollutant, 800.0)
            if val > threshold:
                anomalies.append(f"STACJA {station_code}: [{date}] Ekstremalnie wysoka wartość {val} (Próg: {threshold})")

            #Fast value jump in short time
            if prev_val is not None:
                delta = abs(val - prev_val)
                if delta > FAST_CHANGE_THRESHOLD:
                    anomalies.append(f"STACJA {station_code}: [{date}] Nagly skok wartości o {delta:.2f} względem poprzedniego pomiaru.")
            prev_val = val

    return anomalies

def main():
    measurement_path = Path("data") / "measurements" / "2023_As(PM10)_24g.csv" # pathlib take care off proper system path symbol
    res = csv_parser.parse_measurements(measurement_path)

    anomalie = find_anomalies(res)
    print(anomalie)


if __name__ == "__main__":
    main()