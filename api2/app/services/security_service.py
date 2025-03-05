from flask import current_app, render_template, url_for
from app.models import get_db
from app.models.user_model import User as Entity
from app.errors.user_error import UserNotFoundError, UserEmailNotValide, UserEmailDoesExist
from app.errors.security_error import LoginError, TokenAlreadyUsed
from werkzeug.security import check_password_hash
from sqlalchemy.orm import Session
from app.models.token_model import Token
from flask_mail import Message, Mail
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token

aware_datetime = datetime.now(timezone.utc)


def login(entity_login: dict) -> dict:
    """
    Authenticates a user by verifying their credentials.

    Args:
        entity_login (dict): Dictionary containing user's email and password.

    Returns:
        dict: User information (email, firstname, role) if authentication is successful.

    Raises:
        LoginError: If the email or password is incorrect.
        UserNotFoundError: If the user does not exist.
    """
    db: Session = next(get_db())
    try:
        entity: Entity = db.query(Entity).filter(
            Entity._email == entity_login["email"]).first()

        if not entity or not check_password_hash(entity.get_password(),
                                                 entity_login["password"]):
            raise LoginError("Invalid email or password.")

        entity.set_login_at()
        db.add(entity)
        db.commit()

        return {
            "email": entity.get_email(),
            "firstname": entity.get_firstname(),
            "role": entity.get_role()
        }
    finally:
        db.close()


def insert(entity_dict: dict) -> str:
    """
    Inserts a new user into the database.

    Args:
        entity_dict (dict): Dictionary containing the user's information.

    Returns:
        str: The email of the inserted user.

    Raises:
        UserEmailDoesExist: If the email is already in use.
        UserEmailNotValide: If the email is invalid.
    """
    db: Session = next(get_db())
    try:
        if db.query(Entity).filter(
                Entity._email == entity_dict["email"]).first():
            raise UserEmailDoesExist()

        entity = Entity(entity_dict["email"])
        entity.set_password(entity_dict["password"])

        link = make_link('security.inscription_complete', entity_dict["email"],
                         "email_verification")
        token_entity = Token(link["token"])

        template_email = render_template("mail/validation.html",
                                         user_name=entity_dict["email"],
                                         confirmation_url=link["route"],
                                         current_year=datetime.today().year)

        send_email("Inscription-mairie", [entity_dict["email"]],
                   template_email)

        db.add(entity)
        db.add(token_entity)
        db.commit()

        return entity_dict["email"]
    finally:
        db.close()


def send_email(subject: str, recipients: list, template: str) -> None:
    """
    Sends an email using Flask-Mail.

    Args:
        subject (str): Subject of the email.
        recipients (list): List of recipient email addresses.
        template (str): HTML content of the email.
    """
    msg = Message(subject=subject,
                  sender=current_app.config["MAIL_DEFAULT_SENDER"],
                  recipients=recipients,
                  html=template)
    mail: Mail = current_app.extensions["mail"]
    mail.send(msg)


def password_reset(entity_reset: dict) -> None:
    """
    Initiates a password reset process by generating a reset token and sending an email.

    Args:
        entity_reset (dict): Dictionary containing the user's email.

    Raises:
        UserNotFoundError: If the user does not exist.
    """
    db: Session = next(get_db())
    try:
        result = db.query(Entity).filter(
            Entity._email == entity_reset["email"]).first()
        if not result:
            raise UserNotFoundError

        link = make_link("security.password_reset", entity_reset["email"],
                         "reset_password")
        token_insert(link["token"])

        template = render_template("mail/reset.html",
                                   user_name=result.get_firstname(),
                                   reset_url=link["route"],
                                   current_year=datetime.today().year)

        send_email("Réinitialisation mot de passe", [entity_reset["email"]],
                   template)
    finally:
        db.close()


def make_link(route: str, email: str, type: str) -> dict:
    """
    Generates a verification/reset link with a JWT token.

    Args:
        route (str): The Flask route for the link.
        email (str): The user's email.
        type (str): The type of token (e.g., email_verification, reset_password).

    Returns:
        dict: A dictionary containing the route and token.
    """
    token = create_access_token(identity=email,
                                expires_delta=timedelta(minutes=30),
                                additional_claims={"type": type})
    return {
        "route": url_for(route, token=token, _external=True),
        "token": token
    }


def token_check(token: str) -> bool:
    """
    Verifies if a token is still valid and has not been used before.

    Args:
        token (str): The JWT token to check.

    Returns:
        bool: True if the token is valid, False otherwise.

    Raises:
        TokenAlreadyUsed: If the token has already been used.
    """
    db: Session = next(get_db())
    try:
        token_find = db.query(Token).filter(Token._token == token).first()
        if not token_find:
            raise TokenAlreadyUsed
        token_purge(db)
        db.delete(token_find)
        db.commit()
        return True
    finally:
        db.close()


def token_insert(token: str) -> None:
    """
    Inserts a newly generated token into the database.

    Args:
        token (str): The JWT token to store.
    """
    db: Session = next(get_db())
    db.add(Token(token))
    db.commit()
    db.close()


def token_purge(db: Session) -> None:
    """
    Removes expired tokens from the database.

    Args:
        db (Session): The database session.
    """
    limite = aware_datetime + timedelta(minutes=30)
    tokens_ood_find = db.query(Token).filter(Token._created_at <= limite)
    if tokens_ood_find:
        for token in tokens_ood_find:
            db.delete(token)
