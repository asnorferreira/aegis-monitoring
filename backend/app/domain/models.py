from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class User:
    id: int
    email: str
    password_hash: str

@dataclass
class Structure:
    id: int
    name: str
    location: str
    status: str
    created_at: datetime
    updated_at: datetime

@dataclass
class SensorData:
    id: int
    structure_id: int
    sensor_type: str
    value: float
    timestamp: datetime
