from flask import Blueprint, jsonify
from app.services.role_service import select_all
from flask_jwt_extended import jwt_required, get_jwt
from app.errors.security_error import AccessDenied

role_blueprint = Blueprint('role', __name__)


class RoleController():

    @staticmethod
    @role_blueprint.route('', methods=['GET'])
    @jwt_required()
    def index():
        try:
            payload: dict = get_jwt()
            if not 'role' in payload or payload['role'] != 'ROLE_ADMIN':
                raise AccessDenied()

            return jsonify({"roles": select_all()}), 200
        except AccessDenied as e:
            return jsonify({'error': str(e)})
