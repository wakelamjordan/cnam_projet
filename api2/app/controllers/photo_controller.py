from flask import Blueprint, jsonify, request, current_app
from app.services.photo_service import select_all, insert, select_one
from app.errors.service_error import InvalidEntryError, EntryUnavailableError

photo_blueprint = Blueprint('photo', __name__)


class PhotoController():

    @staticmethod
    @photo_blueprint.route('', methods=['GET'])
    def index():
        return jsonify({"photos": select_all()}), 200

    @staticmethod
    @photo_blueprint.route('', methods=['POST'])
    def post():
        # try:
        data: dict = request.json
        file = request.files['photo']
        print(file, data)

    #     propery_check: list = ['path', 'name', 'description']
    #     for x in range(len(data)):
    #         if propery_check[x] not in data:
    #             raise InvalidEntryError()
    #     print(select_one(data))
    #     if select_one(data):
    #         raise EntryUnavailableError('Entry name\'s already exist.')
    #     return jsonify({"photos": insert()}), 200
    # except InvalidEntryError as e:
    #     return jsonify({'error': str(e)}), 400
    # except EntryUnavailableError as e:
    #     return jsonify({'error': str(e)}), 400

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in  current_app.config['ALLOWED_EXTENSIONS']
