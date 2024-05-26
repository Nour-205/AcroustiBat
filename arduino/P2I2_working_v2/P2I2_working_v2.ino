#include "Adafruit_Si7021.h"
#include "Ultrasonic.h"
#include "arduinoFFT.h"

#include <PubSubClient.h>
#include <WiFi.h>

/*-----AUDIO SETUP-----*/
#define AUDIO_CHANNEL A0

const uint16_t samples = 8192; //This value MUST ALWAYS be a power of 2
const float samplingFrequency = 44100; //Hz, must be less than 10000 due to ADC
unsigned int sampling_period_us;
unsigned long microseconds;

float vReal[samples];
float vImag[samples];

ArduinoFFT<float> FFT = ArduinoFFT<float>(vReal, vImag, samples, samplingFrequency, true);
/*-----DONE-----*/

/*-----ULTRASONIC SETUP-----*/
Ultrasonic ultrasonic(25);
bool enableHeater = false;
/*-----DONE-----*/

/*-----TEMP & HUMIDITY SETUP-----*/
#define I2C_SDA 32
#define I2C_SCL 33

Adafruit_Si7021 si7021_sensor;

float temp = 0;
float hum = 0;
float temps;
/*-----DONE-----*/

/*-----WIFI & MQTT-----*/
// WiFi
const char *ssid = "Nour"; // Enter your WiFi name
const char *password ="test1234";  // Enter WiFi password

// MQTT Broker
const char *mqtt_broker = "172.20.10.4";
const char *topic   = "my/test/channel";
const char *mqtt_username = "rickastley";
const char *mqtt_password = "password";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);
/*-----DONE-----*/


/*-----SETUP-----*/
void setup() {
  Serial.begin(115200);
  Serial.println("Test");
  
  if (!si7021_sensor.begin()) {
    Serial.println("Did not find Si7021 sensor!");
  }
  sampling_period_us = round(1000000*(1.0/samplingFrequency));

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
    Serial.println(WiFi.status());
    Serial.println(WL_CONNECTED);
  }
  
   client.setServer(mqtt_broker, mqtt_port);
   client.setCallback(callback);
   while (!client.connected()) {
       String client_id = "esp32-client-";
       client_id += String(WiFi.macAddress());
       Serial.printf("The client %s connects to the MQTT broker\n", client_id.c_str());
       if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
           Serial.println("Connected");
       } else {
           Serial.print("failed with state ");
           Serial.print(client.state());
           delay(2000);
       }
   }
   // Publish and subscribe
   client.publish(topic, "Hi, I'm ESP32 ^^");
   client.subscribe("rick/astley/measure");
   client.subscribe("rick/astley/frequency");
  
  Serial.println("Ready :D");
}
/*-----DONE-----*/

void callback(char *topic, byte *payload, unsigned int length) {
  String top = topic;
  if (top == "rick/astley/frequency") {
    sendFrequencies();
  }
  if (top == "rick/astley/measure") {
    measure();
  }
}

void measure() {
   /*-----ULTRASONIC-----*/
  long RangeInCentimeters;
  RangeInCentimeters = ultrasonic.read();
  Serial.print("Distance : ");
  Serial.println(RangeInCentimeters,DEC);
  char buffer[8]; // Adjust the buffer size according to your needs
  sprintf(buffer, "%d", RangeInCentimeters);
  client.publish("rick/astley/distance", buffer);
  /*-----DONE-----*/

  /*-----HUMIDITY & TEMPERATURE-----*/
  hum = float(si7021_sensor.readHumidity());
  temp = float(si7021_sensor.readTemperature());
  
  Serial.print("Humidité relative (en %) : ");
  Serial.println(hum, 2);
  
  char buffer1[8]; // Adjust the buffer size according to your needs
  snprintf(buffer1, sizeof(buffer1), "%.2f", hum);
  client.publish("rick/astley/humidity", buffer1);
  Serial.print("Température (en °C) : ");
  Serial.println(temp, 2);
  
  char buffer2[8]; // Adjust the buffer size according to your needs
  snprintf(buffer2, sizeof(buffer2), "%.2f", temp);
  client.publish("rick/astley/temperature", buffer2);
  //Serial.println(temp, 2);
  /*-----DONE-----*/

  /*-----AUDIO SAMPLING AND THINGS-----*/
  microseconds = micros();
  for(int i=0; i<samples; i++)
  {
      vReal[i] = analogRead(AUDIO_CHANNEL);
      vImag[i] = 0;
      while(micros() - microseconds < sampling_period_us){
        //empty loop
      }
      microseconds += sampling_period_us;
  }
  FFT.windowing(FFTWindow::Hamming, FFTDirection::Forward);  // Weigh data
  FFT.compute(FFTDirection::Forward); // Compute FFT 
  FFT.complexToMagnitude(); // Compute magnitudes
  Serial.println("Computed magnitudes");
  sendData(vReal, (samples >> 1));
  /*-----DONE-----*/
}

/*-----DATA SENDING FUNCTIONS-----*/
void sendData(float *vData, uint16_t bufferSize){
    for (uint16_t i = 0; i < bufferSize; i++){
      float abscissa;
      abscissa = ((i * 1.0 * samplingFrequency) / samples);
      char buffer[50]; // Adjust the buffer size according to your needs
      snprintf(buffer, sizeof(buffer), "%.4f", vData[i]);
      client.publish("rick/astley/fft", buffer);
    }
    client.publish("rick/astley/stop", "stop");
    Serial.println();
}

 void sendFrequencies(){
  Serial.println("Sending frequencies");
  for (uint16_t i = 0; i< (samples >> 1); i++) {
    float abscissa;
    abscissa = ((i * 1.0 * samplingFrequency) / samples);
    char buffer[50]; // Adjust the buffer size according to your needs
    snprintf(buffer, sizeof(buffer), "%.2f", abscissa);
    client.publish("rick/astley/frequencies", buffer);
  }
 }
 /*-----DONE-----*/

void loop() {
   client.loop();
}
