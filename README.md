<div align="center">

# 🌵 Mangaba AI
### Soberania Energética & Inteligência IoT
**Projeto Arabian Nights | Hackathon Energy AI**

![Python](https://img.shields.io/badge/Brain-Python_3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![ESP32](https://img.shields.io/badge/Edge-ESP32-red?style=for-the-badge&logo=espressif&logoColor=white)
![MQTT](https://img.shields.io/badge/Protocol-MQTT-orange?style=for-the-badge&logo=mqtt&logoColor=white)
![Status](https://img.shields.io/badge/Status-MVP_Funcional-green?style=for-the-badge)

</div>

---

## 🧠 Sobre a Mangaba AI

> *"Transformando hardware legado em eficiência energética de ponta."*

O **Mangaba AI** é um sistema híbrido que desacopla a leitura de sensores da tomada de decisão. Diferente de sensores de presença comuns que desligam a luz quando você fica parado, nosso sistema utiliza **lógica fuzzy e persistência de dados** para garantir conforto térmico sem desperdício.

### 🎯 Pilares da Solução
* 🌡️ **Conforto:** Só liga o AC se houver gente **E** estiver quente.
* 💰 **Economia:** Desliga automaticamente em salas vazias.
* 🛠️ **Manutenção Preditiva:** Detecta se o AC está ligado mas não está gelando.

---

## ⚙️ Arquitetura do Sistema

Neste MVP, simulamos o ambiente físico na nuvem enquanto o processamento neural ocorre localmente.

```mermaid
graph LR
    subgraph Wokwi Cloud
    A[🌡️ DHT22 Sensor] -->|Leitura| B(📟 ESP32 Node)
    C[👀 PIR Movimento] -->|Detecção| B
    B -->|Atuação| D[💡 LED/Relé AC]
    end

    B <-->|MQTT Pub/Sub| E((☁️ Mosquitto Broker))

    subgraph Mangaba Hub
    E <-->|JSON Data| F[🧠 Python Script]
    end
````

### 💻 A Lógica do "Cérebro" (Python)

| Cenário | Condição | Ação | Resultado |
| :--- | :--- | :--- | :--- |
| **Economia** | Sala Vazia + Quente | `OFF` (Mantém desligado) | Zero desperdício de energia. |
| **Conforto** | Presença + Quente (\>24°C) | `ON` (Liga AC) | Conforto imediato. |
| **Timeout** | Sala fica vazia por 15s | `OFF` (Desliga AC) | Economia automática. |
| **Alerta** | AC Ligado + Temp não cai | `ALERT` (Log de Erro) | Aviso de manutenção. |

-----

## 🚀 Guia de Reprodução (Como Rodar)

### 1\. O Cérebro (Seu Computador/Linux)

Este script atua como o servidor central. Ele deve rodar antes ou durante a simulação.

**Instale a dependência:**

```bash
pip install paho-mqtt
```

**Execute o Hub:**

```bash
python mangaba_ai_hub.py
```

*O terminal ficará aguardando: `🧠 Iniciando Mangaba AI...`*

-----

### 2\. O Hardware (Simulação Wokwi)

Para validar o hardware sem custos, usamos o simulador Wokwi.

**Passo A: Configurar Bibliotecas (`libraries.txt`)**
É crucial usar as bibliotecas corretas para o ESP32 virtual. Na aba `libraries.txt`, cole:

```text
PubSubClient
ArduinoJson
DHT sensor library for ESPx
```

**Passo B: Montar o Circuito (`diagram.json`)**
Substitua o conteúdo da aba `diagram.json` pelo arquivo disponível na pasta `/docs` deste projeto.
*Isso conecta automaticamente: DHT22 (Pino 32), PIR (Pino 27) e LED (Pino 25).*

**Passo C: Carregar Firmware (`sketch.ino`)**
Copie o código C++ fornecido para a aba principal. Verifique se as credenciais estão apontando para o gateway virtual:

```cpp
const char* SSID_NAME = "Wokwi-GUEST";
const char* SSID_PASS = "";
```

**Passo D: Rodar**
Clique no botão **Play (▶)** verde no Wokwi.

-----

## 🔄 Roteiro de Demonstração (Pitch)

Siga este fluxo para apresentar aos juízes:

1.  **Estado Inicial:** Mostre o terminal Python rodando e o Wokwi com o LED apagado.
      * *Narrativa:* "O sistema está monitorando, mas como a sala está vazia, o AC permanece desligado para economizar."
2.  **Ação 1 (Calor + Gente):**
      * No Wokwi, clique no DHT22 e suba a temperatura para **28°C**.
      * Clique no PIR e selecione "Simulate Motion".
      * *Resultado:* O terminal mostra `🔥 Calor + presença` e o **LED Vermelho acende**.
3.  **Ação 2 (Saída de Pessoas):**
      * Pare a simulação de movimento no PIR.
      * Aguarde 15 segundos (Timeout configurado).
      * *Resultado:* O terminal mostra `❄️ Sala vazia` e o **LED apaga**.

-----

## 📁 Estrutura de Arquivos

```bash
Mangaba-Project/
├── 📄 README.md           # Esta documentação
├── 🧠 mangaba_ai_hub.py   # Script Python (Cérebro)
├── ⚡ sketch.ino          # Firmware ESP32 C++
└── 🔌 diagram.json        # Arquitetura de Hardware Wokwi
```

-----

<div align="center">

**Equipe Arrocha Árabe**
*Rhuan Pablo • Gabriel Filipe • José Antônio • Ana Laylla • Daví Antonio*

<i>Desenvolvido com ❤️ no Hackathon Energy AI 2025<i>

<div>

```
```
