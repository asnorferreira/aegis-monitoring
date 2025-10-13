from typing import List, Optional
from sqlalchemy import asc
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
        new_user = UserModel(email=user.email, password_hash=user.password_hash)
        db.session.add(new_user)
        db.session.commit()
        return User(id=new_user.id, email=new_user.email, password_hash=new_user.password_hash)
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        user_model = UserModel.query.get(user_id)
        if user_model:
            return User(id=user_model.id, email=user_model.email, password_hash=user_model.password_hash)
        return None

    def find_all(self) -> List[User]:
        user_models = UserModel.query.all()
        return [
            User(id=m.id, email=m.email, password_hash=m.password_hash)
            for m in user_models
        ]

    def update(self, user: User) -> Optional[User]:
        user_model = UserModel.query.get(user.id)
        if user_model:
            user_model.email = user.email
            user_model.password_hash = user.password_hash
            db.session.commit()
            return user
        return None

    def delete(self, user_id: int) -> bool:
        user_model = UserModel.query.get(user_id)
        if user_model:
            db.session.delete(user_model)
            db.session.commit()
            return True
        return False

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
        
        models = query.order_by(asc(SensorDataModel.timestamp)).all()
        return [
            SensorData(
                id=m.id, structure_id=m.structure_id, sensor_type=m.sensor_type,
                value=m.value, timestamp=m.timestamp
            ) for m in models
        ]
