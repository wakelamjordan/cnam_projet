from flask import current_app, render_template, url_for
from app.models import get_db
from app.models.user_model import User as Entity
from app.errors.user_error import UserNotFoundError
from app.errors.security_error import LoginError
from werkzeug.security import check_password_hash
from sqlalchemy.orm import Session
from app.models import get_db
from app.errors.user_error import UserEmailNotValide, UserEmailDoesExist
from app.models.user_model import User as Entity
from flask_mail import Message, Mail
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token


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


def insert(entity_dict: dict) -> str:
    """
    Insère un nouvel utilisateur dans la base de données.

    Paramètres:
        entity_dict (dict) : Dictionnaire contenant les informations de l'utilisateur à insérer.

    Retourne:
        str : L'email de l'utilisateur inséré.

    Lève:
        UserEmailDoesExist : Si l'email existe déjà.
        UserEmailNotValide : Si l'email n'est pas valide.
    """
    db: Session = next(get_db())

    try:
        check_email = db.query(Entity).filter(
            Entity._email == entity_dict["email"]).first()
        if check_email is not None:
            raise UserEmailDoesExist()
        entity: Entity = Entity(entity_dict["email"])
        entity.set_password(entity_dict["password"])
        db.add(entity)

        link: str = make_link('security.inscription_complete',
                              entity_dict["email"])
        template_email: str = render_template(
            "mail/validation.html",
            user_name=entity_dict["email"],
            confirmation_url=link,
            current_year=datetime.today().year)

        send_verification("Inscription-mairie", [entity_dict["email"]],
                          template_email)
        db.commit()

        return entity_dict["email"]
    except UserEmailDoesExist:
        db.rollback()
        raise
    except UserEmailNotValide:
        db.rollback()
        raise
    finally:
        db.close()


def send_verification(subject: str, recipients: list, template: str) -> None:
    msg = Message(subject=subject,
                  sender=current_app.config["MAIL_DEFAULT_SENDER"],
                  recipients=recipients,
                  html=template)
    mail: Mail = current_app.extensions["mail"]
    mail.send(msg)


def make_link(route: str, email: str) -> str:
    token: str = create_access_token(
        identity=email,
        expires_delta=timedelta(hours=24),
        additional_claims={"type": "email_verification"})
    route = url_for(route, token=token, _external=True)
    return route
