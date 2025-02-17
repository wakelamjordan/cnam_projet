from app.models.user import User as entity  # Import de la classe Base pour le mapping ORM
from app.manager.manager import Manager
from datetime import date


class User:

    def findAll():
        return entity.to_list(entity.query.all())

    def findByName(name):
        return entity.to_list(entity.query.filter_by(name=name).all())

    def insert(user):
        if user.getBirthAt() == None:
            user.setBirthAt(date(1989, 12, 12).isoformat())
        # Manager.insert(user)
        return user.to_dict()
