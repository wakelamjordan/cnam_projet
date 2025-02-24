import pytest
from app import create_app
from app.models.user_model import User

from urllib.parse import urlencode


@pytest.fixture
def client():
    """Fixture pour créer un client de test Flask."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def headers():
    headers = {"Content-Type": "application/json"}
    yield headers


def test_user_controller_index_new_ok(client, mocker, headers):
    list_users_ok = [
        "testss@gmail.com", "test1@gmail.com", "test2@gmail.com",
        "test3@gmail.com"
    ]

    for email in list_users_ok:
        u = User(email)

        # 🚀 Supprimer le patch pour tester réellement la base de données
        mocker.patch("app.controllers.user_controller.service_insert",
                     return_value=u.get_email())

        response = client.post("/user/new",
                               json={"email": u.get_email()},
                               headers=headers)

        # ✅ Vérifie le code HTTP
        assert response.status_code == 201

        # ✅ Vérifie la structure et la valeur de la réponse
        assert response.json["email"] == u.get_email()


def test_user_controller_index_new_not_ok(client, mocker, headers):
    """Test insertion utilisateur avec un email invalide"""
    invalid_emails = [
        "test@@gmail.com", "test@1@gmail.com", "usercom", "user@com"
    ]

    for email in invalid_emails:
        # u = User(email)
        data = {"email": email}

        # mocker.patch("app.controllers.user_controller.service_insert",
        #              side_effect=ValueError("Invalid email format"))

        response = client.post("/user/new", json=data, headers=headers)

        # ✅ Vérifie que l'API renvoie une erreur 400 pour une adresse invalide
        assert response.status_code == 404

        # ✅ Vérifie le message d'erreur
        assert response.json == {"error": "Email not valid"}


def test_user_controller_index_get_all(client, mocker):
    list_users = [
        "test@gmail.com", "test1@gmail.com", "test2@gmail.com",
        "test3@gmail.com"
    ]
    for i in range(len(list_users)):
        u: User = User(list_users[i])
        list_users[i] = u
    mocker.patch('app.controllers.user_controller.service_find_all',
                 return_value=list_users)

    response = client.get('/user/')

    assert len(response.json) == len(list_users)


def test_user_controller_index_get_one(client, headers):
    email = "testgmail.com"
    params = urlencode({"email": email})
    response = client.get('/user/?{params}')
    # print(response)
    assert response.json[0]["email"] == email


def test_user_controller_index_update_put(client, headers):
    response = client.put('/user/',
                          json={
                              "email": "test@gmail.com",
                              "firstname": "modif put",
                              "lastname": "modif put",
                              "birth_at": "1990-07-28"
                          },
                          headers=headers)
    assert response.json["email"] == "test@gmail.com"
    assert response.json["firstname"] and response.json[
        "lastname"] == "modif put"


def test_user_controller_index_update_patch(client, headers):
    response = client.put('/user/',
                          json={
                              "email": "test@gmail.com",
                              "firstname": "modif patch",
                              "lastname": "modif patch",
                              "birth_at": "1990-07-28"
                          },
                          headers=headers)
    assert response.json["email"] == "test@gmail.com"
    assert response.json["firstname"] and response.json[
        "lastname"] == "modif patch"


# def test_user_controller_delete(client, mocker,headers):
