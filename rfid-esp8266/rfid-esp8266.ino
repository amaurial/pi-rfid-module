/*
Many thanks to nikxha from the ESP8266 forum
*/

#include <ESP8266WiFi.h>
#include <SPI.h>
#include <MFRC522.h>

/* wiring the MFRC522 to ESP8266 (ESP-12)
RST     = GPIO5
SDA(SS) = GPIO4 
MOSI    = GPIO13
MISO    = GPIO12
SCK     = GPIO14
GND     = GND
3.3V    = 3.3V
*/

#define RST_PIN  5  // RST-PIN für RC522 - RFID - SPI - Modul GPIO5 
#define SS_PIN  4  // SDA-PIN für RC522 - RFID - SPI - Modul GPIO4 
#define SERIAL 1

//const char *ssid =  "BRZHOME";     // change according to your Network - cannot be longer than 32 characters!
//const char *pass =  "Casabrasilis"; // change according to your Network
//const char* host = "192.168.1.100";

const char *ssid =  "canpiwi";     // change according to your Network - cannot be longer than 32 characters!
const char *pass =  ""; // change according to your Network
const char* host = "192.168.45.1";
const int port = 7777;
const int sensorid = 1;

byte buffer[50];
int msg_size = 0;
char t[20];

MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance
WiFiClient client;
boolean connected = false;

void setup() {
  pinMode(SS_PIN, OUTPUT);
  pinMode(RST_PIN, OUTPUT);
  
  #ifdef SERIAL
     Serial.begin(115200);    // Initialize serial communications
     delay(250);
     Serial.println(F("Booting...."));
  #endif
  
  SPI.begin();           // Init SPI bus
  
  mfrc522.PCD_Init();    // Init MFRC522
  mfrc522.PCD_DumpVersionToSerial();  // Show details of PCD - MFRC522 Card Reader details
  
  WiFi.begin(ssid, pass);
  
  int retries = 0;
  while ((WiFi.status() != WL_CONNECTED) && (retries < 10)) {
    retries++;
    delay(500);
    
    #ifdef SERIAL
      Serial.print(".");
    #endif
    
  }

  #ifdef SERIAL
    if (WiFi.status() == WL_CONNECTED) {
      Serial.println(F("WiFi connected"));
    }
    
    Serial.println(F("Ready!"));
    Serial.println(F("======================================================")); 
    Serial.println(F("Scan for Card and print UID:"));
  #endif

  connect();
  
}

void loop() { 
  boolean cardpresent = true;
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) {    
    cardpresent = false;

    #ifdef SERIAL
      //Serial.println("Card not present");
    #endif
    mfrc522.PCD_Init();    // Init MFRC522
    //mfrc522.PCD_DumpVersionToSerial();  // Show details of PCD - MFRC522 Card Reader details
  }
  else{
    cardpresent = true;
  }
    
  // Select one of the cards
  boolean cardread = false;
  if (cardpresent) {
    if ( ! mfrc522.PICC_ReadCardSerial()) {
      cardread = false;
    }
    else{
      cardread = true;
    }
  }
  // Show some details of the PICC (that is: the tag/card)
  if (cardread){
    msg_size = 0;    
   
    for (byte i = 0; i < mfrc522.uid.size; i++) {       
      buffer[i] = mfrc522.uid.uidByte[i];  
      msg_size ++;    
    }
    //memset(t,0,20);
    sprintf(t , "%d%d%d%d\n", buffer[0], buffer[1], buffer[2] ,buffer[3]);
    Serial.print(t);

    #ifdef SERIAL
      Serial.print(F("Card UID:"));
      dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size);
      Serial.println();  
    #endif

    
    if (!client.connected()){
      connect();
    }
    else{
      //for (byte i = 0; i < msg_size; i++) {
        //client.print(buffer[i]);
      //}
      client.print(String(sensorid) + ";" + String(t));
      //client.print('\n');
      while(client.available()){
          String line = client.readStringUntil('\r');
          #ifdef SERIAL 
          Serial.print(line);
          #endif
      }      
    }
       
  }  
}

// Helper routine to dump a byte array as hex values to Serial
void dump_byte_array(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}

void connect(){
  connected = client.connect(host , port);
  int retries = 0;
  while (!connected && retries < 10){
    #ifdef SERIAL
      Serial.println("Trying to connect to tcp server.");       
    #endif
    delay(200);
    connected = client.connect(host , port);  
    retries ++;  
  }
}
/*
 * if (client.connect(host, 80))
  {
    Serial.println("connected]");

    Serial.println("[Sending a request]");
    client.print(String("GET /") + " HTTP/1.1\r\n" +
                 "Host: " + host + "\r\n" +
                 "Connection: close\r\n" +
                 "\r\n"
                );

    Serial.println("[Response:]");
    while (client.connected())
    {
      if (client.available())
      {
        String line = client.readStringUntil('\n');
        Serial.println(line);
      }
    }
    client.stop();
    Serial.println("\n[Disconnected]");
  }
  else
  {
    Serial.println("connection failed!]");
    client.stop();
  }
  delay(5000);
}*/
 
