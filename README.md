<div align="center">

# ❄️ Xingó Cold
### Sistema Inteligente de Gestão Energética
**Impulsionado por Mangaba AI 🧠**

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-C51A4A?style=for-the-badge&logo=Raspberry-Pi&logoColor=white)
![ESP32](https://img.shields.io/badge/Hardware-ESP32-red?style=for-the-badge&logo=espressif&logoColor=white)
![MQTT](https://img.shields.io/badge/Protocolo-MQTT-orange?style=for-the-badge&logo=mqtt&logoColor=white)

</div>

---

## 🧠 Sobre a Mangaba AI

> *"A inteligência que entende o ambiente para economizar energia de forma inteligente"*

**Mangaba AI** é o cérebro do sistema **Xingó Cold**, responsável por:
* 🎯 **Análise preditiva** de padrões de uso.
* 🌡️ **Monitoramento inteligente** de temperatura e ocupação.
* 💡 **Otimização em tempo real** do consumo energético.
* 📊 **Aprendizado contínuo** com dados dos sensores.

---

## ⚙️ Arquitetura do Sistema (Visão Final)



### 🎯 Objetivo do Produto Final
Sistema completo de gestão energética usando **Raspberry Pi 4/5** (ou Linux) como unidade de processamento na borda (*edge computing*), sensores ESP32 distribuídos, e a **Mangaba AI** tomando decisões inteligentes para otimizar o consumo do ar condicionado.

### 🔄 Arquitetura de Produção

```mermaid
graph LR
    A[📟 ESP32 Sensores] -->|MQTT| B(🦟 Broker MQTT)
    B -->|MQTT| C[🍓 Raspberry Pi / Linux]
    C -->|Comando| B
    B -->|Comando| A
    subgraph Dispositivo de Borda
    C
    end
````

> **💡 INFORMAÇÃO IMPORTANTE: Linux = Raspberry Pi**
>
> Rodar a Mangaba AI no Linux é **FUNCIONALMENTE IDÊNTICO** a rodar num Raspberry Pi real\!
>
>   * ✅ **Mesmo Sistema Operacional:** O Raspberry Pi OS é baseado em Debian Linux.
>   * ✅ **Mesmos Pacotes Python:** As bibliotecas são idênticas.
>   * ✅ **Mesmo Código:** O script roda em ambos sem modificações.
>   * ✅ **Portabilidade Total:** O que roda aqui, roda lá.

-----

## 🎭 Demo MVP (Simulação Atual para o Hackathon)

Para fins de demonstração, estamos simulando a arquitetura física:

| Componente | Função | Ferramenta Usada |
| :--- | :--- | :--- |
| **Microcontrolador** | Simula ESP32 e sensores | 🌐 **Wokwi** |
| **Sensores** | Detecção PIR, IR, mmWave | 📡 **Sensores Virtuais** |
| **Atuador** | Simula status do Ar Condicionado | 💡 **LED (Wokwi)** |
| **Comunicação** | Intermediário de mensagens | 🦟 **MQTT Broker Público** |
| **Cérebro (Edge)** | Processamento inteligente (Mangaba AI) | 🐧 **Notebook Linux** |

-----

## 📁 Estrutura do Projeto

```bash
xingo-cold-project/
├── 📄 README.md           # Documentação
├── 🔧 mangaba_ai_hub.py   # O Cérebro: Mangaba AI (Python)
├── ⚡ main.ino            # O Corpo: Código do ESP32 (Wokwi)
├── 🔌 diagram.json       # O Hardware: Diagrama do circuito (Wokwi)
└── 🛠️ secrets.h         # Configurações de Rede (Wokwi)
```

-----

## 🚀 TUTORIAL RÁPIDO: Como Rodar

### 🐧 Para Usuários Linux (Recomendado\!)

1.  **Instale Python e dependências:**

    ```bash
    sudo apt update && sudo apt install python3 python3-pip
    pip3 install paho-mqtt
    ```

2.  **Execute a Mangaba AI:**

    ```bash
    python3 mangaba_ai_hub.py
    ```

### 🪟 Para Usuários Windows

1.  Instale o Python do [python.org](https://python.org).
2.  Instale a biblioteca: `pip install paho-mqtt`
3.  Execute: `python mangaba_ai_hub.py`


### 🔌 Configurar ESP32 no Wokwi (Passo a Passo)

Para rodar a simulação na nuvem, precisamos configurar o ambiente virtual.

1.  **Crie um novo projeto:**
    Acesse [Wokwi ESP32 Starter](https://wokwi.com/projects/new/esp32) para abrir um projeto em branco.

2.  **Instale as Bibliotecas (Essencial):**
    No editor do Wokwi, clique na aba **`Library Manager`** (ou crie um arquivo chamado `libraries.txt` clicando no **+**) e adicione o seguinte conteúdo:
    ```text
    PubSubClient
    ArduinoJson
    DHT sensor library
    ```
3.  **Configure o Hardware (`diagram.json`):**
    Clique na aba `diagram.json` e substitua todo o código pelo conteúdo do arquivo `diagram.json` deste repositório.
    *Isso montará automaticamente o ESP32, o Sensor DHT22, o Interruptor e o LED.*

4.  **Configure a Rede (`secrets.h`):**
    Clique na **▾** (seta ao lado de "Library Manager"), crie um novo arquivo chamado `secrets.h` e cole:
    ```cpp
    #define SECRET_SSID "Wokwi-GUEST"
    #define SECRET_PASS ""
    ```

5.  **Carregue o Código (`main.ino`):**
    Na aba principal `sketch.ino` (ou `main.ino`), apague tudo e cole o código C++ deste repositório.
    *Certifique-se de que a linha `mqtt_server` aponta para `"test.mosquitto.org"`.*

6.  **Rodar:**
    Clique no botão **Play (▶️)** verde.
-----

## 📡 Tópicos MQTT

| Tópico | Direção | Função |
| :--- | :--- | :--- |
| `mangaba/sala/sensor` | ESP32 → Mangaba AI | Envia dados de presença e temperatura |
| `mangaba/sala/controle` | Mangaba AI → ESP32 | Envia comandos (LIGAR/DESLIGAR) AC |

-----

## 🔄 Fluxo da Demonstração (Demo Day)

1.  **Iniciar:** Execute a Mangaba AI no Linux (`python3 mangaba_ai_hub.py`).
2.  **Wokwi:** Inicie a simulação no navegador.
3.  **Ação:** Clique nos sensores no Wokwi para simular presença.
4.  **Reação em Cadeia:**
      * ✅ ESP32 detecta movimento.
      * ✅ Envia dados via MQTT.
      * ✅ **Mangaba AI** processa (temperatura + histórico).
      * ✅ Envia comando de volta.
      * ✅ **LED acende** (Ar Condicionado LIGADO).
5.  **Economia Inteligente:**
      * ⏰ Mangaba AI monitora inatividade.
      * 🧠 Decide desligar para economizar.
      * ✅ **LED apaga**.

-----

## 🎊 O que esperar no Terminal

```bash
🚀 Iniciando Mangaba AI no Linux (Equivalente Raspberry Pi)...
✅ Conectado ao Broker MQTT!
🎯 PIR: Presença detectada! | 🌡️ Temperatura: 31°C
🔥 Temperatura ALTA! Ligando ar condicionado via PIR...
💡 Comando ON enviado para o ESP32
```

-----

<div align="center">

**Xingó Cold & Mangaba AI**
*Hackathon Energy 2025*
</div>
