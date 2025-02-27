import pytest
from app import create_app
import os
from urllib.parse import urlencode
from app.models.user_model import User
from app.models.role_model import Role
from werkzeug.security import generate_password_hash
from app.services.user_service import insert as insert_user
from app.services.role_service import insert as insert_role

ADMIN_TOKEN = None
USER_TOKEN = None


@pytest.fixture
def client():
    """
    Crée un client de test Flask configuré en mode `testing`.
    
    - Définit la variable d'environnement `FLASK_ENV` à "testing".
    - Active le mode `TESTING` dans la configuration de l'application.
    - Retourne un client de test pour exécuter des requêtes HTTP.
    """
    os.environ["FLASK_ENV"] = "testing"
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def headers():
    """
    Fixture définissant les en-têtes HTTP par défaut pour les requêtes JSON.
    """
    headers = {"Content-Type": "application/json"}
    yield headers


# -------------------login
def test_login_admin(client, headers):
    global ADMIN_TOKEN
    payload = {
        "email": "admin@gmail.com",
        "password": "lnYg6Rtwp9NqEm$ygUjxf1u17"
    }

    response = client.post("/login/", json=payload, headers=headers)

    assert response.status_code == 200

    assert response.json.get("message") == "Login successful"

    ADMIN_TOKEN = response.json.get("token")


def test_login_false(client, headers):
    # global ADMIN_TOKEN
    payload = {
        "email": "admin@gmail.com",
        "password": "Vdqcw4TympGe3lrKbpUUrN79@e"
    }

    response = client.post("/login/", json=payload, headers=headers)

    assert response.status_code == 401
    assert response.json.get("error") == "Invalid email or password."


def test_login_email_bad_format(client, headers):
    # global ADMIN_TOKEN
    payload = {
        "email": "admingmailcom",
        "password": "Vdqcw4TympGe3lrKbpUUrN79@e"
    }

    response = client.post("/login/", json=payload, headers=headers)

    assert response.status_code == 415

    assert response.json.get("error") == "Email not valid"


def test_login_user(client, headers):
    global USER_TOKEN
    payload = {
        "email": "user1@mail.com",
        "password": "lnYg6Rtwp9NqEm$ygUjxf1u17"
    }

    response = client.post("/login/", json=payload, headers=headers)

    assert response.status_code == 200

    assert response.json.get("message") == "Login successful"

    USER_TOKEN = response.json.get("token")


# ------------------new
def test_user_new_admin(client, headers):
    global ADMIN_TOKEN
    user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.post("/user/new",
                           json=user_know,
                           headers=headers_with_token)
    assert response.status_code == 201
    assert response.json.get("email") == "test@gmail.com"


def test_user_new_admin_user_know(client, headers):
    global ADMIN_TOKEN
    user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.post("/user/new",
                           json=user_know,
                           headers=headers_with_token)
    assert response.status_code == 400

    assert response.json.get("error") == "Email test@gmail.com does exist"


