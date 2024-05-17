import paho.mqtt.client as mqtt
from time import sleep

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



# Publish a message eveyr 2 seconds to the topic "my/test/topic"
i = 0
while True:
    i += 1
    client.publish(f"my/test/topic", "Hello, world!{i}")
    sleep(2)
    # run the loop
