import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from ..database import db
from ..database.models import UserModel, StructureModel, SensorDataModel
from ...main import create_app

def seed_data():
    app = create_app()
    with app.app_context():
        print("Starting database seeding...")
        
        # Clean existing data
        db.session.query(SensorDataModel).delete()
        db.session.query(StructureModel).delete()
        db.session.query(UserModel).delete()
        db.session.commit()
        print("Cleared existing data.")

        # Create User
        if not UserModel.query.filter_by(email='engineer@aegis.com').first():
            hashed_password = generate_password_hash('password123', method='pbkdf2:sha256')
            user = UserModel(email='engineer@aegis.com', password_hash=hashed_password)
            db.session.add(user)
            print("Created user: engineer@aegis.com")

        # Create Structures
        structures_to_create = [
            {'name': 'Recife-Olinda Bridge', 'location': 'Recife, PE', 'status': 'Operational'},
            {'name': 'Boa Viagem Building A', 'location': 'Recife, PE', 'status': 'Warning'},
            {'name': 'Suape Port Viaduct', 'location': 'Ipojuca, PE', 'status': 'Critical'},
            {'name': 'Tacaruna Shopping Center Expansion', 'location': 'Recife, PE', 'status': 'Operational'},
        ]
        
        for s_data in structures_to_create:
            if not StructureModel.query.filter_by(name=s_data['name']).first():
                structure = StructureModel(**s_data)
                db.session.add(structure)
        
        db.session.commit()
        print(f"Created {len(structures_to_create)} structures.")

        # Create Sensor Data for each structure
        structures = StructureModel.query.all()
        sensor_types = ['Vibration', 'Strain', 'Temperature']
        now = datetime.utcnow()

        for structure in structures:
            for i in range(100): # 100 data points per structure
                for sensor in sensor_types:
                    value = 0
                    if sensor == 'Vibration': value = random.uniform(0.1, 2.5)
                    elif sensor == 'Strain': value = random.uniform(100, 500)
                    elif sensor == 'Temperature': value = random.uniform(20, 35)
                    
                    timestamp = now - timedelta(hours=100-i)
                    
                    data_point = SensorDataModel(
                        structure_id=structure.id,
                        sensor_type=sensor,
                        value=round(value, 4),
                        timestamp=timestamp
                    )
                    db.session.add(data_point)
        
        db.session.commit()
        print("Seeded sensor data.")
        print("Database seeding complete.")

if __name__ == '__main__':
    seed_data()
