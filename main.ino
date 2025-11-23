#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "secrets.h"
#include <DHT.h>

// --- MUDANÇA AQUI: Vamos usar o Pino 4 ---
#define DHTPIN 4     
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// ... (Resto das configurações MQTT iguais) ...

void setup() {
  Serial.begin(115200);
  
  // Inicializa Hardware
  pinMode(PIR_PIN, INPUT);
  pinMode(AC_LED_PIN, OUTPUT);
  digitalWrite(AC_LED_PIN, LOW);

  // --- CORREÇÃO DO SENSOR ---
  // O DHT precisa de um "PullUp" (ajuda na leitura) e tempo para ligar
  // pinMode(DHTPIN, INPUT_PULLUP); // Opcional, a biblioteca geralmente cuida disso, mas mal não faz
  dht.begin(); 
  
  Serial.println("Aguardando o sensor DHT esquentar...");
  delay(2000); // <--- IMPORTANTE: Espera 2 segundos pro sensor acordar
  
  setup_wifi();
  // ... (Resto do setup igual) ...
}
// ... (Resto do código igual) ...
