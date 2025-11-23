import paho.mqtt.client as mqtt
import time
import json

# --- Configurações MQTT ---
MQTT_BROKER_HOST = "test.mosquitto.org"
MQTT_BROKER_PORT = 1883
TOPIC_SENSOR_DATA = "mangaba/sala/sensor"
TOPIC_AC_CONTROL = "mangaba/sala/controle"

# --- Estado da Inteligência ---
class EstadoSala:
    def __init__(self):
        self.ac_virtual_status = "OFF"  # O que a Mangaba ACHOU que fez
        self.last_movement_time = 0
        self.current_temp = 25.0
        self.current_humid = 60.0
        self.target_temp = 23.0         # Meta de conforto

estado = EstadoSala()

# --- Constantes de Decisão ---
TIMEOUT_SEM_MOVIMENTO = 15  # Segundos para desligar (Demo)
TEMP_LIMITE_LIGAR = 26.0    # Se > 26°C e tem gente, liga
TEMP_ALERTA_FALHA = 28.0    # Se AC tá "ON" mas temp continua alta

def mangaba_ai_logic(dados):
    """
    Cérebro da Mangaba AI: Analisa sensores e infere estado real
    """
    global estado
    
    # 1. Atualiza percepção do ambiente
    movimento = dados.get("movement", False)
    estado.current_temp = dados.get("temperature", 25.0)
    estado.current_humid = dados.get("humidity", 60.0)
    agora = time.time()

    if movimento:
        estado.last_movement_time = agora
        print(f"👀 Movimento detectado! | Temp: {estado.current_temp}°C")

    # 2. Inferência de Estado (A sacada do Gabriel!)
    # Verifica se o AC está realmente funcionando
    if estado.ac_virtual_status == "ON" and estado.current_temp > TEMP_ALERTA_FALHA:
        print(f"⚠️ ALERTA: AC deveria estar ligado, mas sala está quente ({estado.current_temp}°C). Possível janela aberta!")

    # 3. Tomada de Decisão
    
    # REGRA A: Ligar AC (Conforto)
    # Se tem gente E (tá quente OU umidade alta) E AC tá desligado
    if movimento and (estado.current_temp >= TEMP_LIMITE_LIGAR) and estado.ac_virtual_status == "OFF":
        print(f"🔥 Sala ocupada e quente ({estado.current_temp}°C). Ligando AC...")
        client.publish(TOPIC_AC_CONTROL, "ON")
        estado.ac_virtual_status = "ON"
        return

    # REGRA B: Desligar AC (Economia)
    # Se não tem gente há X tempo E AC tá ligado
    tempo_ocioso = agora - estado.last_movement_time
    if estado.ac_virtual_status == "ON" and tempo_ocioso > TIMEOUT_SEM_MOVIMENTO:
        print(f"📉 Sala vazia por {int(tempo_ocioso)}s. Economizando energia...")
        client.publish(TOPIC_AC_CONTROL, "OFF")
        estado.ac_virtual_status = "OFF"
        return

# --- Callbacks MQTT ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Mangaba AI Conectada! Monitorando {TOPIC_SENSOR_DATA}...")
        client.subscribe(TOPIC_SENSOR_DATA)
    else:
        print(f"❌ Falha na conexão. Código: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        dados = json.loads(payload)
        mangaba_ai_logic(dados)
    except Exception as e:
        print(f"❌ Erro ao processar dados: {e}")

# --- Inicialização ---
print("🧠 Iniciando Mangaba AI Hub (com
