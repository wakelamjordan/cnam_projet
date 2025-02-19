from flask import Blueprint, jsonify, request
from ..models.user_model import User as Entity
from ..services.user_service import insert, delete
import string, secrets

user_blueprint = Blueprint('user', __name__)


class UserController:

    @staticmethod
    @user_blueprint.route('/', methods=['GET', 'POST'])
    def index():
        character_all = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(character_all) for i in range(20))

        data = Entity(request.form.get('email'), password)
        insert(data)
        # return data.__repr__()
        return jsonify({'email': request.form.get('email')}), 200

    @staticmethod
    @user_blueprint.route('/new', methods=['GET', 'POST'])
    def new():
        character_all = string.ascii_letters + string.digits
        password: str = ''.join(
            secrets.choice(character_all) for i in range(20))

        data = Entity(request.form.get('email'), password)
        insert(data)
        # return data.__repr__()
        return jsonify({'email': request.form.get('email')}), 200

    @staticmethod
    @user_blueprint.route('/delete', methods=['DELETE'])
    def delete():
        email = request.form.get('email')
        response = delete(email)
        if response:
            code: int = 200
            message = {'email': email}
        else:
            code: int = 404
            message = {'error': 'error!'}
        return jsonify(message), code
