from typing import List, Optional
from ...domain.models import User, Structure, SensorData
from ...domain.repositories import IUserRepository, IStructureRepository
from ..database import db
from ..database.models import UserModel, StructureModel, SensorDataModel

class SQLUserRepository(IUserRepository):
    def find_by_email(self, email: str) -> Optional[User]:
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            return User(id=user_model.id, email=user_model.email, password_hash=user_model.password_hash)
        return None

    def add(self, user: User) -> User:
        # Note: This is a simplified add method. In a real app, password would be hashed here.
        new_user = UserModel(email=user.email, password_hash=user.password_hash)
        db.session.add(new_user)
        db.session.commit()
        return User(id=new_user.id, email=new_user.email, password_hash=new_user.password_hash)

class SQLStructureRepository(IStructureRepository):
    def find_all(self) -> List[Structure]:
        models = StructureModel.query.order_by(StructureModel.name).all()
        return [
            Structure(
                id=m.id, name=m.name, location=m.location, status=m.status,
                created_at=m.created_at, updated_at=m.updated_at
            ) for m in models
        ]

    def find_by_id(self, structure_id: int) -> Optional[Structure]:
        model = StructureModel.query.get(structure_id)
        if model:
            return Structure(
                id=model.id, name=model.name, location=model.location, status=model.status,
                created_at=model.created_at, updated_at=model.updated_at
            )
        return None
    
    def get_sensor_data(self, structure_id: int, sensor_type: Optional[str] = None) -> List[SensorData]:
        query = SensorDataModel.query.filter_by(structure_id=structure_id)
        if sensor_type:
            query = query.filter_by(sensor_type=sensor_type)
        
        models = query.order_by(SensorDataModel.timestamp.asc()).all()
        return [
            SensorData(
                id=m.id, structure_id=m.structure_id, sensor_type=m.sensor_type,
                value=m.value, timestamp=m.timestamp
            ) for m in models
        ]
