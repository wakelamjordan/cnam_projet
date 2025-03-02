from flask_mail import Message
from flask import Blueprint, current_app

message_blueprint = Blueprint('message', __name__)


@message_blueprint.route("/")
def test():
    mail = current_app.extensions['mail']
    msg = Message(subject="Hello",
                  sender="mairie@gmail.com",
                  recipients=["admin@gmail.com", "user1@gmail.com"])
    mail.send(msg)
    return
