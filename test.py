import csv
import json 

l = []

def insert_frequency_table():
    with open('frequencies.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        for line in reader: 
            for ch in line: 
                frequency = float(ch)
                int_freq = int(frequency)
                l.append(int_freq)
    json.dump(l, open('frequencies.json', 'w'))

insert_frequency_table()