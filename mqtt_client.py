import paho.mqtt.client as mqtt
import csv
import sql_insert
import datetime
import json


    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print(f"Connection failed with error code {rc}")
# Create a client instance
client = mqtt.Client()

# Set the on_connect callback
client.on_connect = on_connect

# Connect to the Mosquitto broker
client.connect("localhost", 1883, 60)


# Subscribe to the topic "my/test/topic"

client.subscribe("rick/astley/measure")
client.subscribe("rick/astley/fft")
client.subscribe("rick/astley/distance")
client.subscribe("rick/astley/frequency")
client.subscribe("rick/astley/frequencies")
client.subscribe("rick/astley/humidity")
client.subscribe("rick/astley/temperature")
client.subscribe("rick/astley/stop")

#  establish connection with sql database

connexion_bd = sql_insert.ouvrir_connexion_bd()

serie = True
batiment = input("Enter the building of the measurement: ")
salle = input("Enter the room number: ")

#check if place in database
check, id_lieu = sql_insert.check_lieu(connexion_bd, batiment, salle)
print(id_lieu)

if check == False:
    sql_insert.ajouter_lieu(connexion_bd, batiment, salle)
    id_lieu = sql_insert.get_id_lieu(connexion_bd, batiment, salle)
    print(id_lieu)

#get series id max 
series_id = sql_insert.get_series_id(connexion_bd)

#insert series +1  into database
ask_series = input("Do you want to add a new series? (y/n) : ")

if ask_series == "y":
    sql_insert.ajouter_serie(connexion_bd, id_lieu)
    series_id += 1
else : 
    print("no series added")

x = 0 
y=[]
i =0 
while serie:
    client.connect("localhost", 1883, 60)
    # ask user if they want to continue the series
    continuer = input("Do you want to continue the series? (y/n) : ")
    if continuer == "n":
        serie = False
        print("series ended")
        client.disconnect()
        client.loop_stop()
        print("disconnected")
        break

    change_y = input("Do you want to change the value of y? (y/n) : ")
    if  change_y == "y":
        y.append(input("Enter the value of y: "))
        x = 0


    #get th id of the measurement
    measurement_id = sql_insert.get_measurement_id(connexion_bd)

    l = []
    #ask user if they want to send a message 
    humidity = []
    temperature = []
    distance = []
    fft_coef = []

    
    message = input("what do you want to do? (fft, freq, ect..) or press no :")

    if message == "fft":
        # send a message to measure topic to get the fft
        client.publish("rick/astley/measure", "get fft")
    elif message == "freq":
        client.publish("rick/astley/frequency", "freq")
    elif message == "no" :
        print("no message sent")
        client.disconnect()




    # recieve the message

    def on_message(client, userdata, message):
        print(f"Received message '{message.payload.decode()}' on topic '{message.topic}' with QoS {message.qos}")
        if message.topic == "rick/astley/stop":
            client.disconnect()
            print("disconnected")
        if message.topic == "rick/astley/humidity":
            humidity.append(float(message.payload.decode()))
        if message.topic == "rick/astley/temperature":
            temperature.append(float(message.payload.decode()))
        if message.topic == "rick/astley/distance":
            distance.append(float(message.payload.decode())) 
        if message.topic == "rick/astley/fft":
            fft_coef.append(int(float(message.payload.decode())))

    def frequency_list(client, userdata, message):
            if message.topic == "rick/astley/frequencies":
                l.append(message.payload.decode())
                #put in csv file 
                with open('frequencies.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(l)
            else :
                print("no message")



    # Set the on_message callback

    client.on_message = on_message


    #client.on_message = frequency_list

    # run the loop
    client.loop_forever()

    print(temperature, humidity, distance)

    x += distance[i]

    if temperature != [] and humidity != [] and distance != []:

        # insert distance/temperature/humidity into sql database and measurement id in the table

        sql_insert.ajouter_mesure(connexion_bd,series_id  ,temperature[i], humidity[i], x, y[i])


        # insert fft coefficients into sql database
        
        liste_frequence = json.load(open('frequencies.json', 'r'))

        sql_insert.ajouter_mesure_fft(connexion_bd, measurement_id + 1,liste_frequence, fft_coef)

        # close the connection with the database

          
        print("data inserted into database")
        continue 

    else: 
        print("no data received")
    i += 1

sql_insert.fermer_connexion_bd(connexion_bd) 









