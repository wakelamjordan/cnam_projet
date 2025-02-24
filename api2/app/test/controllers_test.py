import pytest
from app import create_app
from app.models.user_model import User


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


def test_user_new_ok(client, mocker, headers,
                     u: User = User("test@gmail.com")):
    # 🔹 Données à envoyer dans la requête
    data = {"email": u.get_email()}

    # ✅ Patch correctement la méthode `service_insert`
    mocker.patch("app.controllers.user_controller.service_insert",
                 return_value=u.get_email())

    # # 🔹 Headers pour indiquer qu'on envoie du JSON
    # headers = {"Content-Type": "application/json"}

    # 🔹 Envoie la requête POST
    response = client.post("/user/new", json=data, headers=headers)

    # return response

    # ✅ Vérifie le code HTTP
    assert response.status_code == 201

    # ✅ Vérifie la structure et la valeur de la réponse
    assert response.json == data


def test_user_new_not_ok(client, mocker, headers):
    """Test insertion utilisateur avec un email invalide"""
    invalid_emails = [
        "test@@gmail.com", "test@1@gmail.com", "user@.com", "user@com"
    ]

    for email in invalid_emails:
        data = {"email": email}

        mocker.patch("app.controllers.user_controller.service_insert",
                     side_effect=ValueError("Invalid email format"))

        response = client.post("/user/new", json=data, headers=headers)

        # ✅ Vérifie que l'API renvoie une erreur 400 pour une adresse invalide
        assert response.status_code == 404

        # ✅ Vérifie le message d'erreur
        assert response.json == {"error": "Email not valid"}


def test_user_index_get_all(client, mocker):
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


def test_user_index(client, mocker, headers):

    # 🔹 Emails valides
    list_users_ok = [
        "test@gmail.com", "test1@gmail.com", "test2@gmail.com",
        "test3@gmail.com"
    ]

    # 🔹 Emails invalides
    list_users_not_ok = [
        "test@@gmail.com", "test@1@gmail.com", "user@com", "user@com"
    ]

    for user in list_users_ok:
        u = User(user)
        test_user_new_ok(client, mocker, headers, u)

    for user in list_users_not_ok:
        data = {"email": user}
        mocker.patch("app.controllers.user_controller.service_insert",
                     side_effect=ValueError("Invalid email format"))

        client.post("/user/new", json=data, headers=headers)
