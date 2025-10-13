from abc import ABC, abstractmethod
from typing import List, Optional
from .models import User, Structure, SensorData

class IUserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def find_all(self) -> List[User]:
        pass

    @abstractmethod
    def add(self, user: User) -> User:
        pass
        
    @abstractmethod
    def update(self, user: User) -> Optional[User]:
        pass
        
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass

class IStructureRepository(ABC):
    @abstractmethod
    def find_all(self) -> List[Structure]:
        pass

    @abstractmethod
    def find_by_id(self, structure_id: int) -> Optional[Structure]:
        pass

    @abstractmethod
    def get_sensor_data(self, structure_id: int, sensor_type: Optional[str] = None) -> List[SensorData]:
        pass
