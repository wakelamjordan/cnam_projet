import flask
from app.models.user import User
from app.manager.user import User as Manager


class userController():

    def new(self):
        if flask.request.method == 'GET':
            return 'token'
        elif flask.request.method == 'POST':
            user = User(flask.request.form.get("email"),
                        flask.request.form.get("firstName"),
                        flask.request.form.get("lastName"))

            return Manager.insert(user)
            # print(user.to_dict())
