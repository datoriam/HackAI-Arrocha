<div align="center">

# 🌡️ Projeto sem nome
### Sistema Inteligente de Gestão Energética

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![ESP32](https://img.shields.io/badge/Hardware-ESP32-red?style=for-the-badge&logo=espressif&logoColor=white)
![MQTT](https://img.shields.io/badge/Protocol-MQTT-orange?style=for-the-badge&logo=mqtt&logoColor=white)
![Status](https://img.shields.io/badge/Status-MVP%20Demo-success?style=for-the-badge)

</div>

---

## ⚙️ Arquitetura da Simulação (MVP Demo)

> **🎯 Objetivo da Demonstração**
> Simular o ciclo completo de detecção de movimento/presença via sensor IR no Wokwi (ESP32), envio de dados para o **"Mangaba AI Hub"** (notebook com Python), processamento inteligente por IA, e controle remoto de um "ar condicionado" (representado por LED).

---

## 🛠️ Componentes e Ferramentas

| Componente | Função |
| :--- | :--- |
| 🌐 **Wokwi** | Plataforma online de simulação de eletrônica |
| 📟 **ESP32 (Wokwi)** | Microcontrolador simulado |
| 📡 **Sensor PIR/IR** | Detecção de movimento/presença |
| 💡 **LED (Wokwi)** | Simula status do ar condicionado |
| 🦟 **Mosquitto MQTT** | Broker intermediário de comunicação |
| 🐍 **Python 3 + paho** | Processamento inteligente no "Mangaba AI Hub" |

---

## 🚀 Tutorial de Configuração

### 🦟 Passo 1: Configurar o Mosquitto MQTT Broker

O Broker MQTT é o "carteiro" que entrega as mensagens entre o ESP32 e o Python.

**Instalação:**

```bash
# 🐧 Linux (Debian/Ubuntu)
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto.service
sudo systemctl start mosquitto.service

# 🍎 macOS (via Homebrew)
brew install mosquitto
brew services start mosquitto

# 🪟 Windows: Baixe do site mosquitto.org



````

**Verificação:**
Abra dois terminais. No primeiro (para escutar):

```bash
mosquitto_sub -h localhost -t test/topic -v
```

No segundo (para enviar):

```bash
mosquitto_pub -h localhost -t test/topic -m "Hello Mosquitto!"
```

-----

### 🧠 Passo 2: Configurar o Mangaba AI Hub

Este script simula a inteligência artificial que processa os dados.

1.  **Instale a dependência:**

    ```bash
    pip install paho-mqtt
    ```

2.  **Configure o IP:**
    No arquivo `mangaba_ai_hub.py`, altere a linha:

    ```python
    MQTT_BROKER_HOST = "SEU_IP_DO_NOTEBOOK" # Ex: 192.168.1.15
    ```

    > ⚠️ **Importante:** Use o comando `ipconfig` (Windows) ou `ifconfig` (Linux/Mac) para descobrir seu IP local.

3.  **Execute o Hub:**

    ```bash
    python mangaba_ai_hub.py
    ```

-----

### 🔌 Passo 3: Configurar ESP32 no Wokwi

1.  Crie um projeto **ESP32** no [Wokwi](https://wokwi.com/).
2.  Monte o circuito conforme o `diagram.json` (PIR no GPIO 27, LED no GPIO 25).
3.  Copie o código do `main.ino` para o editor.

**Configurações Críticas no Wokwi:**

  * **IP do Broker:** No `main.ino`, atualize a variável `mqtt_server` com o **MESMO IP** usado no Python.
  * **Secrets:** Crie uma aba `secrets.h` no Wokwi com o seguinte conteúdo (obrigatório para simulação):
    ```cpp
    #define SECRET_SSID "Wokwi-GUEST"
    #define SECRET_PASS ""
    ```

-----

## 🔄 Fluxo da Demonstração (Demo Day)

1.  **Start:** Inicie o Mosquitto e rode o script Python (`mangaba_ai_hub.py`).
2.  **Wokwi:** Inicie a simulação. O ESP32 deve conectar ao WiFi e ao MQTT.
3.  **Ação:** Clique no sensor PIR no Wokwi (simula movimento).
4.  **Reação:**
      * ESP32 envia dados ao Hub.
      * Hub processa (Temp + Movimento).
      * Hub envia comando `ON`.
      * **LED acende** (Ar Condicionado LIGADO).
5.  **Economia:** Aguarde 15s sem interagir.
      * Hub detecta inatividade.
      * Hub envia comando `OFF`.
      * **LED apaga** (Economia de energia).

-----

## 🎯 Características da Demonstração

| Funcionalidade | Status | Observações |
| :--- | :---: | :--- |
| **Detecção de movimento** | ✅ Funcional | Sensor PIR simulado |
| **Processamento IA** | ✅ Básico | Lógica de temperatura + movimento |
| **Controle remoto** | ✅ Funcional | LED como simulador de AC |
| **Comunicação MQTT** | ✅ Estável | Broker local Mosquitto |

-----

## 📈 Próximas Evoluções

\<div align="left"\>

**🛠️ Expansões técnicas**

  - [ ] Integração com sensores reais (DHT22, PIR físico)
  - [ ] Dashboard web em tempo real
  - [ ] Algoritmos de ML para otimização preditiva
  - [ ] Múltiplas salas/zones

**💼 Oportunidades de negócio**

  - [ ] Escala para outras instituições (hospitais, indústrias)
  - [ ] Modelo SaaS com assinatura
  - [ ] Serviços de analytics preditivo
  - [ ] Integração com sistemas BMS existentes

\</div\>

-----

## 🏆 Reflexões do Hackathon

### 💪 Pontos Fortes

  * Arquitetura modular e escalável.
  * Protótipo funcional em ambiente simulado.
  * Potencial claro de economia energética.
  * Tecnologias acessíveis e documentadas.

### 🚧 Áreas de Evolução

  * Robustez em ambientes de produção.
  * Segurança (autenticação MQTT, criptografia).
  * Políticas mais complexas de controle.
  * Análise de dados históricos.

-----

## 🤝 Como Contribuir

Quer ajudar a melhorar o Mangaba AI? Siga os passos:

1.  🍴 Faça um **fork** do projeto
2.  🌿 Crie uma **branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3.  💻 Faça o **commit** das suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4.  🚀 Faça o **push** para a branch (`git push origin feature/AmazingFeature`)
5.  📬 Abra um **Pull Request**

-----

## 📄 Licença

Distribuído sob licença **MIT**. Veja `LICENSE` para mais informações.

-----

<div align="center">

**🔗 Links úteis**

[📚 Documentação Wokwi](https://docs.wokwi.com/) • [🦟 Mosquitto MQTT](https://mosquitto.org/) • [🐍 Paho-MQTT](https://pypi.org/project/paho-mqtt/)

</div>

```
```
