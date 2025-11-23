#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ================= CONFIGURAÇÃO =================
const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* mqtt_server = "test.mosquitto.org";

// ================= PINOS =================
const int PIR_PIN = 27;    
const int IR_PIN = 26;     // Emulando sensor IR
const int MMWAVE_PIN = 14; // Emulando sensor mmWave  
const int LED_PIN = 25;

// ================= TÓPICOS =================
const char* topic_sensor = "mangaba/sala/sensor";
const char* topic_control = "mangaba/sala/controle";

// ================= VARIÁVEIS =================
WiFiClient espClient;
PubSubClient client(espClient);

bool lastPirState = false;
bool lastIrState = false; 
bool lastMmwaveState = false;
bool ledState = false;

String sensorAtivo = "PIR"; // Pode alternar: "PIR", "IR", "MMWAVE"

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("📡 Conectando à ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  int timeout = 0;
  while (WiFi.status() != WL_CONNECTED && timeout < 20) {
    delay(500);
    Serial.print(".");
    timeout++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("");
    Serial.println("✅ WiFi conectado!");
  } else {
    Serial.println("❌ Falha na conexão WiFi");
  }
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("📨 Mensagem recebida [");
  Serial.print(topic);
  Serial.print("]: ");
  
  String messageTemp;
  for (int i = 0; i < length; i++) {
    messageTemp += (char)message[i];
  }
  Serial.println(messageTemp);

  if (String(topic) == topic_control) {
    if (messageTemp == "ON") {
      digitalWrite(LED_PIN, HIGH);
      ledState = true;
      Serial.println("💡 AR CONDICIONADO LIGADO");
    } else if (messageTemp == "OFF") {
      digitalWrite(LED_PIN, LOW);
      ledState = false;
      Serial.println("💡 AR CONDICIONADO DESLIGADO");
    }
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("🔄 Tentando conexão MQTT...");
    
    String clientId = "MangabaESP32-";
    clientId += String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println("✅ Conectado ao broker!");
      client.subscribe(topic_control);
    } else {
      Serial.print("❌ Falha, rc=");
      Serial.print(client.state());
      Serial.println(" tentando novamente em 5s...");
      delay(5000);
    }
  }
}

void enviarDadosSensor(String tipoSensor, bool movimento, float calor = 0, float confianca = 0, float distancia = 0) {
  DynamicJsonDocument doc(200);
  
  doc["sensor_type"] = tipoSensor;
  doc["movimento"] = movimento;
  doc["timestamp"] = millis();
  
  // Dados específicos por sensor
  if (tipoSensor == "IR") {
    doc["calor"] = calor;
  } else if (tipoSensor == "MMWAVE") {
    doc["confianca"] = confianca;
    doc["distancia"] = distancia;
  }
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  client.publish(topic_sensor, jsonString.c_str());
  
  Serial.print("📤 Dados ");
  Serial.print(tipoSensor);
  Serial.print(" enviados: ");
  Serial.println(jsonString);
}

void setup() {
  Serial.begin(115200);
  
  pinMode(PIR_PIN, INPUT);
  pinMode(IR_PIN, INPUT);
  pinMode(MMWAVE_PIN, INPUT); 
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  Serial.println("🚀 Iniciando Sistema Mangaba Multi-Sensor...");
  Serial.println("🎮 Sensores: PIR | IR | mmWave");
  
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Leitura dos sensores (simulados no Wokwi)
  bool pirState = digitalRead(PIR_PIN);
  bool irState = digitalRead(IR_PIN);
  bool mmwaveState = digitalRead(MMWAVE_PIN);
  
  // Detecção PIR
  if (pirState == HIGH && lastPirState == LOW) {
    Serial.println("🎯 PIR: Movimento detectado!");
    enviarDadosSensor("PIR", true);
  }
  
  // Detecção IR (emulando sensor de calor)
  if (irState == HIGH && lastIrState == LOW) {
    Serial.println("🎯 IR: Calor + movimento detectado!");
    float calorSimulado = random(30, 40); // Temperatura corporal
    enviarDadosSensor("IR", true, calorSimulado);
  }
  
  // Detecção mmWave (emulando sensor avançado)
  if (mmwaveState == HIGH && lastMmwaveState == LOW) {
    Serial.println("🎯 mmWave: Detecção avançada!");
    float confiancaSimulada = random(70, 95) / 100.0;
    float distanciaSimulada = random(10, 50) / 10.0;
    enviarDadosSensor("MMWAVE", true, 0, confiancaSimulada, distanciaSimulada);
  }
  
  lastPirState = pirState;
  lastIrState = irState;
  lastMmwaveState = mmwaveState;
  
  delay(100);
}
