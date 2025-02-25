import pytest
from app import create_app
import os
from urllib.parse import urlencode


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


@pytest.fixture
def list_users_ok():
    """
    Fixture contenant une liste d'adresses email valides pour les tests.
    """
    list_users_ok = [{
        "email": "test@gmail.com",
        "password": "Vdqcw4TympGe3lrKbpUUrN79@"
    }, {
        "email": "test2@gmail.com",
        "password": "Vdqcw4TympGe3lrKbpUUrN79@"
    }, {
        "email": "test3@gmail.com",
        "password": "Vdqcw4TympGe3lrKbpUUrN79@"
    }, {
        "email": "test4@gmail.com",
        "password": "Vdqcw4TympGe3lrKbpUUrN79@"
    }, {
        "email": "test5@gmail.com",
        "password": "Vdqcw4TympGe3lrKbpUUrN79@"
    }]
    yield list_users_ok


@pytest.fixture
def list_user_not_ok():
    """
    Fixture contenant une liste d'adresses email invalides pour tester la validation.
    """
    list_user_not_ok = [{
        "email": "testgmailcom",
        "password": "Vdqcw4TympG"
    }, {
        "email": "test2@@gmail.@com",
        "password": "Vdqcw4TympG"
    }, {
        "email": "test3_t$js@gmail.com",
        "password": "Vdqcw4TympG"
    }, {
        "email": "@test4@gmailcom",
        "password": "Vdqcw4TympG"
    }, {
        "email": "tiiii@@est5@gmailcom",
        "password": "Vdqcw4TympG"
    }]
    yield list_user_not_ok


def test_user_controller_new(client, headers, list_users_ok, list_user_not_ok):
    """
    Teste l'ajout d'un nouvel utilisateur via l'endpoint `/user/new`.
    
    - Vérifie que l'ajout d'un utilisateur valide retourne un code `201 Created`.
    - Vérifie qu'un email déjà existant retourne une erreur `400 Bad Request`.
    - Vérifie que les emails invalides sont rejetés avec un code `415 Unsupported Media Type`.
    """
    for user in list_users_ok:
        response = client.post("/user/new",
                               json={"email": user["email"]},
                               headers=headers)
        assert response.status_code == 201
        assert response.json["email"] == user["email"]

        response = client.post("/user/new",
                               json={"email": list_users_ok[0]["email"]},
                               headers=headers)
        assert response.status_code == 400
        assert response.json["error"] == f"Email {list_users_ok[0]["email"]} does exist"

    for user in list_user_not_ok:
        response = client.post("/user/new",
                               json={"email": user["email"]},
                               headers=headers)
        # assert response.
        assert response.status_code == 415
        assert response.json == {"error": "Email not valid"}


def test_user_controller_index(client, headers, list_users_ok, list_user_not_ok):
    """
    Teste la récupération, la mise à jour et la modification d'un utilisateur via l'endpoint `/user/`.
    
    - Vérifie la récupération de tous les utilisateurs (`GET /user/`).
    - Vérifie la récupération d'un utilisateur spécifique (`GET /user/?email=<email>`).
    - Vérifie les mises à jour (`PUT` et `PATCH`) avec des modifications valides et invalides.
    - Vérifie que la récupération d'un utilisateur inexistant retourne une erreur `404 Not Found`.
    """
    response = client.get('/user/')
    for i in range(len(list_users_ok)):
        assert response.json[i]["email"] == list_users_ok[i]["email"]

    params = urlencode({"email": list_users_ok[0]["email"]})
    response = client.get(f'/user/?{params}')
    assert response.status_code == 200
    assert response.json["email"] == list_users_ok[0]["email"]

    params = urlencode({"email": "inconnu@gmail.com"})
    response = client.get(f'/user/?{params}')
    assert response.status_code == 404
    assert response.json["error"] == "User not found!"

    params = urlencode({"email": "test3_t$js@gmail.com"})
    response = client.get(f'/user/?{params}')
    assert response.status_code == 415
    assert response.json["error"] == "Email not valid"

    response = client.put('/user/',
                          json={
                              "email": list_users_ok[0]["email"],
                              "firstname": "modif put",
                              "lastname": "modif put",
                              "birth_at": "1990-07-28",
                              "password":list_users_ok[0]["password"]
                          },
                          headers=headers)
    assert response.status_code == 200
    assert response.json["firstname"] == "modif put"
    assert response.json["lastname"] == "modif put"

    response = client.patch('/user/',
                            json={
                                "email": list_users_ok[0]["email"],
                                "firstname": "modif patch",
                                "lastname": "modif patch",
                                "birth_at": "1990-07-28",
                                "password":list_users_ok[0]["password"]
                            },
                            headers=headers)
    assert response.status_code == 200
    assert response.json["firstname"] == "modif patch"
    assert response.json["lastname"] == "modif patch"

    response = client.put('/user/',
                          json={
                              "email": "emailnotfound@gmail.com",
                              "firstname": "modif put",
                              "lastname": "modif put",
                              "birth_at": "1990-07-28"
                          },
                          headers=headers)
    assert response.status_code == 404
    assert response.json["error"] == "Email emailnotfound@gmail.com not found"

    response = client.patch('/user/',
                            json={
                                "email": "emailnotfound@gmail.com",
                                "firstname": "modif patch",
                                "lastname": "modif patch",
                                "birth_at": "1990-07-28"
                            },
                            headers=headers)
    assert response.status_code == 404
    assert response.json["error"] == "Email emailnotfound@gmail.com not found"

    response = client.put('/user/',
                          json={
                              "email": "emailnotfound@gmail.com",
                              "firstname": "modif put",
                              "lastname": "modif put",
                              "birth_at": "1990-07-28",
                              "password":list_user_not_ok[0]["password"]
                          },
                          headers=headers)
    assert response.status_code == 415
    assert response.json["error"] == "Password not valid"

    response = client.patch('/user/',
                            json={
                                "email": "emailnotfound@gmail.com",
                                "firstname": "modif patch",
                                "lastname": "modif patch",
                                "birth_at": "1990-07-28",
                                "password":list_user_not_ok[0]["password"]
                            },
                            headers=headers)
    assert response.status_code == 415
    assert response.json["error"] == "Password not valid"


def test_user_controller_delete(client, headers, list_users_ok):
    """
    Teste la suppression d'un utilisateur via l'endpoint `/user/delete`.
    
    - Vérifie que la suppression d'un utilisateur existant retourne un code `200 OK`.
    - Vérifie que la suppression d'un utilisateur inexistant retourne une erreur `404 Not Found`.
    """
    for user in list_users_ok:
        response = client.delete("/user/delete",
                                 json={"email": user["email"]},
                                 headers=headers)
        assert response.status_code == 200

    response = client.delete("/user/delete",
                             json={"email": "emailnotfound@gmail.com"})
    assert response.status_code == 404
