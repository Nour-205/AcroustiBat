import sql_insert
import csv
import json

db = sql_insert.ouvrir_connexion_bd()

# insert into frequency table the frequencies from the csv file
def insert_frequency_table():
    with open('frequencies.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        for line in reader: 
            for ch in line: 
                frequency = float(ch)
                int_freq = int(frequency)
                sql_insert.ajouter_mesure(db, int_freq)

 
def insert_frequency_table_from_json():
    with open('frequencies.json', 'r', encoding='utf-8') as file:
        list_freq = json.load(file)
        for freq in list_freq:
            sql_insert.ajouter_frequence(db, freq)
        
                


insert_frequency_table_from_json()


sql_insert.fermer_connexion_bd(db)
print("=> End of the program")
            