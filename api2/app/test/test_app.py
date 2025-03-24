import pytest
from app import create_app
import os

ADMIN_TOKEN = None
USER_TOKEN = None
TEST_TOKEN = None


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
    """
    Teste la connexion d'un administrateur.

    - Envoie une requête POST à l'endpoint `/login/` avec les identifiants de l'administrateur.
    - Vérifie que le statut de la réponse est 200.
    - Vérifie que le message de réponse est "Login successful".
    - Met à jour le jeton d'administrateur (ADMIN_TOKEN).
    """
    global ADMIN_TOKEN
    payload = {
        "email": "admin@gmail.com",
        "password": "lnYg6Rtwp9NqEm$ygUjxf1u17"
    }

    response = client.post("/login", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json.get("message") == "Login successful"
    ADMIN_TOKEN = response.json.get("token")


def test_login_false(client, headers):
    """
    Teste la connexion avec des identifiants incorrects.

    - Envoie une requête POST à l'endpoint `/login/` avec un mot de passe incorrect.
    - Vérifie que le statut de la réponse est 401.
    - Vérifie que le message d'erreur est "Invalid email or password.".
    """
    payload = {
        "email": "admin@gmail.com",
        "password": "Vdqcw4TympGe3lrKbpUUrN79@e"
    }

    response = client.post("/login", json=payload, headers=headers)

    assert response.status_code == 401
    assert response.json.get("error") == "Invalid email or password."


def test_login_email_bad_format(client, headers):
    """
    Teste la connexion avec un format d'email incorrect.

    - Envoie une requête POST à l'endpoint `/login/` avec un email mal formaté.
    - Vérifie que le statut de la réponse est 415.
    - Vérifie que le message d'erreur est "Email not valid".
    """
    payload = {
        "email": "admingmailcom",
        "password": "Vdqcw4TympGe3lrKbpUUrN79@e"
    }

    response = client.post("/login", json=payload, headers=headers)

    assert response.status_code == 415
    assert response.json.get("error") == "Email not valid"


def test_login_user(client, headers):
    """
    Teste la connexion d'un utilisateur.

    - Envoie une requête POST à l'endpoint `/login/` avec les identifiants de l'utilisateur.
    - Vérifie que le statut de la réponse est 200.
    - Vérifie que le message de réponse est "Login successful".
    - Met à jour le jeton de l'utilisateur (USER_TOKEN).
    """
    global USER_TOKEN
    payload = {
        "email": "user1@mail.com",
        "password": "lnYg6Rtwp9NqEm$ygUjxf1u17"
    }

    response = client.post("/login", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json.get("message") == "Login successful"
    USER_TOKEN = response.json.get("token")


# ------------------new
def test_user_new_admin(client, headers):
    """
    Teste la création d'un nouvel utilisateur par un administrateur.

    - Envoie une requête POST à l'endpoint `/user/new` avec un email valide.
    - Vérifie que le statut de la réponse est 201.
    - Vérifie que l'email de l'utilisateur créé est correct.
    """
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
    """
    Teste la création d'un utilisateur déjà existant par un administrateur.

    - Envoie une requête POST à l'endpoint `/user/new` avec un email déjà existant.
    - Vérifie que le statut de la réponse est 400.
    - Vérifie que le message d'erreur est "Email test@gmail.com does exist".
    """
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
    """
    Teste la création d'un utilisateur avec un format d'email incorrect par un administrateur.

    - Envoie une requête POST à l'endpoint `/user/new` avec un email mal formaté.
    - Vérifie que le statut de la réponse est 415.
    - Vérifie que le message d'erreur est "Email not valid".
    """
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
    """
    Teste la création d'un utilisateur par un utilisateur non administrateur.

    - Envoie une requête POST à l'endpoint `/user/new` avec un jeton d'utilisateur.
    - Vérifie que le statut de la réponse est 403.
    - Vérifie que le message d'erreur est "Access Denied".
    """
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
    """
    Teste la création d'un utilisateur sans être connecté.

    - Envoie une requête POST à l'endpoint `/user/new` sans jeton d'authentification.
    - Vérifie que le statut de la réponse est 401.
    - Vérifie que le message d'erreur est "Missing Authorization Header".
    """
    user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    response = client.get("/user/new",
                          json=user_know,
                          headers=headers_with_token)
    assert response.status_code == 401
    assert response.json.get("msg") == "Missing Authorization Header"


# ---------------put
def test_user_put_not_logged(client, headers):
    """
    Teste la mise à jour d'un utilisateur sans être connecté.

    - Envoie une requête PUT à l'endpoint `/user/test@gmail.com` sans jeton d'authentification.
    - Vérifie que le statut de la réponse est 401.
    - Vérifie que le message d'erreur est "Missing Authorization Header".
    """
    user_know = {
        "email": "test@gmail.com",
        "firstname": "modif put",
        "lastname": "modif put",
        "birth_at": "1990-07-28",
        "password": "lnYg6Rtwp9NqEm$ygUjxf1u17",
        "role": None
    }
    headers_with_token = headers
    response = client.put("/user/test@gmail.com",
                          json=user_know,
                          headers=headers_with_token)
    assert response.status_code == 401
    assert response.json.get("msg") == "Missing Authorization Header"


def test_user_put_admin(client, headers):
    """
    Teste la mise à jour d'un utilisateur par un administrateur.

    - Envoie une requête PUT à l'endpoint `/user/test@gmail.com` avec un jeton d'administrateur.
    - Vérifie que le statut de la réponse est 200.
    - Vérifie que les données retournées correspondent aux modifications apportées.
    """
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
        "role": None
    }


def test_user_put_admin_user_not_know(client, headers):
    """
    Teste la mise à jour d'un utilisateur inexistant par un administrateur.

    - Envoie une requête PUT à l'endpoint `/user/unknow@gmail.com` avec un jeton d'administrateur.
    - Vérifie que le statut de la réponse est 404.
    - Vérifie que le message d'erreur est "Email unknow@gmail.com not found".
    """
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
    """
    Teste la mise à jour d'un utilisateur avec un format d'email incorrect par un administrateur.

    - Envoie une requête PUT à l'endpoint `/user/test@gmailcom` avec un jeton d'administrateur.
    - Vérifie que le statut de la réponse est 415.
    - Vérifie que le message d'erreur est "Email not valid".
    """
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
    """
    Teste la mise à jour d'un utilisateur par un utilisateur non administrateur.

    - Envoie une requête PUT à l'endpoint `/user/test@gmail.com` avec un jeton d'utilisateur.
    - Vérifie que le statut de la réponse est 403.
    """
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
    """
    Teste la mise à jour partielle d'un utilisateur sans être connecté.

    - Envoie une requête PATCH à l'endpoint `/user/test@gmail.com` sans jeton d'authentification.
    - Vérifie que le statut de la réponse est 401.
    - Vérifie que le message d'erreur est "Missing Authorization Header".
    """
    user_know = {
        "firstname": "modif patch",
        "lastname": "modif patch",
    }
    headers_with_token = headers
    response = client.patch("/user/test@gmail.com",
                            json=user_know,
                            headers=headers_with_token)
    assert response.status_code == 401
    assert response.json.get("msg") == "Missing Authorization Header"


def test_user_patch_admin(client, headers):
    """
    Teste la mise à jour partielle d'un utilisateur par un administrateur.

    - Envoie une requête PATCH à l'endpoint `/user/test@gmail.com` avec un jeton d'administrateur.
    - Vérifie que le statut de la réponse est 200.
    - Vérifie que les données retournées correspondent aux modifications apportées.
    """
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
    assert response.json == {
        "email": "test@gmail.com",
        "firstname": "modif patch",
        "lastname": "modif patch",
        "role": None
    }


def test_user_patch_admin_user_not_know(client, headers):
    """
    Teste la mise à jour partielle d'un utilisateur inexistant par un administrateur.

    - Envoie une requête PATCH à l'endpoint `/user/unknow@gmail.com` avec un jeton d'administrateur.
    - Vérifie que le statut de la réponse est 404.
    - Vérifie que le message d'erreur est "Email unknow@gmail.com not found".
    """
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
    """
    Teste la mise à jour partielle d'un utilisateur avec un format d'email incorrect par un administrateur.

    - Envoie une requête PATCH à l'endpoint `/user/test@gmailcom` avec un jeton d'administrateur.
    - Vérifie que le statut de la réponse est 415.
    - Vérifie que le message d'erreur est "Email not valid".
    """
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
    """
    Teste la mise à jour partielle d'un utilisateur par un utilisateur non administrateur.

    - Envoie une requête PATCH à l'endpoint `/user/test@gmail.com` avec un jeton d'utilisateur.
    - Vérifie que le statut de la réponse est 403.
    """
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
    """
    Teste la récupération d'un utilisateur sans être connecté.

    - Envoie une requête GET à l'endpoint `/user/test@gmail.com` sans jeton d'authentification.
    - Vérifie que le statut de la réponse est 401.
    - Vérifie que le message d'erreur est "Missing Authorization Header".
    """
    headers_with_token = headers
    response = client.get("/user/test@gmail.com", headers=headers_with_token)
    assert response.status_code == 401
    assert response.json.get("msg") == "Missing Authorization Header"


def test_user_get_one_admin(client, headers):
    """
    Teste la récupération d'un utilisateur par un administrateur.

    - Envoie une requête GET à l'endpoint `/user/test@gmail.com` avec un jeton d'administrateur.
    - Vérifie que le statut de la réponse est 200.
    - Vérifie que l'email de l'utilisateur retourné est correct.
    """
    global ADMIN_TOKEN
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.get("/user/test@gmail.com", headers=headers_with_token)
    assert response.status_code == 200
    assert response.json.get("email") == "test@gmail.com"


def test_user_get_one_admin_user_not_know(client, headers):
    """
    Teste la récupération d'un utilisateur inexistant par un administrateur.

    - Envoie une requête GET à l'endpoint `/user/unknow@gmail.com` avec un jeton d'administrateur.
    - Vérifie que le statut de la réponse est 404.
    - Vérifie que le message d'erreur est "Email unknow@gmail.com not found".
    """
    global ADMIN_TOKEN
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.get("/user/unknow@gmail.com", headers=headers_with_token)
    assert response.status_code == 404
    assert response.json.get("error") == 'Email unknow@gmail.com not found'


def test_user_get_one_admin_email_bad_format(client, headers):
    """
    Teste la récupération d'un utilisateur avec un format d'email incorrect par un administrateur.

    - Envoie une requête GET à l'endpoint `/user/test@gmailcom` avec un jeton d'administrateur.
    - Vérifie que le statut de la réponse est 415.
    - Vérifie que le message d'erreur est "Email not valid".
    """
    global ADMIN_TOKEN
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.get("/user/test@gmailcom", headers=headers_with_token)
    assert response.status_code == 415
    assert response.json.get("error") == "Email not valid"


def test_user_get_one_user(client, headers):
    """
    Teste la récupération d'un utilisateur par un utilisateur non administrateur.

    - Envoie une requête GET à l'endpoint `/user/test@gmail.com` avec un jeton d'utilisateur.
    - Vérifie que le statut de la réponse est 403.
    """
    global USER_TOKEN
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + USER_TOKEN
    response = client.get("/user/test@gmail.com", headers=headers_with_token)
    assert response.status_code == 403


# ---------------get_all
def test_user_get_all_admin(client, headers):
    """
    Teste la récupération de tous les utilisateurs par un administrateur.

    - Envoie une requête GET à l'endpoint `/user/` avec un jeton d'administrateur.
    - Vérifie que le statut de la réponse est 200.
    """
    global ADMIN_TOKEN
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.get("/user", headers=headers_with_token)
    assert response.status_code == 200


def test_user_get_all_user(client, headers):
    """
    Teste la récupération de tous les utilisateurs par un utilisateur non administrateur.

    - Envoie une requête GET à l'endpoint `/user/` avec un jeton d'utilisateur.
    - Vérifie que le statut de la réponse est 403.
    """
    global USER_TOKEN
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + USER_TOKEN
    response = client.get("/user", headers=headers_with_token)
    assert response.status_code == 403


def test_user_get_all_not_logged(client, headers):
    """
    Teste la récupération de tous les utilisateurs sans être connecté.

    - Envoie une requête GET à l'endpoint `/user/` sans jeton d'authentification.
    - Vérifie que le statut de la réponse est 401.
    - Vérifie que le message d'erreur est "Missing Authorization Header".
    """
    headers_with_token = headers
    response = client.get("/user", headers=headers_with_token)
    assert response.status_code == 401
    assert response.json.get("msg") == "Missing Authorization Header"


# -publications------------all-for-user
def test_publications_not_logged(client):
    response = client.get("/publications")
    assert response.status_code == 401
    assert response.json.get("msg") == "Missing Authorization Header"


def test_publications_logged_user(client, headers):
    global USER_TOKEN
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + USER_TOKEN
    response = client.get("/publications", headers=headers_with_token)
    assert response.status_code == 200
    publications: dict = response.json.get("publications")
    assert publications[0]['author_email'] == "user1@mail.com"


def test_publications_logged_admin(client, headers):
    global ADMIN_TOKEN
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.get("/publications", headers=headers_with_token)
    assert response.status_code == 200
    publications: dict = response.json.get("publications")
    assert publications[0]['author_email'] == "user1@mail.com"


# -publication-------------------new
def test_publication_new_not_logged(client, headers):
    # global ADMIN_TOKEN
    # headers_with_token = headers
    # headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    # response = client.get("/publications", headers=headers_with_token)
    publication = {
        "title": "My First Publication-test-user",
        "slug": "my-first-publication-test-user",
        "description": "This is a sample publication for testing purposes.",
        "content":
        "<h2>Qu’est-ce que c’est ?</h2> <p>La transition écologique est une évolution vers un nouveau modèle économique et social, un modèle de développement durable qui renouvelle nos façons de consommer, de produire, de travailler, de vivre ensemble pour répondre aux grands enjeux environnementaux : changement climatique, rareté des ressources, perte accélérée de la biodiversité et multiplication des risques sanitaires environnementaux.</p> <p>Cela regroupe donc un ensemble de principes, fondés sur les problématiques de résilience locale, d’économie circulaire et de réduction des émissions de CO2.</p> <h2>À Pussay</h2> <p>Pour répondre aux enjeux de la transition écologique de notre commune, la municipalité a mis en place une commission dédiée. Celle-ci, composée d’élus et de citoyens concernés et motivés, se réunit régulièrement pour aborder des thématiques variées, et réfléchir sur les réponses concrètes qui peuvent participer au mieux vivre ensemble.</p> <p>Cette commission travaille notamment sur un <strong>Atlas de la biodiversité Communale</strong>, en collaboration avec l’Agence Française pour la Biodiversité.</p> <h2>Présentation</h2> <h3>Un Atlas de la biodiversité communale, mais pour quoi faire ?</h3> <p>Chaque atlas est élaboré, à l’échelle communale ou intercommunale, à partir d’un inventaire précis et cartographié des habitats, de la faune et de la flore.</p> <p>Ces atlas ont pour objectifs de :</p> <ul> <li><strong>Sensibiliser et mobiliser</strong> les élus, les acteurs socio-économiques et les citoyens à la biodiversité.</li> <li><strong>Mieux connaître</strong> la biodiversité sur le territoire d’une commune et identifier les enjeux spécifiques liés.</li> <li><strong>Faciliter la prise en compte</strong> de la biodiversité lors de la mise en place des politiques locales.</li> </ul> <p>Cette démarche est soutenue par l’Agence française pour la biodiversité.</p> <h2>Résultats</h2> <p>Ce projet comprend deux composantes principales :</p> <h3>1. La réalisation d’un inventaire</h3> <p>Celui-ci a été réalisé courant 2019 par le bureau d’étude <strong>EcoloGIE</strong>. Il permet de répertorier les espèces et de préciser les secteurs méritant une protection complémentaire.</p> <p>Retrouvez le document complet : <a href='#'>Pussay ABC Ecolo-GIE.pdf</a></p> <h3>2. Des actions de sensibilisation et de mobilisation citoyenne</h3> <p>Nous avons souhaité que les habitants se sentent concernés. De nombreuses actions ont donc été proposées sur le thème de la biodiversité, animées par des associations locales.</p> <p>Complément d'inventaire : <a href='#'>Pussay complément messicoles - Ecolo GIE.pdf</a></p>",
        "on_line": True,
        "revision": False
    }
    response = client.post("/publication/new", json=publication)
    assert response.status_code == 401
    # publications: dict = response.json.get("publications")
    # assert publications[0]['author_email'] == "user1@mail.com"


def test_publication_new_user_logged(client, headers):
    global USER_TOKEN
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + USER_TOKEN
    # response = client.get("/publications", headers=headers_with_token)
    publication = {
        "title": "My First Publication-test-user",
        "slug": "my-first-publication-test-user",
        "description": "This is a sample publication for testing purposes.",
        "content":
        "<h2>Qu’est-ce que c’est ?</h2> <p>La transition écologique est une évolution vers un nouveau modèle économique et social, un modèle de développement durable qui renouvelle nos façons de consommer, de produire, de travailler, de vivre ensemble pour répondre aux grands enjeux environnementaux : changement climatique, rareté des ressources, perte accélérée de la biodiversité et multiplication des risques sanitaires environnementaux.</p> <p>Cela regroupe donc un ensemble de principes, fondés sur les problématiques de résilience locale, d’économie circulaire et de réduction des émissions de CO2.</p> <h2>À Pussay</h2> <p>Pour répondre aux enjeux de la transition écologique de notre commune, la municipalité a mis en place une commission dédiée. Celle-ci, composée d’élus et de citoyens concernés et motivés, se réunit régulièrement pour aborder des thématiques variées, et réfléchir sur les réponses concrètes qui peuvent participer au mieux vivre ensemble.</p> <p>Cette commission travaille notamment sur un <strong>Atlas de la biodiversité Communale</strong>, en collaboration avec l’Agence Française pour la Biodiversité.</p> <h2>Présentation</h2> <h3>Un Atlas de la biodiversité communale, mais pour quoi faire ?</h3> <p>Chaque atlas est élaboré, à l’échelle communale ou intercommunale, à partir d’un inventaire précis et cartographié des habitats, de la faune et de la flore.</p> <p>Ces atlas ont pour objectifs de :</p> <ul> <li><strong>Sensibiliser et mobiliser</strong> les élus, les acteurs socio-économiques et les citoyens à la biodiversité.</li> <li><strong>Mieux connaître</strong> la biodiversité sur le territoire d’une commune et identifier les enjeux spécifiques liés.</li> <li><strong>Faciliter la prise en compte</strong> de la biodiversité lors de la mise en place des politiques locales.</li> </ul> <p>Cette démarche est soutenue par l’Agence française pour la biodiversité.</p> <h2>Résultats</h2> <p>Ce projet comprend deux composantes principales :</p> <h3>1. La réalisation d’un inventaire</h3> <p>Celui-ci a été réalisé courant 2019 par le bureau d’étude <strong>EcoloGIE</strong>. Il permet de répertorier les espèces et de préciser les secteurs méritant une protection complémentaire.</p> <p>Retrouvez le document complet : <a href='#'>Pussay ABC Ecolo-GIE.pdf</a></p> <h3>2. Des actions de sensibilisation et de mobilisation citoyenne</h3> <p>Nous avons souhaité que les habitants se sentent concernés. De nombreuses actions ont donc été proposées sur le thème de la biodiversité, animées par des associations locales.</p> <p>Complément d'inventaire : <a href='#'>Pussay complément messicoles - Ecolo GIE.pdf</a></p>",
        "on_line": True,
        "revision": False
    }
    response = client.post("/publication/new",
                           json=publication,
                           headers=headers_with_token)
    assert response.status_code == 200
    publications: dict = response.json.get("message")
    assert publications == "my-first-publication-test-user"


def test_publication_new_user_logged_already_exist(client, headers):
    global USER_TOKEN
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + USER_TOKEN
    # response = client.get("/publications", headers=headers_with_token)
    publication = {
        "title": "My First Publication-test-user",
        "slug": "my-first-publication-test-user",
        "description": "This is a sample publication for testing purposes.",
        "content":
        "<h2>Qu’est-ce que c’est ?</h2> <p>La transition écologique est une évolution vers un nouveau modèle économique et social, un modèle de développement durable qui renouvelle nos façons de consommer, de produire, de travailler, de vivre ensemble pour répondre aux grands enjeux environnementaux : changement climatique, rareté des ressources, perte accélérée de la biodiversité et multiplication des risques sanitaires environnementaux.</p> <p>Cela regroupe donc un ensemble de principes, fondés sur les problématiques de résilience locale, d’économie circulaire et de réduction des émissions de CO2.</p> <h2>À Pussay</h2> <p>Pour répondre aux enjeux de la transition écologique de notre commune, la municipalité a mis en place une commission dédiée. Celle-ci, composée d’élus et de citoyens concernés et motivés, se réunit régulièrement pour aborder des thématiques variées, et réfléchir sur les réponses concrètes qui peuvent participer au mieux vivre ensemble.</p> <p>Cette commission travaille notamment sur un <strong>Atlas de la biodiversité Communale</strong>, en collaboration avec l’Agence Française pour la Biodiversité.</p> <h2>Présentation</h2> <h3>Un Atlas de la biodiversité communale, mais pour quoi faire ?</h3> <p>Chaque atlas est élaboré, à l’échelle communale ou intercommunale, à partir d’un inventaire précis et cartographié des habitats, de la faune et de la flore.</p> <p>Ces atlas ont pour objectifs de :</p> <ul> <li><strong>Sensibiliser et mobiliser</strong> les élus, les acteurs socio-économiques et les citoyens à la biodiversité.</li> <li><strong>Mieux connaître</strong> la biodiversité sur le territoire d’une commune et identifier les enjeux spécifiques liés.</li> <li><strong>Faciliter la prise en compte</strong> de la biodiversité lors de la mise en place des politiques locales.</li> </ul> <p>Cette démarche est soutenue par l’Agence française pour la biodiversité.</p> <h2>Résultats</h2> <p>Ce projet comprend deux composantes principales :</p> <h3>1. La réalisation d’un inventaire</h3> <p>Celui-ci a été réalisé courant 2019 par le bureau d’étude <strong>EcoloGIE</strong>. Il permet de répertorier les espèces et de préciser les secteurs méritant une protection complémentaire.</p> <p>Retrouvez le document complet : <a href='#'>Pussay ABC Ecolo-GIE.pdf</a></p> <h3>2. Des actions de sensibilisation et de mobilisation citoyenne</h3> <p>Nous avons souhaité que les habitants se sentent concernés. De nombreuses actions ont donc été proposées sur le thème de la biodiversité, animées par des associations locales.</p> <p>Complément d'inventaire : <a href='#'>Pussay complément messicoles - Ecolo GIE.pdf</a></p>",
        "on_line": True,
        "revision": False
    }
    response = client.post("/publication/new",
                           json=publication,
                           headers=headers_with_token)
    assert response.status_code == 403
    publications: dict = response.json.get("error")
    assert publications == 'Your title already exists!'

    publication = {
        "title": "My First Publication-test-usere",
        "slug": "my-first-publication-test-user",
        "description": "This is a sample publication for testing purposes.",
        "content":
        "<h2>Qu’est-ce que c’est ?</h2> <p>La transition écologique est une évolution vers un nouveau modèle économique et social, un modèle de développement durable qui renouvelle nos façons de consommer, de produire, de travailler, de vivre ensemble pour répondre aux grands enjeux environnementaux : changement climatique, rareté des ressources, perte accélérée de la biodiversité et multiplication des risques sanitaires environnementaux.</p> <p>Cela regroupe donc un ensemble de principes, fondés sur les problématiques de résilience locale, d’économie circulaire et de réduction des émissions de CO2.</p> <h2>À Pussay</h2> <p>Pour répondre aux enjeux de la transition écologique de notre commune, la municipalité a mis en place une commission dédiée. Celle-ci, composée d’élus et de citoyens concernés et motivés, se réunit régulièrement pour aborder des thématiques variées, et réfléchir sur les réponses concrètes qui peuvent participer au mieux vivre ensemble.</p> <p>Cette commission travaille notamment sur un <strong>Atlas de la biodiversité Communale</strong>, en collaboration avec l’Agence Française pour la Biodiversité.</p> <h2>Présentation</h2> <h3>Un Atlas de la biodiversité communale, mais pour quoi faire ?</h3> <p>Chaque atlas est élaboré, à l’échelle communale ou intercommunale, à partir d’un inventaire précis et cartographié des habitats, de la faune et de la flore.</p> <p>Ces atlas ont pour objectifs de :</p> <ul> <li><strong>Sensibiliser et mobiliser</strong> les élus, les acteurs socio-économiques et les citoyens à la biodiversité.</li> <li><strong>Mieux connaître</strong> la biodiversité sur le territoire d’une commune et identifier les enjeux spécifiques liés.</li> <li><strong>Faciliter la prise en compte</strong> de la biodiversité lors de la mise en place des politiques locales.</li> </ul> <p>Cette démarche est soutenue par l’Agence française pour la biodiversité.</p> <h2>Résultats</h2> <p>Ce projet comprend deux composantes principales :</p> <h3>1. La réalisation d’un inventaire</h3> <p>Celui-ci a été réalisé courant 2019 par le bureau d’étude <strong>EcoloGIE</strong>. Il permet de répertorier les espèces et de préciser les secteurs méritant une protection complémentaire.</p> <p>Retrouvez le document complet : <a href='#'>Pussay ABC Ecolo-GIE.pdf</a></p> <h3>2. Des actions de sensibilisation et de mobilisation citoyenne</h3> <p>Nous avons souhaité que les habitants se sentent concernés. De nombreuses actions ont donc été proposées sur le thème de la biodiversité, animées par des associations locales.</p> <p>Complément d'inventaire : <a href='#'>Pussay complément messicoles - Ecolo GIE.pdf</a></p>",
        "on_line": True,
        "revision": False
    }
    response = client.post("/publication/new",
                           json=publication,
                           headers=headers_with_token)
    assert response.status_code == 403
    publications: dict = response.json.get("error")
    assert publications == 'Your slug does exist!'


# -publication-------------------PUT
def test_publication_new_not_logged(client, headers):
    # global ADMIN_TOKEN
    # headers_with_token = headers
    # headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    # response = client.get("/publications", headers=headers_with_token)
    publication = {
        "title": "My First Publication-test-user",
        "slug": "my-first-publication-test-user",
        "description": "This is a sample publication for testing purposes.",
        "content":
        "<h2>Qu’est-ce que c’est ?</h2> <p>La transition écologique est une évolution vers un nouveau modèle économique et social, un modèle de développement durable qui renouvelle nos façons de consommer, de produire, de travailler, de vivre ensemble pour répondre aux grands enjeux environnementaux : changement climatique, rareté des ressources, perte accélérée de la biodiversité et multiplication des risques sanitaires environnementaux.</p> <p>Cela regroupe donc un ensemble de principes, fondés sur les problématiques de résilience locale, d’économie circulaire et de réduction des émissions de CO2.</p> <h2>À Pussay</h2> <p>Pour répondre aux enjeux de la transition écologique de notre commune, la municipalité a mis en place une commission dédiée. Celle-ci, composée d’élus et de citoyens concernés et motivés, se réunit régulièrement pour aborder des thématiques variées, et réfléchir sur les réponses concrètes qui peuvent participer au mieux vivre ensemble.</p> <p>Cette commission travaille notamment sur un <strong>Atlas de la biodiversité Communale</strong>, en collaboration avec l’Agence Française pour la Biodiversité.</p> <h2>Présentation</h2> <h3>Un Atlas de la biodiversité communale, mais pour quoi faire ?</h3> <p>Chaque atlas est élaboré, à l’échelle communale ou intercommunale, à partir d’un inventaire précis et cartographié des habitats, de la faune et de la flore.</p> <p>Ces atlas ont pour objectifs de :</p> <ul> <li><strong>Sensibiliser et mobiliser</strong> les élus, les acteurs socio-économiques et les citoyens à la biodiversité.</li> <li><strong>Mieux connaître</strong> la biodiversité sur le territoire d’une commune et identifier les enjeux spécifiques liés.</li> <li><strong>Faciliter la prise en compte</strong> de la biodiversité lors de la mise en place des politiques locales.</li> </ul> <p>Cette démarche est soutenue par l’Agence française pour la biodiversité.</p> <h2>Résultats</h2> <p>Ce projet comprend deux composantes principales :</p> <h3>1. La réalisation d’un inventaire</h3> <p>Celui-ci a été réalisé courant 2019 par le bureau d’étude <strong>EcoloGIE</strong>. Il permet de répertorier les espèces et de préciser les secteurs méritant une protection complémentaire.</p> <p>Retrouvez le document complet : <a href='#'>Pussay ABC Ecolo-GIE.pdf</a></p> <h3>2. Des actions de sensibilisation et de mobilisation citoyenne</h3> <p>Nous avons souhaité que les habitants se sentent concernés. De nombreuses actions ont donc été proposées sur le thème de la biodiversité, animées par des associations locales.</p> <p>Complément d'inventaire : <a href='#'>Pussay complément messicoles - Ecolo GIE.pdf</a></p>",
        "on_line": True,
        "revision": False
    }
    response = client.put("/publication/new", json=publication)
    assert response.status_code == 401
    # publications: dict = response.json.get("publications")
    # assert publications[0]['author_email'] == "user1@mail.com"


def test_publication_new_user_logged(client, headers):
    global USER_TOKEN
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + USER_TOKEN
    # response = client.get("/publications", headers=headers_with_token)
    publication = {
        "title": "My First Publication-test-user",
        "slug": "my-first-publication-test-user",
        "description": "This is a sample publication for testing purposes.",
        "content":
        "<h2>Qu’est-ce que c’est ?</h2> <p>La transition écologique est une évolution vers un nouveau modèle économique et social, un modèle de développement durable qui renouvelle nos façons de consommer, de produire, de travailler, de vivre ensemble pour répondre aux grands enjeux environnementaux : changement climatique, rareté des ressources, perte accélérée de la biodiversité et multiplication des risques sanitaires environnementaux.</p> <p>Cela regroupe donc un ensemble de principes, fondés sur les problématiques de résilience locale, d’économie circulaire et de réduction des émissions de CO2.</p> <h2>À Pussay</h2> <p>Pour répondre aux enjeux de la transition écologique de notre commune, la municipalité a mis en place une commission dédiée. Celle-ci, composée d’élus et de citoyens concernés et motivés, se réunit régulièrement pour aborder des thématiques variées, et réfléchir sur les réponses concrètes qui peuvent participer au mieux vivre ensemble.</p> <p>Cette commission travaille notamment sur un <strong>Atlas de la biodiversité Communale</strong>, en collaboration avec l’Agence Française pour la Biodiversité.</p> <h2>Présentation</h2> <h3>Un Atlas de la biodiversité communale, mais pour quoi faire ?</h3> <p>Chaque atlas est élaboré, à l’échelle communale ou intercommunale, à partir d’un inventaire précis et cartographié des habitats, de la faune et de la flore.</p> <p>Ces atlas ont pour objectifs de :</p> <ul> <li><strong>Sensibiliser et mobiliser</strong> les élus, les acteurs socio-économiques et les citoyens à la biodiversité.</li> <li><strong>Mieux connaître</strong> la biodiversité sur le territoire d’une commune et identifier les enjeux spécifiques liés.</li> <li><strong>Faciliter la prise en compte</strong> de la biodiversité lors de la mise en place des politiques locales.</li> </ul> <p>Cette démarche est soutenue par l’Agence française pour la biodiversité.</p> <h2>Résultats</h2> <p>Ce projet comprend deux composantes principales :</p> <h3>1. La réalisation d’un inventaire</h3> <p>Celui-ci a été réalisé courant 2019 par le bureau d’étude <strong>EcoloGIE</strong>. Il permet de répertorier les espèces et de préciser les secteurs méritant une protection complémentaire.</p> <p>Retrouvez le document complet : <a href='#'>Pussay ABC Ecolo-GIE.pdf</a></p> <h3>2. Des actions de sensibilisation et de mobilisation citoyenne</h3> <p>Nous avons souhaité que les habitants se sentent concernés. De nombreuses actions ont donc été proposées sur le thème de la biodiversité, animées par des associations locales.</p> <p>Complément d'inventaire : <a href='#'>Pussay complément messicoles - Ecolo GIE.pdf</a></p>",
        "on_line": True,
        "revision": False
    }
    response = client.post("/publication/new",
                           json=publication,
                           headers=headers_with_token)
    assert response.status_code == 200
    publications: dict = response.json.get("message")
    assert publications == "my-first-publication-test-user"


def test_publication_new_user_logged_already_exist(client, headers):
    global USER_TOKEN
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + USER_TOKEN
    # response = client.get("/publications", headers=headers_with_token)
    publication = {
        "title": "My First Publication-test-user",
        "slug": "my-first-publication-test-user",
        "description": "This is a sample publication for testing purposes.",
        "content":
        "<h2>Qu’est-ce que c’est ?</h2> <p>La transition écologique est une évolution vers un nouveau modèle économique et social, un modèle de développement durable qui renouvelle nos façons de consommer, de produire, de travailler, de vivre ensemble pour répondre aux grands enjeux environnementaux : changement climatique, rareté des ressources, perte accélérée de la biodiversité et multiplication des risques sanitaires environnementaux.</p> <p>Cela regroupe donc un ensemble de principes, fondés sur les problématiques de résilience locale, d’économie circulaire et de réduction des émissions de CO2.</p> <h2>À Pussay</h2> <p>Pour répondre aux enjeux de la transition écologique de notre commune, la municipalité a mis en place une commission dédiée. Celle-ci, composée d’élus et de citoyens concernés et motivés, se réunit régulièrement pour aborder des thématiques variées, et réfléchir sur les réponses concrètes qui peuvent participer au mieux vivre ensemble.</p> <p>Cette commission travaille notamment sur un <strong>Atlas de la biodiversité Communale</strong>, en collaboration avec l’Agence Française pour la Biodiversité.</p> <h2>Présentation</h2> <h3>Un Atlas de la biodiversité communale, mais pour quoi faire ?</h3> <p>Chaque atlas est élaboré, à l’échelle communale ou intercommunale, à partir d’un inventaire précis et cartographié des habitats, de la faune et de la flore.</p> <p>Ces atlas ont pour objectifs de :</p> <ul> <li><strong>Sensibiliser et mobiliser</strong> les élus, les acteurs socio-économiques et les citoyens à la biodiversité.</li> <li><strong>Mieux connaître</strong> la biodiversité sur le territoire d’une commune et identifier les enjeux spécifiques liés.</li> <li><strong>Faciliter la prise en compte</strong> de la biodiversité lors de la mise en place des politiques locales.</li> </ul> <p>Cette démarche est soutenue par l’Agence française pour la biodiversité.</p> <h2>Résultats</h2> <p>Ce projet comprend deux composantes principales :</p> <h3>1. La réalisation d’un inventaire</h3> <p>Celui-ci a été réalisé courant 2019 par le bureau d’étude <strong>EcoloGIE</strong>. Il permet de répertorier les espèces et de préciser les secteurs méritant une protection complémentaire.</p> <p>Retrouvez le document complet : <a href='#'>Pussay ABC Ecolo-GIE.pdf</a></p> <h3>2. Des actions de sensibilisation et de mobilisation citoyenne</h3> <p>Nous avons souhaité que les habitants se sentent concernés. De nombreuses actions ont donc été proposées sur le thème de la biodiversité, animées par des associations locales.</p> <p>Complément d'inventaire : <a href='#'>Pussay complément messicoles - Ecolo GIE.pdf</a></p>",
        "on_line": True,
        "revision": False
    }
    response = client.post("/publication/new",
                           json=publication,
                           headers=headers_with_token)
    assert response.status_code == 403
    publications: dict = response.json.get("error")
    assert publications == 'Your title already exists!'

    publication = {
        "title": "My First Publication-test-usere",
        "slug": "my-first-publication-test-user",
        "description": "This is a sample publication for testing purposes.",
        "content":
        "<h2>Qu’est-ce que c’est ?</h2> <p>La transition écologique est une évolution vers un nouveau modèle économique et social, un modèle de développement durable qui renouvelle nos façons de consommer, de produire, de travailler, de vivre ensemble pour répondre aux grands enjeux environnementaux : changement climatique, rareté des ressources, perte accélérée de la biodiversité et multiplication des risques sanitaires environnementaux.</p> <p>Cela regroupe donc un ensemble de principes, fondés sur les problématiques de résilience locale, d’économie circulaire et de réduction des émissions de CO2.</p> <h2>À Pussay</h2> <p>Pour répondre aux enjeux de la transition écologique de notre commune, la municipalité a mis en place une commission dédiée. Celle-ci, composée d’élus et de citoyens concernés et motivés, se réunit régulièrement pour aborder des thématiques variées, et réfléchir sur les réponses concrètes qui peuvent participer au mieux vivre ensemble.</p> <p>Cette commission travaille notamment sur un <strong>Atlas de la biodiversité Communale</strong>, en collaboration avec l’Agence Française pour la Biodiversité.</p> <h2>Présentation</h2> <h3>Un Atlas de la biodiversité communale, mais pour quoi faire ?</h3> <p>Chaque atlas est élaboré, à l’échelle communale ou intercommunale, à partir d’un inventaire précis et cartographié des habitats, de la faune et de la flore.</p> <p>Ces atlas ont pour objectifs de :</p> <ul> <li><strong>Sensibiliser et mobiliser</strong> les élus, les acteurs socio-économiques et les citoyens à la biodiversité.</li> <li><strong>Mieux connaître</strong> la biodiversité sur le territoire d’une commune et identifier les enjeux spécifiques liés.</li> <li><strong>Faciliter la prise en compte</strong> de la biodiversité lors de la mise en place des politiques locales.</li> </ul> <p>Cette démarche est soutenue par l’Agence française pour la biodiversité.</p> <h2>Résultats</h2> <p>Ce projet comprend deux composantes principales :</p> <h3>1. La réalisation d’un inventaire</h3> <p>Celui-ci a été réalisé courant 2019 par le bureau d’étude <strong>EcoloGIE</strong>. Il permet de répertorier les espèces et de préciser les secteurs méritant une protection complémentaire.</p> <p>Retrouvez le document complet : <a href='#'>Pussay ABC Ecolo-GIE.pdf</a></p> <h3>2. Des actions de sensibilisation et de mobilisation citoyenne</h3> <p>Nous avons souhaité que les habitants se sentent concernés. De nombreuses actions ont donc été proposées sur le thème de la biodiversité, animées par des associations locales.</p> <p>Complément d'inventaire : <a href='#'>Pussay complément messicoles - Ecolo GIE.pdf</a></p>",
        "on_line": True,
        "revision": False
    }
    response = client.post("/publication/new",
                           json=publication,
                           headers=headers_with_token)
    assert response.status_code == 403
    publications: dict = response.json.get("error")
    assert publications == 'Your slug already exists!'


# -publication-------------------delete
def test_publication_delete_user_logged(client, headers):
    global USER_TOKEN
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + USER_TOKEN
    # response = client.get("/publications", headers=headers_with_token)
    publication = {"title": "My First Publication-test-user"}
    response = client.delete("/publication/delete",
                             json=publication,
                             headers=headers_with_token)
    assert response.status_code == 200
    assert response.json.get("delete") == "my-first-publication-test-user"
    # publications: dict = response.json.get("publications")
    # assert publications[0]['author_email'] == "user1@mail.com"


# ---------------------publication---------------------
def test_publication_category_get_visiteur(client):
    response = client.get('/category')
    data: list = response.json

    for category in data:
        assert category['role'] == None
    assert response.status_code == 200


def test_publication_category_get_user(client, headers):
    global USER_TOKEN
    headers_with_token = headers
    headers_with_token['Authorization'] = f'Bearer {USER_TOKEN}'
    response = client.get('/category', headers=headers_with_token)
    data: list = response.json

    for category in data:
        assert category['role'] == None or 'ROLE_USER'
    assert response.status_code == 200


def test_publication_category_get_admin(client, headers):
    global ADMIN_TOKEN
    headers_with_token = headers
    headers_with_token['Authorization'] = f'Bearer {ADMIN_TOKEN}'
    response = client.get('/category', headers=headers_with_token)
    data: list = response.json

    for category in data:
        assert category['role'] == None or 'ROLE_USER' or 'ROLE_ADMIN'
    assert response.status_code == 200


def test_publication_category_post_visiteur(client):
    data: dict = {
        "name": "Technology to delete",
        "no": 0,
        "parent": "Technology",
        "role": "ROLE_ADMIN",
        "url": "/technology/to_delete"
    }
    response = client.post('/category', json=data)
    assert response.json.get('msg') == 'Missing Authorization Header'
    assert response.status_code == 401


def test_publication_category_post_user(client, headers):
    global USER_TOKEN
    headers_with_token = headers
    headers_with_token['Authorization'] = f'Bearer {USER_TOKEN}'
    data: dict = {
        "name": "Technology to delete",
        "no": 0,
        "parent": "Technology",
        "role": "ROLE_ADMIN",
        "url": "/technology/to_delete"
    }
    response = client.post('/category', json=data, headers=headers_with_token)
    assert response.json.get('error') == 'Access Denied'
    assert response.status_code == 403


def test_publication_category_post_admin(client, headers):
    global ADMIN_TOKEN
    headers_with_token = headers
    headers_with_token['Authorization'] = f'Bearer {ADMIN_TOKEN}'
    data: dict = {
        "name": "Technology to delete",
        "no": 0,
        "parent": "Technology",
        "role": "ROLE_ADMIN",
        "url": "/technology/to_delete"
    }
    response = client.post('/category', json=data, headers=headers_with_token)
    assert response.json.get('category') == "Technology to delete"
    assert response.status_code == 200


def test_publication_category_put_visiteur(client):
    data: dict = {
        "category": "Technology to delete",
        "data": {
            "name": "Technology Put",
            "no": 0,
            "parent": "Technology",
            "role": "ROLE_ADMIN",
            "url": "/technology/to_delete"
        }
    }
    response = client.put('/category', json=data)
    assert response.json.get('msg') == 'Missing Authorization Header'
    assert response.status_code == 401


def test_publication_category_put_user(client, headers):
    global USER_TOKEN
    headers_with_token = headers
    headers_with_token['Authorization'] = f'Bearer {USER_TOKEN}'
    data: dict = {
        "category": "Technology to delete",
        "data": {
            "name": "Technology Put",
            "no": 0,
            "parent": "Technology",
            "role": "ROLE_ADMIN",
            "url": "/technology/to_delete"
        }
    }
    response = client.put('/category', json=data, headers=headers_with_token)
    assert response.json.get('error') == 'Access Denied'
    assert response.status_code == 403


def test_publication_category_put_admin(client, headers):
    global ADMIN_TOKEN
    headers_with_token = headers
    headers_with_token['Authorization'] = f'Bearer {ADMIN_TOKEN}'
    data: dict = {
        "category": "Technology to delete",
        "data": {
            "name": "Technology Put",
            "no": 0,
            "parent": "Technology",
            "role": "ROLE_ADMIN",
            "url": "/technology/to_delete"
        }
    }
    response = client.put('/category', json=data, headers=headers_with_token)
    assert response.json.get('category') == "Technology Put"
    assert response.status_code == 200


def test_publication_category_delete_visiteur(client):
    data: dict = {"name": "Technology to delete"}
    response = client.delete('/category', json=data)
    assert response.json.get('msg') == 'Missing Authorization Header'
    assert response.status_code == 401


def test_publication_category_delete_user(client, headers):
    global USER_TOKEN
    headers_with_token = headers
    headers_with_token['Authorization'] = f'Bearer {USER_TOKEN}'
    data: dict = {"name": "Technology to delete"}
    response = client.delete('/category',
                             json=data,
                             headers=headers_with_token)
    assert response.json.get('error') == 'Access Denied'
    assert response.status_code == 403


def test_publication_category_delete_admin(client, headers):
    global ADMIN_TOKEN
    headers_with_token = headers
    headers_with_token['Authorization'] = f'Bearer {ADMIN_TOKEN}'
    data: dict = {"name": "Technology Put"}
    response = client.delete('/category',
                             json=data,
                             headers=headers_with_token)
    assert response.json.get('category') == "Technology Put"
    assert response.status_code == 200


# ---------------------publication---------------------
# ---------------------home_page_content---------------------
def test_home_page_content_get(client, headers):
    response = client.get('/home_page_content')
    assert response.status_code == 200

    global USER_TOKEN
    headers_with_token = headers
    headers_with_token['Authorization'] = f'Bearer {USER_TOKEN}'
    response = client.get('/home_page_content', headers=headers_with_token)
    assert response.status_code == 200

    global ADMIN_TOKEN
    headers_with_token = headers
    headers_with_token['Authorization'] = f'Bearer {ADMIN_TOKEN}'
    response = client.get('/home_page_content', headers=headers_with_token)
    assert response.status_code == 200


def test_home_page_content_post(client, headers):
    data: dict = {
        "name": "test",
        "element": "#test",
        "description": "test",
        "publication": None
    }
    response = client.post('/home_page_content', json=data)
    assert response.json.get('msg') == 'Missing Authorization Header'
    assert response.status_code == 401

    global USER_TOKEN
    headers_with_token = headers
    headers_with_token['Authorization'] = f'Bearer {USER_TOKEN}'
    response = client.post('/home_page_content',
                           json=data,
                           headers=headers_with_token)
    assert response.json.get('error') == 'Access Denied'
    assert response.status_code == 403

    global ADMIN_TOKEN
    headers_with_token = headers
    headers_with_token['Authorization'] = f'Bearer {ADMIN_TOKEN}'
    response = client.post('/home_page_content',
                           json=data,
                           headers=headers_with_token)
    assert response.json.get('home_page_content') == "test"
    assert response.status_code == 200


def test_home_page_content_put(client, headers):
    data: dict = {
        "name": "test",
        "put": {
            "name": "test_put",
            "element": "#test_put",
            "description": "test",
            "publication": None
        }
    }
    response = client.put('/home_page_content', json=data)
    assert response.json.get('msg') == 'Missing Authorization Header'
    assert response.status_code == 401

    global USER_TOKEN
    headers_with_token = headers
    headers_with_token['Authorization'] = f'Bearer {USER_TOKEN}'
    response = client.put('/home_page_content',
                          json=data,
                          headers=headers_with_token)
    assert response.json.get('error') == 'Access Denied'
    assert response.status_code == 403

    global ADMIN_TOKEN
    headers_with_token = headers
    headers_with_token['Authorization'] = f'Bearer {ADMIN_TOKEN}'
    response = client.put('/home_page_content',
                          json=data,
                          headers=headers_with_token)
    assert response.json.get('home_page_content') == "test_put"
    assert response.status_code == 200


def test_home_page_content_delete(client, headers):
    data: dict = {"name": "test_put"}
    response = client.delete('/home_page_content', json=data)
    assert response.json.get('msg') == 'Missing Authorization Header'
    assert response.status_code == 401

    global USER_TOKEN
    headers_with_token = headers
    headers_with_token['Authorization'] = f'Bearer {USER_TOKEN}'
    response = client.delete('/home_page_content',
                             json=data,
                             headers=headers_with_token)
    assert response.json.get('error') == 'Access Denied'
    assert response.status_code == 403

    global ADMIN_TOKEN
    headers_with_token = headers
    headers_with_token['Authorization'] = f'Bearer {ADMIN_TOKEN}'
    response = client.delete('/home_page_content',
                             json=data,
                             headers=headers_with_token)
    assert response.json.get('home_page_content') == "test_put"
    assert response.status_code == 200


# ---------------------home_page_content---------------------


# -user-------------------delete
def test_user_delete_admin(client, headers):
    """
    Teste la suppression d'un utilisateur par un administrateur.

    - Envoie une requête DELETE à l'endpoint `/user/delete` avec un jeton d'administrateur.
    - Vérifie que le statut de la réponse est 200.
    """
    global ADMIN_TOKEN
    user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + ADMIN_TOKEN
    response = client.delete("/user/delete",
                             json=user_know,
                             headers=headers_with_token)
    assert response.status_code == 200


def test_user_delete_admin_user_not_know(client, headers):
    """
    Teste la suppression d'un utilisateur inexistant par un administrateur.

    - Envoie une requête DELETE à l'endpoint `/user/delete` avec un jeton d'administrateur.
    - Vérifie que le statut de la réponse est 404.
    - Vérifie que le message d'erreur est "Email unknow@gmail.com not found".
    """
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
    """
    Teste la suppression d'un utilisateur avec un format d'email incorrect par un administrateur.

    - Envoie une requête DELETE à l'endpoint `/user/delete` avec un jeton d'administrateur.
    - Vérifie que le statut de la réponse est 415.
    - Vérifie que le message d'erreur est "Email not valid".
    """
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
    """
    Teste la suppression d'un utilisateur par un utilisateur non administrateur.

    - Envoie une requête DELETE à l'endpoint `/user/delete` avec un jeton d'utilisateur.
    - Vérifie que le statut de la réponse est 403.
    """
    global USER_TOKEN
    user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    headers_with_token["Authorization"] = "Bearer " + USER_TOKEN
    response = client.delete("/user/delete",
                             json=user_know,
                             headers=headers_with_token)
    assert response.status_code == 403


def test_user_delete_not_logged(client, headers):
    """
    Teste la suppression d'un utilisateur sans être connecté.

    - Envoie une requête DELETE à l'endpoint `/user/delete` sans jeton d'authentification.
    - Vérifie que le statut de la réponse est 401.
    - Vérifie que le message d'erreur est "Missing Authorization Header".
    """
    user_know = {"email": "test@gmail.com"}
    headers_with_token = headers
    response = client.get("/user/delete",
                          json=user_know,
                          headers=headers_with_token)
    assert response.status_code == 401
    assert response.json.get("msg") == "Missing Authorization Header"
