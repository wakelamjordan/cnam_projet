from ..models import get_db
from ..models.user_model import User as Entity
from sqlalchemy.orm import Session
from ..errors.user_error import UserNotFoundError, UserEmailDoesExist


def insert(entity: Entity):
    """
    Insère un nouvel utilisateur dans la base de données.

    Cette fonction prend un objet `User` en argument et l'ajoute à la base de données.
    Si une erreur survient lors de l'ajout (par exemple, si l'email existe déjà), une exception `UserEmailDoesExist`
    est levée et la transaction est annulée.

    Paramètre:
        entity (Entity) : Un objet `User` représentant l'utilisateur à insérer dans la base de données.
    
    Lève:
        UserEmailDoesExist : Si l'email de l'utilisateur existe déjà dans la base de données.
    """
    db: Session = next(get_db())
    try:
        db.add(entity)
        db.commit()
    except Exception as e:
        db.rollback()
        raise UserEmailDoesExist({'error': 'error!'})
    finally:
        db.close()


def delete(entity: Entity):
    """
    Supprime un utilisateur de la base de données en fonction de son email.

    Cette fonction cherche un utilisateur correspondant à l'email fourni, et si trouvé, le supprime de la base de données.
    Si aucun utilisateur n'est trouvé, elle retourne `None`. Si une erreur survient, une exception `UserNotFoundError`
    est levée.

    Paramètre:
        entity (Entity) : Un objet `User` représentant l'utilisateur à supprimer.

    Retourne:
        str | None : L'email de l'utilisateur supprimé si trouvé, sinon `None`.

    Lève:
        UserNotFoundError : Si aucun utilisateur n'est trouvé avec l'email spécifié.
    """
    db: Session = next(get_db())
    try:
        entity_find = find_by_email(entity)
        if entity_find:
            db.delete(entity_find)
            db.commit()
            return entity.get_email()
        else:
            return None
    except Exception as e:
        db.rollback()
        raise UserNotFoundError({'error': 'error!'})
    finally:
        db.close()


def find_by_email(entity: Entity):
    """
    Recherche un utilisateur dans la base de données en utilisant son email.

    Cette fonction effectue une recherche dans la base de données en filtrant par l'email de l'utilisateur.
    Si aucun utilisateur n'est trouvé, elle lève une exception `UserNotFoundError`.

    Paramètre:
        entity (Entity) : Un objet `User` représentant l'utilisateur dont l'email doit être recherché.

    Retourne:
        Entity : L'utilisateur trouvé, représenté sous forme d'objet `User`.

    Lève:
        UserNotFoundError : Si aucun utilisateur n'est trouvé avec l'email spécifié.
    """
    db: Session = next(get_db())
    try:
        result = db.query(Entity).filter(
            Entity._email == entity.get_email()).first()
        if not result:
            raise UserNotFoundError({'error': 'error!'})
        return result
    finally:
        db.close()


def find_all():
    """
    Récupère tous les utilisateurs dans la base de données.

    Cette fonction retourne une liste contenant tous les utilisateurs présents dans la table `user`.

    Retourne:
        list : Une liste d'objets `User` représentant tous les utilisateurs.
    """
    db: Session = next(get_db())
    return db.query(Entity).all()
