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


def test_login(client, headers):
    global ADMIN_TOKEN
    payload = {
        "email": "admin@gmail.com",
        "password": "Vdqcw4TympGe3lrKbpUUrN79@"
    }

    response = client.post("/login/", json=payload, headers=headers)

    assert response.status_code == 200

    ADMIN_TOKEN = response.json.get("token")


def test_login_0(client, headers):
    # global ADMIN_TOKEN
    payload = {
        "email": "admin@gmail.com",
        "password": "Vdqcw4TympGe3lrKbpUUrN79@e"
    }

    response = client.post("/login/", json=payload, headers=headers)

    assert response.status_code == 401

    # ADMIN_TOKEN = response.json.get("token")


def test_user_new(client, headers):
    global ADMIN_TOKEN
    user_know = {"email": "admin@gmail.com"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.post("/user/new",
                           json=user_know,
                           headers=headers_with_token)
    assert response.status_code == 400


# # @pytest.fixture
# def test_insert_admin(client):
#     role = Role("ROLE_ADMIN")

#     admin = User("admin@gmail.com")
#     admin.set_password(
#         generate_password_hash("Vdqcw4TympGe3lrKbpUUrN79@",
#                                method="pbkdf2:sha256",
#                                salt_length=16))
#     admin.set_role("ROLE_ADMIN")
#     admin.set_firstname("admin")
#     admin.set_lastname("adminlastname")
#     with client.application.app_context():
#         insert_role(role)
#         insert_admin = insert_user(admin)
#     yield insert_admin

# @pytest.fixture
# def login_admin(client, insert_admin, headers):
#     admin_email = insert_admin  # Email de l'admin inséré

#     # Ici, tu peux utiliser l'admin dans tes tests
#     # Par exemple, en simulant une connexion avec JWT

#     payload = {
#         "email": admin_email,
#         "password":
#         "Vdqcw4TympGe3lrKbpUUrN79@eee"  # Mot de passe que tu as défini
#     }

#     # Requête POST pour te connecter avec l'admin
#     response = client.post('/login/', json=payload, headers=headers)
#     assert response.status_code == 401

#     payload = {
#         "email": admin_email,
#         "password":
#         "Vdqcw4TympGe3lrKbpUUrN79@"  # Mot de passe que tu as défini
#     }

#     # Requête POST pour te connecter avec l'admin
#     response = client.post('/login/', json=payload, headers=headers)

#     # Vérifier que la réponse est correcte (ex: status 200 et un token)
#     assert response.status_code == 200

#     login_admin = response.json.get("token")
#     yield login_admin

# # @pytest.fixture
# def test_user_get_all(client, login_admin, headers):
#     headers_json = headers
#     headers_json["Authorization"] = "Bearer " + login_admin
#     response = client.get("/user/", headers=headers)
#     assert response.status_code == 200
#     headers_json["Authorization"] = "Bearer " + login_admin + "kjhkjh"
#     response = client.get("/user/", headers=headers)
#     assert response.status_code == 422

# # @pytest.fixture
# def test_user_get_one(client, login_admin, headers):
#     headers_json = headers
#     headers_json["Authorization"] = "Bearer " + login_admin

#     response = client.get(f"/user/?{urlencode({"email": "admin@gmail.com"})}", headers=headers)
#     assert response.status_code == 200
# headers_json["Authorization"] = "Bearer " + login_admin + "kjhkjh"
# response = client.get("/user/", headers=headers)
# assert response.status_code == 422

# def test_admin_access(client, login_admin, user_get_all, user_get_one):
#     assert login_admin is not None  # Vérifie que le token est bien reçu

# def test_login():
#     admin = User("admin@gmail.com")
#     admin.set_password(
#         generate_password_hash("Vdqcw4TympGe3lrKbpUUrN79@",
#                                method="pbkdf2:sha256",
#                                salt_length=16))
#     admin.set_role("ROLE_ADMIN")
#     admin.set_firstname("admin")
#     admin.set_lastname("adminlastname")
#     email = insert(admin)
#     assert email == "jjj"

# @pytest.fixture
# def list_users_ok():
#     """
#     Fixture contenant une liste d'adresses email valides pour les tests.
#     """
#     list_users_ok = [{
#         "email": "test@gmail.com",
#         "password": "Vdqcw4TympGe3lrKbpUUrN79@",
#     }, {
#         "email": "test2@gmail.com",
#         "password": "Vdqcw4TympGe3lrKbpUUrN79@"
#     }, {
#         "email": "test3@gmail.com",
#         "password": "Vdqcw4TympGe3lrKbpUUrN79@"
#     }, {
#         "email": "test4@gmail.com",
#         "password": "Vdqcw4TympGe3lrKbpUUrN79@"
#     }, {
#         "email": "test5@gmail.com",
#         "password": "Vdqcw4TympGe3lrKbpUUrN79@"
#     }]
#     yield list_users_ok

# @pytest.fixture
# def list_user_not_ok():
#     """
#     Fixture contenant une liste d'adresses email invalides pour tester la validation.
#     """
#     list_user_not_ok = [{
#         "email": "testgmailcom",
#         "password": "Vdqcw4TympG"
#     }, {
#         "email": "test2@@gmail.@com",
#         "password": "Vdqcw4TympG"
#     }, {
#         "email": "test3_t$js@gmail.com",
#         "password": "Vdqcw4TympG"
#     }, {
#         "email": "@test4@gmailcom",
#         "password": "Vdqcw4TympG"
#     }, {
#         "email": "tiiii@@est5@gmailcom",
#         "password": "Vdqcw4TympG"
#     }]
#     yield list_user_not_ok

# def test_security_controller_login

# def test_user_controller_new(client, headers, list_users_ok, list_user_not_ok):
#     """
#     Teste l'ajout d'un nouvel utilisateur via l'endpoint `/user/new`.

#     - Vérifie que l'ajout d'un utilisateur valide retourne un code `201 Created`.
#     - Vérifie qu'un email déjà existant retourne une erreur `400 Bad Request`.
#     - Vérifie que les emails invalides sont rejetés avec un code `415 Unsupported Media Type`.
#     """
#     for user in list_users_ok:
#         response = client.post("/user/new",
#                                json={"email": user["email"]},
#                                headers=headers)
#         assert response.status_code == 201
#         assert response.json["email"] == user["email"]

#         response = client.post("/user/new",
#                                json={"email": list_users_ok[0]["email"]},
#                                headers=headers)
#         assert response.status_code == 400
#         assert response.json["error"] == f"Email {list_users_ok[0]["email"]} does exist"

#     for user in list_user_not_ok:
#         response = client.post("/user/new",
#                                json={"email": user["email"]},
#                                headers=headers)
#         # assert response.
#         assert response.status_code == 415
#         assert response.json == {"error": "Email not valid"}

# def test_user_controller_index(client, headers, list_users_ok, list_user_not_ok):
#     """
#     Teste la récupération, la mise à jour et la modification d'un utilisateur via l'endpoint `/user/`.

#     - Vérifie la récupération de tous les utilisateurs (`GET /user/`).
#     - Vérifie la récupération d'un utilisateur spécifique (`GET /user/?email=<email>`).
#     - Vérifie les mises à jour (`PUT` et `PATCH`) avec des modifications valides et invalides.
#     - Vérifie que la récupération d'un utilisateur inexistant retourne une erreur `404 Not Found`.
#     """
#     response = client.get('/user/')
#     for i in range(len(list_users_ok)):
#         assert response.json[i]["email"] == list_users_ok[i]["email"]

#     params = urlencode({"email": list_users_ok[0]["email"]})
#     response = client.get(f'/user/?{params}')
#     assert response.status_code == 200
#     assert response.json["email"] == list_users_ok[0]["email"]

#     params = urlencode({"email": "inconnu@gmail.com"})
#     response = client.get(f'/user/?{params}')
#     assert response.status_code == 404
#     assert response.json["error"] == "User not found!"

#     params = urlencode({"email": "test3_t$js@gmail.com"})
#     response = client.get(f'/user/?{params}')
#     assert response.status_code == 415
#     assert response.json["error"] == "Email not valid"

#     response = client.put('/user/',
#                           json={
#                               "email": list_users_ok[0]["email"],
#                               "firstname": "modif put",
#                               "lastname": "modif put",
#                               "birth_at": "1990-07-28",
#                               "password":list_users_ok[0]["password"]
#                           },
#                           headers=headers)
#     assert response.status_code == 200
#     assert response.json["firstname"] == "modif put"
#     assert response.json["lastname"] == "modif put"

#     response = client.patch('/user/',
#                             json={
#                                 "email": list_users_ok[0]["email"],
#                                 "firstname": "modif patch",
#                                 "lastname": "modif patch",
#                                 "birth_at": "1990-07-28",
#                                 "password":list_users_ok[0]["password"]
#                             },
#                             headers=headers)
#     assert response.status_code == 200
#     assert response.json["firstname"] == "modif patch"
#     assert response.json["lastname"] == "modif patch"

#     response = client.put('/user/',
#                           json={
#                               "email": "emailnotfound@gmail.com",
#                               "firstname": "modif put",
#                               "lastname": "modif put",
#                               "birth_at": "1990-07-28"
#                           },
#                           headers=headers)
#     assert response.status_code == 404
#     assert response.json["error"] == "Email emailnotfound@gmail.com not found"

#     response = client.patch('/user/',
#                             json={
#                                 "email": "emailnotfound@gmail.com",
#                                 "firstname": "modif patch",
#                                 "lastname": "modif patch",
#                                 "birth_at": "1990-07-28"
#                             },
#                             headers=headers)
#     assert response.status_code == 404
#     assert response.json["error"] == "Email emailnotfound@gmail.com not found"

#     response = client.put('/user/',
#                           json={
#                               "email": list_users_ok[0]["email"],
#                               "firstname": "modif put",
#                               "lastname": "modif put",
#                               "birth_at": "1990-07-28",
#                               "password":list_user_not_ok[0]["password"]
#                           },
#                           headers=headers)
#     assert response.status_code == 415
#     assert response.json["error"] == "Password not valid"

#     response = client.patch('/user/',
#                             json={
#                                 "email":  list_users_ok[0]["email"],
#                                 "firstname": "modif patch",
#                                 "lastname": "modif patch",
#                                 "birth_at": "1990-07-28",
#                                 "password":list_user_not_ok[0]["password"]
#                             },
#                             headers=headers)
#     assert response.status_code == 415
#     assert response.json["error"] == "Password not valid"

# def test_user_controller_delete(client, headers, list_users_ok):
#     """
#     Teste la suppression d'un utilisateur via l'endpoint `/user/delete`.

#     - Vérifie que la suppression d'un utilisateur existant retourne un code `200 OK`.
#     - Vérifie que la suppression d'un utilisateur inexistant retourne une erreur `404 Not Found`.
#     """
#     for user in list_users_ok:
#         response = client.delete("/user/delete",
#                                  json={"email": user["email"]},
#                                  headers=headers)
#         assert response.status_code == 200

#     response = client.delete("/user/delete",
#                              json={"email": "emailnotfound@gmail.com"})
#     assert response.status_code == 404
