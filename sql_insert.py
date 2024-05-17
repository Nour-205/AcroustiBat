# Python built-in Packages
import csv
import json
import random
from datetime import datetime
from inspect import currentframe
# Package MySQL Connector >> pip install mysql-connector-python
import mysql.connector as mysql


def lire_fichier_csv(chemin_vers_fichier):

    print("")
    print(f"Lecture du fichier CSV: {chemin_vers_fichier}")

    nb_lignes = 0
    somme = 0.0

    with open(chemin_vers_fichier, 'r', encoding='utf-8') as fichier:
        reader = csv.reader(fichier, delimiter=';', quotechar='"')
        for ligne in reader:
            nb_lignes += 1
            print(f"ligne = {ligne}")
            numero = int(ligne[0]) 
            mesure = float(ligne[1]) 
            somme += mesure  # à compléter
            print(f"Le capteur n°{numero} a mesuré {mesure}")

    print(f"Nombre de Lignes: {nb_lignes}")
    moyenne = somme/nb_lignes  
    print(f"Moyenne: {moyenne:.2f}")



def ouvrir_connexion_bd():
    print("")
    print("***********************")
    print("** Connexion à la BD **")
    print("***********************")

    connexion_bd = None
    try:
        connexion_bd = mysql.connect(
                host="fimi-bd-srv1.insa-lyon.fr",
                port=3306,
                user="G221_D",     # à compléter
                password="G221_D",  
                database="G221_D_BD1"   # à compléter
            )
    except Exception as e:
        if type(e) == NameError and str(e).startswith("name 'mysql'"):
            print("[ERROR] MySQL: Driver 'mysql' not installed ? (Python Exception: " + str(e) + ")")
            print("[ERROR] MySQL:" +
                  " Package MySQL Connector should be installed [Terminal >> pip install mysql-connector-python ]" +
                  " and imported in the script [import mysql.connector as mysql]")
        else:
            print("[ERROR] MySQL: " + str(e))

    if connexion_bd is not None:
        print("=> Connexion établie...")
    else:
        print("=> Connexion échouée...")

    return connexion_bd


def fermer_connexion_bd(connexion_bd):
    print("")
    print("Fermeture de la Connexion à la BD")

    if connexion_bd is not None:
        try:
            connexion_bd.close()
            print("=> Connexion fermée...")
        except Exception as e:
            print("[ERROR] MySQL: "+str(e))
    else:
        print("=> pas de Connexion ouverte")


def ajouter_mesures_depuis_fichier_csv(connexion_bd, chemin_vers_fichier):
    with open(chemin_vers_fichier, 'r', encoding='utf-8') as fichier:
        reader = csv.reader(fichier, delimiter=';')
        for ligne in reader:
            numero = int(ligne[0]) 
            mesure = float(ligne[1])  # à compléter
            maintenant = datetime.now()
            ajouter_mesure(connexion_bd, numero, maintenant, mesure)   # à compléter


def ajouter_mesure(connexion_bd, id_mesure,id_serie, temp, humid, x, y):
    try:
        cursor = connexion_bd.cursor()
        cursor.execute("INSERT INTO MESURE  (IdMesure, IdSerie, temperature, humidite, positionX, positionY, dateMesure) VALUES (%s, %s, %s, %s, %s, %s, %s)", [ id_mesure, id_serie, temp, humid, x, y, datetime.now()])
        connexion_bd.commit()
    except Exception as e:
        print("MySQL [INSERTION ERROR]")
        print(e)

def check_lieu(connexion_bd, batiment, salle):
    cursor = connexion_bd.cursor()
    cursor.execute("SELECT IdLieu FROM LIEU WHERE nomBatiment = %s AND numeroSalle = %s", [batiment, salle])
    if cursor.fetchone() is not None:
        return True, cursor.fetchone()
    else:
        return False, None

    
def ajouter_lieu(connexion_bd, batiment, salle):
    # trouver id max 
    cursor1 = connexion_bd.cursor()
    cursor1.execute("SELECT MAX(IdLieu) FROM LIEU")
    id = cursor1.fetchone()[0]
    if id is None:
        id = 0
    cursor = connexion_bd.cursor()
    cursor.execute("INSERT INTO LIEU (IdLieu, nomBatiment, numeroSalle) VALUES (%s, %s, %s)", [id+1, batiment, salle])
    connexion_bd.commit()
    return id

def get_series_id(connexion_bd):
    cursor = connexion_bd.cursor()
    cursor.execute("SELECT MAX(IdSerie) FROM SERIE")
    id = cursor.fetchone()[0]
    if id is None:
        id = 0
    return id

def get_measurement_id(connexion_bd):
    cursor = connexion_bd.cursor()
    cursor.execute("SELECT MAX(IdMesure) FROM MESURE")
    id = cursor.fetchone()[0]
    if id is None:
        id = 0
    return id

def ajouter_serie(connexion_bd, id_serie, id_lieu):
    cursor = connexion_bd.cursor()
    cursor.execute("INSERT INTO SERIE (IdSerie, datejour,IdLieu ) VALUES (%s, %s, %s)", [id_serie, datetime.now(), id_lieu])
    connexion_bd.commit()

def ajouter_mesure_fft(connexion_bd, id_mesure, liste_frequence, liste_amplitude):
    for i in range(len(liste_frequence)):
        cursor = connexion_bd.cursor()
        cursor.execute("INSERT INTO COEFFICIENT (IdMesure, frequence, coefficient) VALUES (%s, %s, %s)", [id_mesure, liste_frequence[i], liste_amplitude[i]])
        connexion_bd.commit()

    




if __name__ == "__main__":
    bd = ouvrir_connexion_bd()




    fermer_connexion_bd(bd)
    print("=> Fin du Programme")

    

