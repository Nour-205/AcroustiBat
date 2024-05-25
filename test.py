import csv
import json 
import sql_insert

db = sql_insert.ouvrir_connexion_bd()

def insert_Lieu(db, batiment, salle):
    cursor = db.cursor()
    cursor.execute("INSERT INTO LIEU (nomBatiment, numeroSalle) VALUES ( %s, %s)", [batiment, salle])
    db.commit()
    cursor.close()

insert_Lieu(db, "B1", "1")

sql_insert.fermer_connexion_bd(db)