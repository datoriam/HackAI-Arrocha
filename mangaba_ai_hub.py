import paho.mqtt.client as mqtt
import time
import random
import json
from enum import Enum

class SensorType(Enum):
    PIR = "PIR"
    IR = "IR" 
    MMWAVE = "mmWave"

# ================= CONFIGURAÇÃO =================
MQTT_BROKER_HOST = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC_SENSOR = "mangaba/sala/sensor"
MQTT_TOPIC_CONTROL = "mangaba/sala/controle"

# ================= ESTADO DO SISTEMA =================
ultimo_movimento = 0
ar_condicionado_ligado = False
temperatura_atual = 25
sensor_ativo = SensorType.PIR  # Pode alternar entre os sensores

# ================= DETECÇÃO INTELIGENTE MULTI-SENSOR =================
def detectar_presenca_inteligente(sensor_type, dados_sensor):
    """
    Emula diferentes comportamentos para cada tipo de sensor
    """
    if sensor_type == SensorType.PIR:
        # PIR: Detecção binária (movimento sim/não)
        return dados_sensor.get("movimento", False)
    
    elif sensor_type == SensorType.IR:
        # IR: Detecção por calor + movimento
        calor = dados_sensor.get("calor", 0)
        movimento = dados_sensor.get("movimento", False)
        return movimento and calor > 30  # Temperatura corporal aproximada
    
    elif sensor_type == SensorType.MMWAVE:
        # mmWave: Detecção avançada com confiança
        confianca = dados_sensor.get("confianca", 0)
        distancia = dados_sensor.get("distancia", 0)
        movimento = dados_sensor.get("movimento", False)
        
        # mmWave pode diferenciar humanos de objetos
        return movimento and confianca > 0.7 and 0.5 < distancia < 5.0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado ao MQTT Broker!")
        client.subscribe(MQTT_TOPIC_SENSOR)
        print(f"📡 Inscrito no tópico: {MQTT_TOPIC_SENSOR}")
        print("🎮 Sensores emulados: PIR | IR | mmWave")
    else:
        print(f"❌ Falha na conexão. Código: {rc}")

def on_message(client, userdata, msg):
    global ultimo_movimento, ar_condicionado_ligado, temperatura_atual, sensor_ativo
    
    try:
        payload = msg.payload.decode()
        print(f"📨 Mensagem recebida: {msg.topic} -> {payload}")
        
        if msg.topic == MQTT_TOPIC_SENSOR:
            # Processa dados baseado no tipo de sensor
            dados = json.loads(payload)
            sensor_type = SensorType(dados.get("sensor_type", "PIR"))
            
            # Detecção inteligente baseada no sensor
            presenca_detectada = detectar_presenca_inteligente(sensor_type, dados)
            
            if presenca_detectada:
                ultimo_movimento = time.time()
                temperatura_atual = random.randint(22, 35)
                
                print(f"🎯 {sensor_type.value}: Presença detectada!")
                print(f"🌡️ Temperatura: {temperatura_atual}°C")
                
                # Lógica de controle otimizada por sensor
                if temperatura_atual > 28 and not ar_condicionado_ligado:
                    print(f"🔥 Temperatura ALTA! Ligando ar condicionado via {sensor_type.value}...")
                    client.publish(MQTT_TOPIC_CONTROL, "ON")
                    ar_condicionado_ligado = True
                
    except Exception as e:
        print(f"❌ Erro ao processar mensagem: {e}")

# ================= SIMULAÇÃO AVANÇADA =================
def simular_dados_sensor(sensor_type):
    """
    Gera dados realistas para cada tipo de sensor
    """
    if sensor_type == SensorType.PIR:
        return {
            "sensor_type": "PIR",
            "movimento": random.choice([True, False]),
            "timestamp": time.time()
        }
    
    elif sensor_type == SensorType.IR:
        return {
            "sensor_type": "IR", 
            "movimento": random.choice([True, False]),
            "calor": random.randint(25, 40),  # Emula calor corporal
            "timestamp": time.time()
        }
    
    elif sensor_type == SensorType.MMWAVE:
        return {
            "sensor_type": "mmWave",
            "movimento": random.choice([True, False]),
            "confianca": round(random.uniform(0.1, 0.95), 2),  # Confiança da detecção
            "distancia": round(random.uniform(0.1, 10.0), 2),  # Distância em metros
            "timestamp": time.time()
        }

def main():
    global sensor_ativo
    
    print("🚀 Iniciando Mangaba AI Hub com Multi-Sensor...")
    print("🎮 Sensores disponíveis: PIR | IR | mmWave")
    print("💡 Modo: Emulação Avançada")
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER_HOST, MQTT_PORT, 60)
        client.loop_start()
        
        print("\n🔧 Controles do Sistema:")
        print("1. PIR - Detecção básica de movimento")
        print("2. IR - Detecção por calor + movimento") 
        print("3. mmWave - Detecção avançada com confiança")
        print("4. Auto - Alterna automaticamente entre sensores")
        print("\n⏳ Iniciando em modo AUTO em 5 segundos...")
        
        time.sleep(5)
        
        modo_auto = True
        ciclo_sensores = [SensorType.PIR, SensorType.IR, SensorType.MMWAVE]
        ciclo_index = 0
        
        while True:
            time.sleep(5)
            
            # Alterna entre sensores no modo auto
            if modo_auto:
                sensor_ativo = ciclo_sensores[ciclo_index]
                ciclo_index = (ciclo_index + 1) % len(ciclo_sensores)
                print(f"\n🔄 Alternando para sensor: {sensor_ativo.value}")
            
            # Simula envio de dados do sensor ativo
            dados_simulados = simular_dados_sensor(sensor_ativo)
            
            # Publica dados simulados (como se viessem do ESP32)
            client.publish(MQTT_TOPIC_SENSOR, json.dumps(dados_simulados))
            print(f"📤 Dados {sensor_ativo.value} simulados: {dados_simulados}")
            
            # Economia de energia
            tempo_inativo = time.time() - ultimo_movimento
            if ar_condicionado_ligado and tempo_inativo > 15:
                print(f"💤 Nenhuma presença detectada há {int(tempo_inativo)}s. Desligando...")
                client.publish(MQTT_TOPIC_CONTROL, "OFF")
                ar_condicionado_ligado = False
            
    except KeyboardInterrupt:
        print("\n🛑 Desligando Mangaba AI Hub...")
        client.publish(MQTT_TOPIC_CONTROL, "OFF")
        client.disconnect()

if __name__ == "__main__":
    main()