def test_user_new_admin_email_bad_format(client, headers):
    global ADMIN_TOKEN
    user_know = {"email": "test@gmailcom"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.post("/user/new",
                           json=user_know,
                           headers=headers_with_token)
    assert response.status_code == 415
    assert response.json.get("error") == "Email not valid"


def test_user_new_user(client, headers):
    global USER_TOKEN
    user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + USER_TOKEN
    response = client.post("/user/new",
                           json=user_know,
                           headers=headers_with_token)
    assert response.status_code == 403
    assert response.json.get("error") == "Access Denied"


def test_user_new_not_logged(client, headers):
    # global ADMIN_TOKEN
    user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    # headers_with_token["Authorization"] = "Bearer "
    response = client.get("/user/new",
                          json=user_know,
                          headers=headers_with_token)
    assert response.status_code == 401
    assert response.json.get("msg") == "Missing Authorization Header"


# ---------------put
def test_user_put_not_logged(client, headers):
    # global ADMIN_TOKEN
    user_know = {
        "email": "test@gmail.com",
        "firstname": "modif put",
        "lastname": "modif put",
        "birth_at": "1990-07-28",
        "password": "lnYg6Rtwp9NqEm$ygUjxf1u17",
        "role": None
    }
    headers_with_token = headers
    # headers_with_token["Authorization"] = "Bearer "
    response = client.put("/user/test@gmail.com",
                          json=user_know,
                          headers=headers_with_token)
    assert response.status_code == 401
    assert response.json.get("msg") == "Missing Authorization Header"


def test_user_put_admin(client, headers):
    global ADMIN_TOKEN
    user_know = {
        "email": "test@gmail.com",
        "firstname": "modif put",
        "lastname": "modif put",
        "birth_at": "1990-07-28",
        "password": "lnYg6Rtwp9NqEm$ygUjxf1u17",
        "role": None
    }
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.put("/user/test@gmail.com",
                          json=user_know,
                          headers=headers_with_token)
    assert response.status_code == 200
    data_return = response.json
    del data_return["birth_at"]
    assert data_return == {
        "email": "test@gmail.com",
        "firstname": "modif put",
        "lastname": "modif put",
        # "birth_at": "1990-07-28",
        "role": None
    }


def test_user_put_admin_user_not_know(client, headers):
    global ADMIN_TOKEN
    user_know = {
        "email": "test@gmail.com",
        "firstname": "modif put",
        "lastname": "modif put",
        "birth_at": "1990-07-28",
        "password": "lnYg6Rtwp9NqEm$ygUjxf1u17",
        "role": None
    }
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.put("/user/unknow@gmail.com",
                          json=user_know,
                          headers=headers_with_token)
    assert response.status_code == 404
    assert response.json.get("error") == 'Email unknow@gmail.com not found'


def test_user_put_admin_email_bad_format(client, headers):
    global ADMIN_TOKEN
    user_know = {
        "email": "test@gmail.com",
        "firstname": "modif put",
        "lastname": "modif put",
        "birth_at": "1990-07-28",
        "password": "lnYg6Rtwp9NqEm$ygUjxf1u17",
        "role": None
    }
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.put("/user/test@gmailcom",
                          json=user_know,
                          headers=headers_with_token)
    assert response.status_code == 415
    assert response.json.get("error") == "Email not valid"


def test_user_put_user(client, headers):
    global USER_TOKEN
    user_know = {
        "email": "test@gmail.com",
        "firstname": "modif put",
        "lastname": "modif put",
        "birth_at": "1990-07-28",
        "password": "lnYg6Rtwp9NqEm$ygUjxf1u17",
        "role": None
    }
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + USER_TOKEN
    response = client.put("/user/test@gmail.com",
                          json=user_know,
                          headers=headers_with_token)
    assert response.status_code == 403


# ---------------patch
def test_user_patch_not_logged(client, headers):
    # global ADMIN_TOKEN
    user_know = {
        "firstname": "modif patch",
        "lastname": "modif patch",
    }
    headers_with_token = headers
    # headers_with_token["Authorization"] = "Bearer "
    response = client.patch("/user/test@gmail.com",
                            json=user_know,
                            headers=headers_with_token)
    assert response.status_code == 401
    assert response.json.get("msg") == "Missing Authorization Header"


def test_user_patch_admin(client, headers):
    global ADMIN_TOKEN
    user_know = {
        "firstname": "modif patch",
        "lastname": "modif patch",
    }
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.patch("/user/test@gmail.com",
                            json=user_know,
                            headers=headers_with_token)
    assert response.status_code == 200


def test_user_patch_admin_user_not_know(client, headers):
    global ADMIN_TOKEN
    user_know = {
        "firstname": "modif patch",
        "lastname": "modif patch",
    }
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.patch("/user/unknow@gmail.com",
                            json=user_know,
                            headers=headers_with_token)
    assert response.status_code == 404
    assert response.json.get("error") == 'Email unknow@gmail.com not found'


def test_user_patch_admin_email_bad_format(client, headers):
    global ADMIN_TOKEN
    user_know = {
        "firstname": "modif patch",
        "lastname": "modif patch",
    }
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.patch("/user/test@gmailcom",
                            json=user_know,
                            headers=headers_with_token)
    assert response.status_code == 415
    assert response.json.get("error") == "Email not valid"


def test_user_patch_user(client, headers):
    global USER_TOKEN
    user_know = {
        "firstname": "modif patch",
        "lastname": "modif patch",
    }
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + USER_TOKEN
    response = client.patch("/user/test@gmail.com",
                            json=user_know,
                            headers=headers_with_token)
    assert response.status_code == 403


# ---------------get_one
def test_user_get_one_not_logged(client, headers):
    # global ADMIN_TOKEN
    # user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    # headers_with_token["Authorization"] = "Bearer "
    response = client.get("/user/test@gmail.com", headers=headers_with_token)
    assert response.status_code == 401
    assert response.json.get("msg") == "Missing Authorization Header"


def test_user_get_one_admin(client, headers):
    global ADMIN_TOKEN
    # user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.get("/user/test@gmail.com", headers=headers_with_token)
    assert response.status_code == 200


def test_user_get_one_admin_user_not_know(client, headers):
    global ADMIN_TOKEN
    user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.get("/user/unknow@gmail.com", headers=headers_with_token)
    assert response.status_code == 404
    assert response.json.get("error") == 'Email unknow@gmail.com not found'


def test_user_get_one_admin_email_bad_format(client, headers):
    global ADMIN_TOKEN
    user_know = {"email": "test@gmailcom"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.get("/user/test@gmailcom", headers=headers_with_token)
    assert response.status_code == 415
    assert response.json.get("error") == "Email not valid"


def test_user_get_one_user(client, headers):
    global USER_TOKEN
    # user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + USER_TOKEN
    response = client.get("/user/test@gmail.com", headers=headers_with_token)
    assert response.status_code == 403


# ---------------get_all
def test_user_get_all_admin(client, headers):
    global ADMIN_TOKEN
    # user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.get("/user/", headers=headers_with_token)
    assert response.status_code == 200


def test_user_get_all_user(client, headers):
    global USER_TOKEN
    # user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + USER_TOKEN
    response = client.get("/user/", headers=headers_with_token)
    assert response.status_code == 403


def test_user_get_all_not_logged(client, headers):
    # global USER_TOKEN
    # user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    # headers_with_token["Authorization"] = "Bearer "
    response = client.get("/user/", headers=headers_with_token)
    assert response.status_code == 401
    assert response.json.get("msg") == "Missing Authorization Header"


# --------------------delete
def test_user_delete_admin(client, headers):
    global ADMIN_TOKEN
    user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.delete("/user/delete",
                             json=user_know,
                             headers=headers_with_token)
    assert response.status_code == 200


def test_user_delete_admin_user_not_know(client, headers):
    global ADMIN_TOKEN
    user_know = {"email": "unknow@gmail.com"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.delete("/user/delete",
                             json=user_know,
                             headers=headers_with_token)
    assert response.status_code == 404
    assert response.json.get("error") == 'Email unknow@gmail.com not found'


def test_user_delete_admin_email_bad_format(client, headers):
    global ADMIN_TOKEN
    user_know = {"email": "test@gmailcom"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.delete("/user/delete",
                             json=user_know,
                             headers=headers_with_token)
    assert response.status_code == 415
    assert response.json.get("error") == "Email not valid"


def test_user_delete_user(client, headers):
    global USER_TOKEN
    user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + USER_TOKEN
    response = client.delete("/user/delete",
                             json=user_know,
                             headers=headers_with_token)
    assert response.status_code == 403


def test_user_delete_not_logged(client, headers):
    # global USER_TOKEN
    user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    # headers_with_token["Authorization"] = "Bearer "
    response = client.get("/user/delete",
                          json=user_know,
                          headers=headers_with_token)
    assert response.status_code == 401
    assert response.json.get("msg") == "Missing Authorization Header"
