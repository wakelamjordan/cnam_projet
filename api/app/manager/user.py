from app.models.user import User as entity  # Import de la classe Base pour le mapping ORM
class User:
    def findAll():
        return entity.to_list(entity.query.all())

    def findByName(name):
        return entity.to_list(entity.query.filter_by(name=name).all())
    

