import json
import random


def json_write(file_name='Dane.json'):
    data = {
        'Model': random.choice(['A', 'B', 'C']),
        'Wynik': random.randint(0, 1000),
        'Czas': f"{random.randint(0, 1000)}s",
    }

    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def json_read(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if data.get('Model') != 'A':
        return 0

    return int(str(data['Czas']).strip().removesuffix('s'))

