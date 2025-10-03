from flask import Blueprint, jsonify
from flasgger import swag_from
from ..application.services import StructureService
from ..infrastructure.repositories.sql_repositories import SQLStructureRepository
from .auth_decorator import token_required

structure_bp = Blueprint('structures', __name__)
structure_repo = SQLStructureRepository()
structure_service = StructureService(structure_repo)

@structure_bp.route('/', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Structures'],
    'summary': 'Get a list of all monitored structures.',
    'security': [{'Bearer': []}],
    'responses': {
        '200': {
            'description': 'A list of structures.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'location': {'type': 'string'},
                        'status': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_structures():
    structures = structure_service.get_all_structures()
    return jsonify([{
        'id': s.id, 'name': s.name, 'location': s.location, 'status': s.status
    } for s in structures])

@structure_bp.route('/<int:structure_id>', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Structures'],
    'summary': 'Get detailed information for a single structure.',
    'security': [{'Bearer': []}],
    'parameters': [
        {'name': 'structure_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        '200': {'description': 'Structure details.'},
        '404': {'description': 'Structure not found.'}
    }
})
def get_structure_details(structure_id):
    details = structure_service.get_structure_details(structure_id)
    if details:
        return jsonify({
            'id': details.id, 'name': details.name, 'location': details.location, 
            'status': details.status, 'created_at': details.created_at
        })
    return jsonify({'message': 'Structure not found'}), 404

@structure_bp.route('/<int:structure_id>/sensor-data', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Structures'],
    'summary': 'Get all sensor data for a specific structure.',
    'security': [{'Bearer': []}],
    'parameters': [
        {'name': 'structure_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        '200': {'description': 'A list of sensor data points.'},
        '404': {'description': 'Structure not found.'}
    }
})
def get_sensor_data(structure_id):
    if not structure_service.get_structure_details(structure_id):
        return jsonify({'message': 'Structure not found'}), 404

    data = structure_service.get_all_sensor_data_for_structure(structure_id)
    return jsonify([{
        'id': d.id, 'sensor_type': d.sensor_type, 'value': d.value,
        'timestamp': d.timestamp.isoformat()
    } for d in data])
