import paho.mqtt.client as mqtt
import time
import random
import json

# ================= CONFIGURAÇÃO =================
MQTT_BROKER_HOST = "test.mosquitto.org"  # Broker público para teste
MQTT_PORT = 1883
MQTT_TOPIC_SENSOR = "mangaba/sala/sensor"
MQTT_TOPIC_CONTROL = "mangaba/sala/controle"

# ================= ESTADO DO SISTEMA =================
ultimo_movimento = 0
ar_condicionado_ligado = False
temperatura_atual = 25

# ================= CALLBACKS MQTT =================
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado ao MQTT Broker!")
        client.subscribe(MQTT_TOPIC_SENSOR)
        print(f"📡 Inscrito no tópico: {MQTT_TOPIC_SENSOR}")
    else:
        print(f"❌ Falha na conexão. Código: {rc}")

def on_disconnect(client, userdata, rc):
    print("⚠️ Desconectado do MQTT. Tentando reconectar em 5s...")
    time.sleep(5)
    client.reconnect()

def on_message(client, userdata, msg):
    global ultimo_movimento, ar_condicionado_ligado, temperatura_atual
    
    try:
        print(f"📨 Mensagem recebida: {msg.topic} -> {msg.payload.decode()}")
        
        if msg.topic == MQTT_TOPIC_SENSOR:
            # Atualiza timestamp do último movimento
            ultimo_movimento = time.time()
            
            # Simula leitura de temperatura (22-35°C)
            temperatura_atual = random.randint(22, 35)
            
            print(f"🚶 Movimento detectado! | 🌡️ Temperatura: {temperatura_atual}°C")
            
            # LÓGICA INTELIGENTE DE CONTROLE
            if temperatura_atual > 28 and not ar_condicionado_ligado:
                print("🔥 Temperatura ALTA! Ligando ar condicionado...")
                client.publish(MQTT_TOPIC_CONTROL, "ON", qos=1)
                ar_condicionado_ligado = True
                print("💡 Comando ON enviado para o ESP32")
                
    except Exception as e:
        print(f"❌ Erro ao processar mensagem: {e}")

# ================= INICIALIZAÇÃO =================
def main():
    print("🚀 Iniciando Mangaba AI Hub...")
    print(f"🌐 Broker: {MQTT_BROKER_HOST}")
    print(f"📡 Tópico Sensor: {MQTT_TOPIC_SENSOR}")
    print(f"🎮 Tópico Controle: {MQTT_TOPIC_CONTROL}")
    
    # Configura cliente MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    # Last Will - Garante que o AC seja desligado se o hub cair
    client.will_set(MQTT_TOPIC_CONTROL, "OFF", qos=1, retain=True)
    
    try:
        print("🔌 Conectando ao broker MQTT...")
        client.connect(MQTT_BROKER_HOST, MQTT_PORT, 60)
        client.loop_start()
        
        print("🤖 Mangaba AI Hub ativo! Aguardando dados dos sensores...")
        print("💡 Dica: Clique no sensor PIR no Wokwi para simular movimento")
        
        # Loop principal para economia de energia
        while True:
            time.sleep(3)  # Verifica a cada 3 segundos
            
            # ECONOMIA DE ENERGIA: Desliga após 15s de inatividade
            tempo_inativo = time.time() - ultimo_movimento
            if ar_condicionado_ligado and tempo_inativo > 15:
                print(f"💤 Nenhum movimento há {int(tempo_inativo)}s. Desligando ar condicionado...")
                client.publish(MQTT_TOPIC_CONTROL, "OFF", qos=1)
                ar_condicionado_ligado = False
                print("💡 Comando OFF enviado para economia de energia")
                
            # Log de status a cada 10s
            if int(time.time()) % 10 == 0:
                status = "LIGADO" if ar_condicionado_ligado else "DESLIGADO"
                print(f"📊 Status: AC {status} | Temp: {temperatura_atual}°C | Inativo: {int(tempo_inativo)}s")
            
    except KeyboardInterrupt:
        print("\n🛑 Desligando Mangaba AI Hub...")
        client.publish(MQTT_TOPIC_CONTROL, "OFF", qos=1)
        client.disconnect()
        print("👋 Hub desligado com segurança!")
    except Exception as e:
        print(f"💥 Erro crítico: {e}")

if __name__ == "__main__":
    main()
