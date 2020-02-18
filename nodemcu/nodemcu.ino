#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include "MAX30100_PulseOximeter.h"
#define REPORTING_PERIOD_MS     1000
PulseOximeter pox;
String testvar;
float Oxy, Hbeat,SHbeat, SOxy;
String msgs;
uint32_t tsLastReport = 0;
ESP8266WebServer server(80);

void setup() {

  Serial.begin(9600);
  WiFi.begin("CV.GLOBAL SOLUSINDO", "cvglobalsolusindo123456");  //Connect to the WiFi network

  while (WiFi.status() != WL_CONNECTED) {  //Wait for connection

    delay(500);
    Serial.println("Waiting to connect…");

  }
  Serial.print("Initializing pulse oximeter..");
  if (!pox.begin()) {
    Serial.println("FAILED");
    for (;;);
  } else {
    Serial.println("SUCCESS");
  }

  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());                         //Print the local IP of the webserver

  server.on("/Python", handlePath);            //Associate the handler function to the path
  server.begin();                                                   //Start the server
  Serial.println("Server listening");
  

  
}

void loop() {

  server.handleClient(); //Handling of incoming requests
  pox.update();
  if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
        Hbeat = pox.getHeartRate();
        Oxy = pox.getSpO2();
        Serial.print("Heart rate:");
        Serial.print(Hbeat);
        Serial.print("bpm / SpO2:");
        Serial.print(Oxy);
        Serial.println("%");
        msgs = String(Hbeat)+";"+ String(Oxy);
        tsLastReport = millis();
    }
    
    
}

void handlePath() { //Handler for the path
server.send(200, "text/plain", msgs);
delay(100);
}
