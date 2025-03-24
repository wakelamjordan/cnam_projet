from app.models.user import User as entity  # Import de la classe Base pour le mapping ORM
from app.manager.manager import Manager
from datetime import date
import secrets
import string


class User:

    def findAll(self):
        return entity.to_list(entity.query.all())

    def findByName(self, name):
        return entity.to_list(entity.query.filter_by(name == name).all())

    def insert(self, user):
        if user.getPassword() == None:
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(20))
            user.setPassword(password)
        Manager.insert(user)

    def findByEmail(self, email):
        user = entity.query.filter_by(email == email).first()
        return user
