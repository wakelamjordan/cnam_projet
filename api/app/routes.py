from . import app

from flask import jsonify


@app.route("/user/<name>", methods=['GET'])
def hello_world(name):
    from app.models.user import User
    u = User.query.filter_by(name=name).first()

    return jsonify(u.to_dict())
