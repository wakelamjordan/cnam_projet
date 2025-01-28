from . import app  # Import de l'application Flask
from flask import jsonify  # Pour renvoyer des réponses JSON
from app.models.user import User  # Import du modèle User


# Route pour récupérer un utilisateur par son nom
@app.route("/user/<name>", methods=['GET'])
def hello_world(name):
    """
    Recherche un utilisateur par son nom et retourne ses données en JSON.

    Paramètres :
    ----------
    name : str
        Le nom de l'utilisateur passé dans l'URL.

    Retour :
    -------
    JSON : Les données de l'utilisateur ou une erreur 404 si non trouvé.
    """
    u = User.query.filter_by(name=name).first()  # Recherche l'utilisateur
    if u is None:
        return jsonify({"error": "User not found"
                        }), 404  # Erreur si aucun utilisateur n'est trouvé
    return jsonify(
        u.to_dict())  # Retourne les données de l'utilisateur en JSON


# Route pour tester une requête SQL brute
@app.route("/test")
def test():
    """
    Exécute une requête SQL brute pour récupérer les utilisateurs nommés "toto".

    Retour :
    -------
    JSON : Les données des utilisateurs trouvés ou une erreur 404 si aucun résultat.
    """
    u = User.query_sql('select * from users where name = :name',
                       {'name': 'admin'})  # Requête SQL brute
    if not u:
        return jsonify({"error": "No users found"
                        }), 404  # Erreur si aucun utilisateur n'est trouvé
    return jsonify(u)  # Retourne les résultats en JSON
