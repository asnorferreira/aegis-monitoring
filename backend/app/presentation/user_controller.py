from flask import Blueprint, request, jsonify
from .auth_decorator import token_required
from ..application.services import UserService
from ..infrastructure.repositories.sql_repositories import SQLUserRepository

user_blueprint = Blueprint('users', __name__, url_prefix='/api/users')

# --- Dependency Injection ---
# Em um projeto maior, usaríamos um container de injeção de dependência.
# Aqui, instanciamos diretamente para manter a simplicidade.
user_repository = SQLUserRepository()
user_service = UserService(user_repository)

@user_blueprint.route('/', methods=['POST'])
@token_required
def create_user(current_user):
    """
    Create a new user
    This endpoint allows an authenticated user to create a new user.
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: new.user@aegis.com
            password:
              type: string
              example: securePassword123
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
            email:
              type: string
      400:
        description: Invalid input or user already exists
      401:
        description: Token is missing or invalid
    """
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400

    new_user = user_service.create_user(data['email'], data['password'])
    
    if not new_user:
        return jsonify({'message': 'User with this email already exists'}), 400

    return jsonify({'id': new_user.id, 'email': new_user.email}), 201

@user_blueprint.route('/', methods=['GET'])
@token_required
def get_all_users(current_user):
    """
    Get all users
    This endpoint returns a list of all users.
    ---
    tags:
      - Users
    security:
      - Bearer: []
    responses:
      200:
        description: A list of users
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              email:
                type: string
      401:
        description: Token is missing or invalid
    """
    users = user_service.get_all_users()
    output = [{'id': user.id, 'email': user.email} for user in users]
    return jsonify(output), 200

@user_blueprint.route('/<int:user_id>', methods=['GET'])
@token_required
def get_user_by_id(current_user, user_id):
    """
    Get a single user by ID
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: User details
      404:
        description: User not found
      401:
        description: Token is missing or invalid
    """
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'id': user.id, 'email': user.email}), 200

@user_blueprint.route('/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    """
    Update a user's details
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
              description: "Optional. Only include if you want to change the password."
    responses:
      200:
        description: User updated successfully
      404:
        description: User not found
      401:
        description: Token is missing or invalid
    """
    data = request.get_json()
    updated_user = user_service.update_user(user_id, data)
    
    if not updated_user:
        return jsonify({'message': 'User not found'}), 404
        
    return jsonify({'id': updated_user.id, 'email': updated_user.email}), 200

@user_blueprint.route('/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    """
    Delete a user
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: User deleted successfully
      404:
        description: User not found
      401:
        description: Token is missing or invalid
    """
    success = user_service.delete_user(user_id)
    if not success:
        return jsonify({'message': 'User not found'}), 404
    
    return '', 204
