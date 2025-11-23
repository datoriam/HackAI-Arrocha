import paho.mqtt.client as mqtt
import time
import json
import sys

# ================= CONFIGURAÇÕES =================
MQTT_BROKER_HOST = "test.mosquitto.org"
MQTT_BROKER_PORT = 1883
TOPIC_SENSOR = "mangaba/sala/sensor"
TOPIC_CONTROL = "mangaba/sala/controle"
TOPIC_ALERT = "mangaba/sala/alerta"   # tópico opcional para alertas

TEMP_LIMITE_CONFORTO = 24.0
TIMEOUT_DESLIGAR = 15   # segundos sem gente para desligar

# ================= MEMÓRIA =================
class Estado:
    def __init__(self):
        self.ultimo_movimento = 0.0
        self.ac_ligado = False

memoria = Estado()

# ================= LÓGICA PRINCIPAL =================
def processar_dados(dados):
    global memoria

    agora = time.time()
    movimento = bool(dados.get("movement", False))
    # Garantir conversão segura — se a chave não existir, usar 0.0
    try:
        temperatura = float(dados.get("temperature", 0.0))
    except (ValueError, TypeError):
        temperatura = 0.0
    try:
        umidade = float(dados.get("humidity", 0.0))
    except (ValueError, TypeError):
        umidade = 0.0

    print(f"📊 Recebido: Movimento={movimento} | Temp={temperatura:.1f}°C | Umid={umidade:.1f}%")

    if movimento:
        memoria.ultimo_movimento = agora
        print("👀 Presença detectada!")

    # REGRA A: LIGAR AC (tem gente + quente)
    if movimento and temperatura > TEMP_LIMITE_CONFORTO and not memoria.ac_ligado:
        print("🔥 Calor + presença → Ligando AC...")
        client.publish(TOPIC_CONTROL, "ON")
        memoria.ac_ligado = True
        return

    # REGRA B: DESLIGAR AC (vazio por TIMEOUT_DESLIGAR)
    tempo_sem_gente = agora - memoria.ultimo_movimento
    if memoria.ac_ligado and tempo_sem_gente > TIMEOUT_DESLIGAR:
        print(f"❄️ Sala vazia há {int(tempo_sem_gente)}s → Desligando AC.")
        client.publish(TOPIC_CONTROL, "OFF")
        memoria.ac_ligado = False
        return

    # REGRA C: ALERTA (AC ligado mas temperatura continua alta)
    if memoria.ac_ligado and temperatura > 29.0:
        msg = "AC_INEFICIENTE"
        print("⚠️ ALERTA: AC está ligado mas a sala continua quente! Publicando alerta.")
        client.publish(TOPIC_ALERT, msg)

# ================= CALLBACKS MQTT =================
def on_connect(client_obj, userdata, flags, rc):
    if rc == 0:
        print("✅ Mangaba AI conectada ao broker!")
        client_obj.subscribe(TOPIC_SENSOR)
    else:
        print(f"❌ Erro de conexão MQTT: rc={rc}")

def on_message(client_obj, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        dados = json.loads(payload)
        processar_dados(dados)
    except json.JSONDecodeError as e:
        print(f"❌ JSON inválido: {e} — payload: {msg.payload!r}")
    except Exception as e:
        print(f"❌ Erro ao processar mensagem: {e}")

def on_disconnect(client_obj, userdata, rc):
    print(f"🔌 Desconectado do broker (rc={rc}). Tentando reconectar...")

# ================= INICIALIZAÇÃO E LOOP =================
def main():
    global client
    print("🧠 Iniciando Mangaba AI...")

    # Criar client com callback_api_version nomeado (paho 2.x compat)
    client = mqtt.Client(
        client_id="Mangaba_Brain_PC",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION1
    )

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    # Conectar e entrar no loop
    try:
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, keepalive=60)
    except Exception as e:
        print(f"❌ Falha ao conectar ao broker: {e}")
        sys.exit(1)

    try:
        # loop_forever faz reconexão automática por padrão
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n✋ Interrompido pelo usuário. Saindo...")
    except Exception as e:
        print(f"❌ Loop MQTT interrompido: {e}")

if __name__ == "__main__":
    main()
