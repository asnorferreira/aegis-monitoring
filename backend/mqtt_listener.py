import paho.mqtt.client as mqtt
import json
from datetime import datetime
import os
import ssl
from dotenv import load_dotenv
from app.main import create_app
from app.infrastructure.database import db
from app.infrastructure.database.models import SensorDataModel
load_dotenv()

MQTT_BROKER_URL = os.getenv("MQTT_BROKER_URL") or "localhost"
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 8883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TLS_ENABLED = os.getenv('MQTT_TLS_ENABLED', 'True').lower() in ('true', '1', 't')
MQTT_TOPIC_TO_SUBSCRIBE = "aegis/structures/+/sensors"

app = create_app()

def on_connect(client, userdata, flags, rc):
    """Callback executado ao conectar-se ao broker."""
    if rc == 0:
        print("✅ Listener conectado ao Broker MQTT!")
        client.subscribe(MQTT_TOPIC_TO_SUBSCRIBE)
        print(f"🎧 Inscrito no tópico: {MQTT_TOPIC_TO_SUBSCRIBE}")
    else:
        print(f"❌ Falha na conexão do Listener, código: {rc}\n")

def on_message(client, userdata, msg):
    """Callback executado ao receber uma mensagem."""
    try:
        topic_parts = msg.topic.split('/')
        if len(topic_parts) == 4 and topic_parts[0] == 'aegis' and topic_parts[3] == 'sensors':
            structure_id = int(topic_parts[2])
            payload = msg.payload.decode()
            data = json.loads(payload)

            print(f"📥 Mensagem recebida: {payload} para a estrutura ID {structure_id}")

            with app.app_context():
                new_sensor_data = SensorDataModel(
                    structure_id=structure_id,
                    sensor_type=data['sensor_type'],
                    value=data['value'],
                    timestamp=datetime.utcnow()
                )
                db.session.add(new_sensor_data)
                db.session.commit()
                print(f"💾 Dado salvo no banco de dados!")
        else:
            print(f"⚠️  Mensagem em tópico inesperado: {msg.topic}")

    except (json.JSONDecodeError, KeyError, IndexError, ValueError) as e:
        print(f"❌ Erro ao processar a mensagem: {e}")

def run_listener():
    """Inicia o cliente MQTT e começa a ouvir as mensagens."""
    if not all([MQTT_BROKER_URL, MQTT_USERNAME, MQTT_PASSWORD]):
        print("❌ Variáveis de ambiente MQTT não configuradas. Verifique seu arquivo .env")
        return

    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    
    if MQTT_TLS_ENABLED:
        client.tls_set(tls_version=ssl.PROTOCOL_TLS)
    
    try:
        client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT)
    except Exception as e:
        print(f"❌ Erro ao conectar no broker: {e}")
        return

    print("👂 Listener aguardando por mensagens...")
    client.loop_forever()

if __name__ == '__main__':
    run_listener()