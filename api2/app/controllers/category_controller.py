from flask import Blueprint, request
from app.services.category_service import find_all
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt

category_blueprint = Blueprint("category", __name__)


class CategoryController:

    @staticmethod
    @category_blueprint.route('', methods=['GET'])
    def categories():
        auth_header = request.headers.get('Authorization')
        if auth_header:
            verify_jwt_in_request()
            role = get_jwt().get('role')
            find_all(role)
        else:
            return find_all()

    @staticmethod
    @category_blueprint.route('/new', methods=['POST'])
    @jwt_required()
    def category_new():
        payload: dict = get_jwt()
        if not 'role' in payload or payload['role'] != 'ROLE_ADMIN':
            return 'pas admin'
        category: dict = request.json

        return category
