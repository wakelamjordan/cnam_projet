import pytest
from app import create_app
from app.models.user_model import User
import os

from urllib.parse import urlencode


@pytest.fixture
def client():
    """Fixture pour créer un client de test Flask."""

    os.environ["FLASK_ENV"] = "testing"
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def headers():
    headers = {"Content-Type": "application/json"}
    yield headers


@pytest.fixture
def list_users_ok():
    list_users_ok = list_users_ok = [
        "test@gmail.com", "test1@gmail.com", "test2@gmail.com",
        "test3@gmail.com"
    ]
    yield list_users_ok


@pytest.fixture
def list_user_not_ok():
    list_user_not_ok = [
        "test@@gmail.com", "test@1@gmail.com", "usercom", "user@com"
    ]
    yield list_user_not_ok


def test_user_controller_index_new(client, headers, list_users_ok,
                                   list_user_not_ok):

    for email in list_users_ok:
        # u = User(email)

        # 🚀 Supprimer le patch pour tester réellement la base de données
        # mocker.patch("app.controllers.user_controller.service_insert",
        #              return_value=u.get_email())

        response = client.post("/user/new",
                               json={"email": email},
                               headers=headers)

        # ✅ Vérifie le code HTTP
        assert response.status_code == 201

        # ✅ Vérifie la structure et la valeur de la réponse
        assert response.json["email"] == email

        response = client.post("/user/new",
                               json={"email": list_users_ok[0]},
                               headers=headers)
        assert response.status_code == 400

        assert response.json["error"] == f"Email {list_users_ok[0]} does exist"

    for email in list_user_not_ok:
        # u = User(email)
        data = {"email": email}

        # mocker.patch("app.controllers.user_controller.service_insert",
        #              side_effect=ValueError("Invalid email format"))

        response = client.post("/user/new", json=data, headers=headers)

        # ✅ Vérifie que l'API renvoie une erreur 400 pour une adresse invalide
        assert response.status_code == 415

        # ✅ Vérifie le message d'erreur
        assert response.json == {"error": "Email not valid"}


def test_user_controller_index_get(client, headers, list_users_ok):
    # for i in range(len(list_users)):
    #     u: User = User(list_users[i])
    #     list_users[i] = u
    # mocker.patch('app.controllers.user_controller.service_find_all',
    #              return_value=list_users)

    response = client.get('/user/')  #get_all

    for i in range(len(list_users_ok)):
        assert response.json[i]["email"] == list_users_ok[i]

    params = urlencode({"email": list_users_ok[0]})
    response = client.get(f'/user/?{params}')  #get_one ok
    # print(response)
    assert response.status_code == 200
    assert response.json["email"] == list_users_ok[0]

    email = "inconu@gmail.com"
    params = urlencode({"email": email})
    response = client.get(f'/user/?{params}')  #get_one not ok
    # print(response)
    assert response.status_code == 404
    assert response.json["error"] == "User not found!"

    response = client.put('/user/',
                          json={
                              "email": list_users_ok[0],
                              "firstname": "modif put",
                              "lastname": "modif put",
                              "birth_at": "1990-07-28"
                          },
                          headers=headers)  # put ok
    assert response.status_code == 200
    assert response.json["email"] == list_users_ok[0]
    assert response.json["firstname"] and response.json[
        "lastname"] == "modif put"

    response = client.patch('/user/',
                            json={
                                "email": list_users_ok[0],
                                "firstname": "modif patch",
                                "lastname": "modif patch",
                                "birth_at": "1990-07-28"
                            },
                            headers=headers)  # patch ok
    assert response.status_code == 200
    assert response.json["email"] == list_users_ok[0]
    assert response.json["firstname"] and response.json[
        "lastname"] == "modif patch"

    response = client.put('/user/',
                          json={
                              "email": "emailnotfound@gmail.com",
                              "firstname": "modif put",
                              "lastname": "modif put",
                              "birth_at": "1990-07-28"
                          },
                          headers=headers)  # put pas ok
    assert response.status_code == 404
    assert response.json["error"] == "Email emailnotfound@gmail.com not found"

    response = client.patch('/user/',
                            json={
                                "email": "emailnotfound@gmail.com",
                                "firstname": "modif patch",
                                "lastname": "modif patch",
                                "birth_at": "1990-07-28"
                            },
                            headers=headers)  # patch pas ok
    assert response.status_code == 404
    assert response.json["error"] == "Email emailnotfound@gmail.com not found"


def test_user_controller_delete(client, headers, list_users_ok):

    for email in list_users_ok:
        response = client.delete("/user/delete",
                                 json={"email": email},
                                 headers=headers)
        response.status_code == 200

    response = client.delete("/user/delete",
                             json={"email": "emailnotfound@gmail.com"})
    assert response.status_code == 404
