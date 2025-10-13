import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações base da aplicação."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'uma-chave-secreta-padrao-muito-forte')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'uma-chave-jwt-secreta-padrao-muito-forte')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql+psycopg://user:password@db:5432/aegis_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações do MQTT (para a próxima etapa)
    MQTT_BROKER_URL = os.environ.get('MQTT_BROKER_URL')
    MQTT_BROKER_PORT = int(os.environ.get('MQTT_BROKER_PORT', 1883))
    MQTT_USERNAME = os.environ.get('MQTT_USERNAME')
    MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')
    MQTT_TLS_ENABLED = os.environ.get('MQTT_TLS_ENABLED', 'False').lower() in ('true', '1', 't')

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurações para produção."""
    DEBUG = False

# Mapeamento para selecionar a configuração correta
config_by_name = dict(
    development=DevelopmentConfig,
    production=ProductionConfig
)