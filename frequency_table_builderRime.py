import csv
import json

import sql_insert

db = sql_insert.ouvrir_connexion_bd()

# insert into frequency table the frequencies from the csv file
def insert_frequency_table_from_json():
    with open('frequencies.json', 'r', encoding='utf-8') as file:
        list_freq = json.load(file)
    cursor = db.cursor()
    insert_data = [(freq,) for freq in list_freq]
    cursor.executemany("INSERT INTO FREQUENCE (frequence) VALUES (%s)", insert_data)
    db.commit()
    cursor.close()


 
def insert_frequency_table():
    with open('frequencies.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        frequencies = [int(float(ch)) for line in reader for ch in line]
    
    cursor = db.cursor()
    insert_data = [(freq,) for freq in frequencies]
    cursor.executemany("INSERT INTO FREQUENCE (frequence) VALUES (%s)", insert_data)
    db.commit()
    cursor.close()                


insert_frequency_table_from_json()


sql_insert.fermer_connexion_bd(db)
print("=> End of the program")
            