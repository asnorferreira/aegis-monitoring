from . import db
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, email: str, password_hash: str, **kwargs): # <-- ADICIONE ESTE MÉTODO
        super().__init__(**kwargs)
        self.email = email
        self.password_hash = password_hash

class StructureModel(db.Model):
    __tablename__ = 'structures'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Operational')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sensor_data = db.relationship('SensorDataModel', backref='structure', lazy=True, cascade="all, delete-orphan")

class SensorDataModel(db.Model):
    __tablename__ = 'sensor_data'

    id: Mapped[int] = mapped_column(primary_key=True)
    structure_id: Mapped[int] = mapped_column(db.ForeignKey('structures.id'), nullable=False)
    sensor_type: Mapped[str] = mapped_column(db.String(50), nullable=False)
    value: Mapped[float] = mapped_column(db.Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, structure_id: int, sensor_type: str, value: float, timestamp: datetime):
        self.structure_id = structure_id
        self.sensor_type = sensor_type
        self.value = value
        self.timestamp = timestamp