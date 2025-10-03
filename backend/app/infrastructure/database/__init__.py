from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instanciamos as extensões aqui, sem associar a nenhuma aplicação Flask ainda.
# Isso evita a importação circular.
db = SQLAlchemy()
migrate = Migrate()
