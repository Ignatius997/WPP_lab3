import csv
import random

def csv_write():
    with open('Dane.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['Model', 'Wynik', 'Czas'])

        modelOptions = ['A', 'B', 'C']

        model = random.choice(modelOptions)
        wynik = random.randint(0, 1000)
        czas = f"{random.randint(0, 1000)}s"

        writer.writerow([model, wynik, czas])

def csv_read(file_name):
    sum = 0
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            model = row[0]
            czas = row[2]
            if model == 'A':
                sum += int(czas[:-1])

    return sum