from . import app

from flask import jsonify, current_app


@app.route("/user/<name>", methods=['GET'])
def hello_world(name):
    from app.models.user import User
    u = User.query.filter_by(name=name).first()

    return jsonify(u.to_dict())


@app.route("/test")
def test():
    from app.models.user import User
    u = User.query_sql('select * from users where name = :name',
                       {'name': 'toto'})
    return jsonify(u)
    # return 'eee'
