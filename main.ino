/*
 * FIRMWARE CORRIGIDO: Mangaba-Xingo Sensor Node
 * PLATAFORMA: ESP32 (Ambiente Wokwi)
 * AUTOR: Equipe Arabian Nights (Hustler & Hackers)
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "DHTesp.h" // Biblioteca específica para ESP32 no Wokwi

// --- CREDENCIAIS DO SIMULADOR (Não altere isso no Wokwi) ---
const char* SSID_NAME = "Wokwi-GUEST"; 
const char* SSID_PASS = "";

// --- CONFIGURAÇÃO MQTT ---
const char* mqtt_server = "test.mosquitto.org";
const char* topic_sensor = "mangaba/sala/sensor";
const char* topic_control = "mangaba/sala/controle";

// --- PINAGEM (Hardware) ---
#define DHT_PIN 32    // Pino blindado (logicamente no simulador)
#define PIR_PIN 27    // Sensor de Presença
#define AC_LED_PIN 25 // Atuador (Lâmpada/LED)

// --- OBJETOS GLOBAIS ---
DHTesp dht; 
WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;

// --- SETUP DO WIFI ---
void setup_wifi() {
  delay(10);
  Serial.println("--------------------------------");
  Serial.print("📡 Iniciando: Conectando a ");
  Serial.println(SSID_NAME);
  
  WiFi.mode(WIFI_STA); 
  WiFi.begin(SSID_NAME, SSID_PASS);

  // Lógica de Timeout para não travar o boot eternamente
  unsigned long startAttemptTime = millis();
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    // Se demorar mais de 10s, tenta reiniciar a busca
    if (millis() - startAttemptTime > 10000) {
        Serial.println("\n❌ Timeout no WiFi. Tentando novamente...");
        WiFi.begin(SSID_NAME, SSID_PASS);
        startAttemptTime = millis();
    }
  }
  
  Serial.println("\n✅ WiFi Conectado!");
  Serial.print("📍 IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.println("--------------------------------");
}

// --- RECEBIMENTO DE MENSAGEM (CALLBACK) ---
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("📩 Mensagem recebida: ");
  
  String msg = "";
  for (int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }
  Serial.println(msg);

  // Controle de Atuadores
  if (msg == "ON") {
    digitalWrite(AC_LED_PIN, HIGH);
    Serial.println("💡 Luz LIGADA");
  } 
  else if (msg == "OFF") {
    digitalWrite(AC_LED_PIN, LOW);
    Serial.println("💡 Luz DESLIGADA");
  }
}

// --- RECONEXÃO MQTT ROBUSTA ---
void reconnect() {
  // Tenta conectar, mas se falhar, NÃO trava o loop principal
  if (!client.connected()) {
    Serial.print("🔌 Tentando MQTT... ");
    
    // ID Único para evitar colisão com outros grupos usando o mesmo servidor
    String clientId = "Mangaba-Node-";
    clientId += String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println("✅ Conectado!");
      client.subscribe(topic_control);
    } else {
      Serial.print("❌ Falha, rc=");
      Serial.print(client.state());
      Serial.println(" (tentará novamente no próximo ciclo)");
      // Não usamos delay() aqui para não travar o sensor
    }
  }
}

// --- SETUP PRINCIPAL ---
void setup() {
  Serial.begin(115200);
  
  pinMode(PIR_PIN, INPUT); // PIR geralmente não precisa de Pullup interno se for módulo
  pinMode(AC_LED_PIN, OUTPUT);
  
  // Inicialização específica da biblioteca DHTesp
  dht.setup(DHT_PIN, DHTesp::DHT22);
  Serial.println("⏳ Sensor DHT (ESPx) inicializado no Pino 32");
  
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

// --- LOOP PRINCIPAL ---
void loop() {
  // Verifica conexão MQTT (non-blocking)
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Timer não-bloqueante (executa a cada 3 segundos)
  unsigned long now = millis();
  if (now - lastMsg > 3000) { 
    lastMsg = now;

    // Leitura dos Sensores
    TempAndHumidity data = dht.getTempAndHumidity();
    bool movement = digitalRead(PIR_PIN); 

    // Validação de erro do sensor
    if (dht.getStatus() != 0) {
      Serial.println("⚠️ Erro de Leitura DHT: " + String(dht.getStatusString()));
      return; 
    }

    // Criação do JSON
    StaticJsonDocument<256> doc; 
    doc["movement"] = movement;
    doc["temperature"] = data.temperature;
    doc["humidity"] = data.humidity;
    
    char buffer[256];
    serializeJson(doc, buffer);
    
    // Envio
    if (client.connected()) {
        if (client.publish(topic_sensor, buffer)) {
            Serial.print("📤 Telemetry Sent: ");
            Serial.println(buffer);
        } else {
            Serial.println("❌ Falha no envio MQTT");
        }
    }
  }
}
