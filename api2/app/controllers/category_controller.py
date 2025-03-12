from flask import Blueprint, request, jsonify
from app.services.category_service import find_all, insert, delete
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt
from app.errors.category_error import CategoryNotValid, CategoryNotExist, CategoryAlreadyExist, CategoryHavePublication, CategoryHaveSub
from app.errors.role_error import RoleNotFoundError
from app.errors.security_error import AccessDenied

category_blueprint = Blueprint("category", __name__)


class CategoryController:

    @staticmethod
    @category_blueprint.route('', methods=['GET'])
    def categories():
        auth_header = request.headers.get('Authorization')
        if auth_header:
            verify_jwt_in_request()
            payload: dict = get_jwt()
            return find_all(payload['role'])
        else:
            return find_all()

    @staticmethod
    @category_blueprint.route('/new', methods=['POST'])
    @jwt_required()
    def category_new():
        try:
            payload: dict = get_jwt()
            if not 'role' in payload or payload['role'] != 'ROLE_ADMIN':
                raise AccessDenied()
            category: dict = request.json

            return jsonify({'category': insert(category)}), 200
        except CategoryNotValid as e:
            return jsonify({"error": str(e)}), 415
        except ValueError as e:
            return jsonify({"error": str(e)}), 415
        except CategoryAlreadyExist as e:
            return jsonify({"error": str(e)}), 400
        except CategoryNotExist as e:
            return jsonify({"error": str(e)}), 404
        except RoleNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403

    @staticmethod
    @category_blueprint.route('/delete', methods=['DELETE'])
    @jwt_required()
    def category_delete():
        try:
            payload: dict = get_jwt()
            if not 'role' in payload or payload['role'] != 'ROLE_ADMIN':
                raise AccessDenied()
            category: dict = request.json
            return jsonify({'category': delete(category)}), 200
        except CategoryNotValid as e:
            return jsonify({"error": str(e)}), 415
        except ValueError as e:
            return jsonify({"error": str(e)}), 415
        except CategoryHaveSub as e:
            return jsonify({"error": str(e)}), 400
        except CategoryHavePublication as e:
            return jsonify({"error": str(e)}), 400
        except CategoryAlreadyExist as e:
            return jsonify({"error": str(e)}), 400
        except CategoryNotExist as e:
            return jsonify({"error": str(e)}), 404
        except RoleNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403
