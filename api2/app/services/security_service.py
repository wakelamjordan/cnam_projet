from app.models import get_db
from app.models.user_model import User as Entity
from app.errors.user_error import UserNotFoundError
from app.errors.security_error import LoginError
from werkzeug.security import check_password_hash


def login(entity_login: dict) -> dict:
    """
    Authentifie un utilisateur en vérifiant ses informations d'identification.

    Paramètres:
        entity_login (dict) : Dictionnaire contenant l'email et le mot de passe de l'utilisateur.

    Retourne:
        dict : Un dictionnaire contenant les informations de l'utilisateur authentifié (email, prénom, rôle).

    Lève:
        LoginError : Si l'email ou le mot de passe est invalide.
        UserNotFoundError : Si l'utilisateur n'est pas trouvé.
    """
    db: Session = next(get_db())
    try:
        entity: Entity = db.query(Entity).filter(
            Entity._email == entity_login["email"]).first()

        if not entity:
            raise LoginError("Invalid email or password.")

        if not check_password_hash(entity.get_password(),
                                   entity_login["password"]):
            raise LoginError("Invalid email or password.")

        entity.set_login_at()

        response = {
            "email": entity.get_email(),
            "firstname": entity.get_firstname(),
            "role": entity.get_role()
        }
        db.add(entity)
        db.commit()
        return response

    except UserNotFoundError:
        raise
    finally:
        db.close()
