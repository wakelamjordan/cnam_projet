import flask
from app.models.user import User
from app.manager.user import User as Manager
from flask import jsonify


class userController():

    def new(self):
        if flask.request.method == 'GET':
            return 'token'
        elif flask.request.method == 'POST':
            user = User(flask.request.form.get("email"),
                        flask.request.form.get("firstName"),
                        flask.request.form.get("lastName"))

            Manager.insert(user)
            return jsonify({"email": user.getEmail()}), 200

    def getUser(self, email):
        user = Manager.findByEmail(email)
        print(user)
