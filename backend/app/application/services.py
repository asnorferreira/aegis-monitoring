import datetime
import jwt
from typing import List, Optional
from werkzeug.security import check_password_hash, generate_password_hash
from ..domain.repositories import IUserRepository, IStructureRepository
from ..domain.models import Structure, SensorData
from ..config import Config

class AuthService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def authenticate(self, email, password) -> Optional[str]:
        user = self.user_repo.find_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            payload = {
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
                'iat': datetime.datetime.now(datetime.timezone.utc),
                'sub': user.id
            }
            return jwt.encode(
                payload,
                Config.JWT_SECRET_KEY,
                algorithm='HS256'
            )
        return None

class UserService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def create_user(self, email: str, password: str) -> Optional[User]:
        if self.user_repo.find_by_email(email):
            return None # User already exists
        
        hashed_password = generate_password_hash(password)
        new_user = User(id=None, email=email, password_hash=hashed_password)
        return self.user_repo.add(new_user)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.user_repo.find_by_id(user_id)

    def get_all_users(self) -> List[User]:
        return self.user_repo.find_all()

    def update_user(self, user_id: int, data: dict) -> Optional[User]:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            return None

        if 'email' in data:
            user.email = data['email']
        
        if 'password' in data and data['password']:
            user.password_hash = generate_password_hash(data['password'])
            
        return self.user_repo.update(user)

    def delete_user(self, user_id: int) -> bool:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            return False
            
        return self.user_repo.delete(user_id)
        
class StructureService:
    def __init__(self, structure_repo: IStructureRepository):
        self.structure_repo = structure_repo

    def get_all_structures(self) -> List[Structure]:
        return self.structure_repo.find_all()

    def get_structure_details(self, structure_id: int) -> Optional[Structure]:
        return self.structure_repo.find_by_id(structure_id)
    
    def get_all_sensor_data_for_structure(self, structure_id: int) -> List[SensorData]:
        return self.structure_repo.get_sensor_data(structure_id)
