import sql_insert_ancien
import csv
import json

db = sql_insert_ancien.ouvrir_connexion_bd()

# insert into frequency table the frequencies from the csv file
def insert_frequency_table():
    with open('frequencies.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        for line in reader: 
            for ch in line: 
                frequency = float(ch)
                int_freq = int(frequency)
                sql_insert_ancien.ajouter_mesure(db, int_freq)

 
def insert_frequency_table_from_json():
    with open('frequencies.json', 'r', encoding='utf-8') as file:
        list_freq = json.load(file)
        print("loaded")
        cursor = db.cursor()
        for freq in list_freq:
            sql_insert_ancien.ajouter_frequence(cursor, db, freq)
        cursor.close()
        
                


insert_frequency_table_from_json()


sql_insert_ancien.fermer_connexion_bd(db)
print("=> End of the program")
            