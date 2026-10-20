import csv
import random

def csv_write():
    with open('Dane.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')

        writer.writerow(['Model', ' Wynik', ' Czas', ' '])

        modelOptions = ['A', 'B', 'C']

        model = random.choice(modelOptions)
        wynik = f"{random.randint(0, 1000)}"
        czas = f"{random.randint(0, 1000)}s"

        writer.writerow([model, wynik, czas, ''])

def csv_read(file_name):
    total_time = 0
    with open(file_name, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if not row or len(row) < 3:
                continue

            model = row[0].strip()
            czas = row[2].strip()

            if model == 'A':
                total_time += int(czas[:-1])

    return total_time