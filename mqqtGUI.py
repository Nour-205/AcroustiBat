import tkinter as tk
from tkinter import messagebox
import paho.mqtt.client as mqtt
import sql_insert
import json

class MQTTClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Client")

        self.client = mqtt.Client()

        self.liste_frequence = json.load(open('frequencies.json', 'r'))

        # UI Elements
        self.status_label = tk.Label(root, text="MQTT Status: Disconnected", fg="red")
        self.status_label.pack()

        self.db_status_label = tk.Label(root, text="DB Status: Not Connected", fg="red")
        self.db_status_label.pack()

        tk.Label(root, text="Building:").pack()
        self.building_entry = tk.Entry(root)
        self.building_entry.pack()

        tk.Label(root, text="Room:").pack()
        self.room_entry = tk.Entry(root)
        self.room_entry.pack()

        self.connect_button = tk.Button(root, text="Connect", command=self.connect)
        self.connect_button.pack()

        self.disconnect_button = tk.Button(root, text="Disconnect", command=self.disconnect)
        self.disconnect_button.pack()

        self.fft_button = tk.Button(root, text="Send FFT", command=self.send_fft)
        self.fft_button.pack()

        self.messages_text = tk.Text(root, state='disabled', height=10)
        self.messages_text.pack()

        # MQTT Callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.status_label.config(text="MQTT Status: Connected", fg="green")
            self.log_message("Connected to broker")
        else:
            self.status_label.config(text="MQTT Status: Connection Failed", fg="red")
            self.log_message(f"Connection failed with error code {rc}")

    def on_message(self, client, userdata, msg):
        self.log_message(f"Received message on {msg.topic}: {msg.payload.decode()}")
        self.handle_message(msg.topic, msg.payload.decode())

    def handle_message(self, topic, message):
        # Implement your message handling logic here
        # Example: Save message to database
        print(f"Handling message from topic {topic}: {message}")
        try:
            # Assuming `sql_insert` module has functions to handle the message
            # Example: sql_insert.process_message(topic, message)
            if topic == "rick/astley/fft":
                self.liste_coefficients.append(message.payload.decode())
            # Add other topic handlers as needed
            elif topic == "rick/astley/stop":
                self.serie = False
                sql_insert.ajouter_mesure(self.connexion_bd, self.id_mesure, self.series_id)
                sql_insert.ajouter_mesure_fft(self.connexion_bd, self.id_mesure, self.liste_frequence, self.liste_amplitude)
                self.log_message(f"Added measurement with ID: {self.id_mesure}")
                self.id_mesure += 1
        except Exception as e:
            self.log_message(f"Error handling message: {e}")

    def log_message(self, message):
        self.messages_text.config(state='normal')
        self.messages_text.insert(tk.END, message + "\n")
        self.messages_text.config(state='disabled')

    def connect(self):
        building = self.building_entry.get()
        room = self.room_entry.get()
        
        if not building or not room:
            messagebox.showwarning("Input Error", "Please enter both building and room")
            return

        # Connect to the MQTT broker
        self.client.connect("localhost", 1883, 60)
        self.client.loop_start()

        # Subscribe to topics
        self.client.subscribe("rick/astley/measure")
        self.client.subscribe("rick/astley/fft")
        self.client.subscribe("rick/astley/distance")
        self.client.subscribe("rick/astley/frequency")
        self.client.subscribe("rick/astley/frequencies")
        self.client.subscribe("rick/astley/humidity")
        self.client.subscribe("rick/astley/temperature")
        self.client.subscribe("rick/astley/stop")

        # Connect to the database
        try:
            self.connexion_bd = sql_insert.ouvrir_connexion_bd()
            self.db_status_label.config(text="DB Status: Connected", fg="green")
            self.log_message("Connected to database")

            # Check if place exists in database
            check, id_lieu = sql_insert.check_lieu(self.connexion_bd, building, room)
            if not check:
                sql_insert.ajouter_lieu(self.connexion_bd, building, room)
                id_lieu = sql_insert.get_id_lieu(self.connexion_bd, building, room)
            self.log_message(f"Location ID: {id_lieu}")

            # Get series ID
            self.series_id = sql_insert.get_series_id(self.connexion_bd) + 1

            ask_series = messagebox.askyesno("New Series", "Do you want to add a new series?")
            if ask_series:
                sql_insert.ajouter_serie(self.connexion_bd, id_lieu)
                self.log_message(f"New series added with ID: {self.series_id}")
            else:
                self.series_id -= 1  # Keep current series ID if not adding new

        except Exception as e:
            self.db_status_label.config(text="DB Status: Connection Failed", fg="red")
            self.log_message(f"Database connection failed: {e}")

        self.serie = True
        self.batiment = building
        self.salle = room

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        self.status_label.config(text="MQTT Status: Disconnected", fg="red")
        self.db_status_label.config(text="DB Status: Not Connected", fg="red")
        self.log_message("Disconnected from broker and database")

    def send_fft(self):
        self.liste_coefficients = []
        self.client.publish("rick/astley/measure", "get fft")
        self.log_message("Sent 'get fft' on channel 'measure'")

if __name__ == "__main__":
    root = tk.Tk()
    app = MQTTClientGUI(root)
    root.mainloop()
