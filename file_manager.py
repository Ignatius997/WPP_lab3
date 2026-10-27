import os
import json_read_write
import csv_read_write


# Mapowanie wartości liczbowych z args.py na nazwy folderów
MONTHS_MAP = {
    1: "Styczen", 2: "Luty", 3: "Marzec", 4: "Kwiecien",
    5: "Maj", 6: "Czerwiec", 7: "Lipiec", 8: "Sierpien",
    9: "Wrzesien", 10: "Pazdziernik", 11: "Listopad", 12: "Grudzien"
}

DAYS_MAP = {
    1: "poniedzialek", 2: "wtorek", 3: "sroda", 
    4: "czwartek", 5: "piatek", 6: "sobota", 7: "niedziela"
}

TIMES_MAP = {1: "rano", 2: "wieczorem"}


def generate_paths(combinations: list[tuple[int, int, int]]) -> list[str]:

    # Generuje listę ścieżek na podstawie krotek zwróconych przez parser.
    paths = []
    for month_idx, day_idx, time_idx in combinations:
        month_name = MONTHS_MAP[month_idx]
        day_name = DAYS_MAP[day_idx]
        time_name = TIMES_MAP[time_idx]
        
        path = os.path.join(month_name, day_name, time_name)
        paths.append(path)
        
    return paths


def ensure_directories_exist(paths: list[str]):
    # Tworzy strukturę katalogów przed zapisem plików.
    for path in paths:
        os.makedirs(path, exist_ok=True)


def create_files(paths: list[str], file_format: str):
    # Tworzy pliki JSON lub CSV we wskazanych ścieżkach.
    ensure_directories_exist(paths)
    
    for path in paths:
        if file_format == 'json':
            file_path = os.path.join(path, 'Dane.json')
            json_read_write.json_write(file_path)
            
        elif file_format == 'csv':
            # csv_write() nie przyjmuje ścieżki, więc musimy tymczasowo zmienić folder roboczy
            original_dir = os.getcwd()
            os.chdir(path)
            try:
                csv_read_write.csv_write()
            finally:
                os.chdir(original_dir)
                
    print(f"[Sukces] Utworzono pliki {file_format.upper()} w {len(paths)} lokalizacjach.")


def read_files(paths: list[str], file_format: str) -> int:
    # Odczytuje pliki JSON lub CSV z podanych ścieżek i sumuje czas dla Modelu A.
    total_time = 0
    
    for path in paths:
        if file_format == 'json':
            file_path = os.path.join(path, 'Dane.json')
            if os.path.exists(file_path):
                total_time += json_read_write.json_read(file_path)
                
        elif file_format == 'csv':
            file_path = os.path.join(path, 'Dane.csv')
            if os.path.exists(file_path):
                total_time += csv_read_write.csv_read(file_path)
                
    print(f"\n[Wynik] Łączny czas dla Modelu 'A' ({file_format.upper()}): {total_time}s")
    return total_time
