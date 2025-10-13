import paho.mqtt.client as mqtt
import ssl
import time
import json
import random
import os
from dotenv import load_dotenv
load_dotenv()

MQTT_BROKER_URL = os.getenv("MQTT_BROKER_URL") or "localhost"
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TLS_ENABLED = os.getenv('MQTT_TLS_ENABLED', 'True').lower() in ('true', '1', 't')
STRUCTURE_IDS = [1, 2, 3, 4]

def on_connect(client, userdata, flags, rc):
    """Callback executado ao conectar-se ao broker."""
    if rc == 0:
        print("✅ Simulador conectado ao Broker MQTT com sucesso!")
    else:
        print(f"❌ Falha na conexão do simulador, código: {rc}\n")

def simulate_sensor_data():
    """Gera dados simulados para um sensor."""
    sensor_type = random.choice(['Vibration', 'Strain', 'Temperature'])
    value = 0
    if sensor_type == 'Vibration':
        value = random.uniform(0.1, 2.5)
    elif sensor_type == 'Strain':
        value = random.uniform(100, 500)
    elif sensor_type == 'Temperature':
        value = random.uniform(20, 35)
    
    return {"sensor_type": sensor_type, "value": round(value, 4)}

def run_simulator():
    """Inicia o cliente MQTT e começa a publicar dados."""
    if not all([MQTT_BROKER_URL, MQTT_USERNAME, MQTT_PASSWORD]):
        print("❌ Variáveis de ambiente MQTT não configuradas. Verifique seu arquivo .env")
        return

    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    
    if MQTT_TLS_ENABLED:
        client.tls_set(tls_version=ssl.PROTOCOL_TLS)
    
    try:
        client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT)
    except Exception as e:
        print(f"❌ Erro ao conectar no broker: {e}")
        return

    client.loop_start()
    print("🚀 Iniciando simulação de sensores...")
    
    try:
        while True:
            structure_id = random.choice(STRUCTURE_IDS)
            data = simulate_sensor_data()
            topic = f"aegis/structures/{structure_id}/sensors"
            payload = json.dumps(data)
            
            result = client.publish(topic, payload)
            if result[0] == 0:
                print(f"🛰️  Enviado `{payload}` para o tópico `{topic}`")
            else:
                print(f"⚠️  Falha ao enviar mensagem para o tópico {topic}")

            time.sleep(random.randint(3, 7))
    except KeyboardInterrupt:
        print("\n🛑 Simulação interrompida.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("🔌 Simulador desconectado.")

if __name__ == '__main__':
    run_simulator()