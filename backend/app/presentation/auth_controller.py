from flask import Blueprint, request, jsonify
from flasgger import swag_from
from ..application.services import AuthService
from ..infrastructure.repositories.sql_repositories import SQLUserRepository

auth_bp = Blueprint('auth', __name__)
user_repo = SQLUserRepository()
auth_service = AuthService(user_repo)

@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Authenticate a user and get a JWT token.',
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'schema': {
                'type': 'object',
                'required': ['email', 'password'],
                'properties': {
                    'email': {'type': 'string', 'example': 'engineer@aegis.com'},
                    'password': {'type': 'string', 'example': 'password123'}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Authentication successful.',
            'schema': {
                'type': 'object',
                'properties': {
                    'token': {'type': 'string'}
                }
            }
        },
        '401': {'description': 'Invalid credentials.'}
    }
})
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    token = auth_service.authenticate(email, password)
    
    if token:
        return jsonify({'token': token})
    
    return jsonify({'message': 'Invalid credentials'}), 401
