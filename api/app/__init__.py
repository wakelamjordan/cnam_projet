from flask import Flask  # Importation de la classe Flask pour créer l'application
from app.manager.database import db_session  # Importation de la session de base de données
from app.config import config  # Importation de la configuration de l'application
import os  # Importation du module os pour gérer les variables d'environnement

# Création de l'instance de l'application Flask
app = Flask(__name__)

# Configuration de l'application
# Charge la configuration appropriée en fonction de l'environnement (développement, production, etc.)
# L'environnement est récupéré à partir de la variable d'environnement FLASK_ENV, sinon 'dev' est utilisé par défaut.
app.config.from_object(config[os.getenv(
    'FLASK_ENV', 'dev')])  # Change 'DevelopmentConfig' selon l'environnement
"""
Ici, la configuration de l'application est choisie en fonction de l'environnement (développement, production, etc.).
- `os.getenv('FLASK_ENV', 'dev')` : Récupère la valeur de la variable d'environnement `FLASK_ENV`. Si elle n'est pas définie, utilise 'dev' (développement) par défaut.
- `config` est un dictionnaire qui contient différentes configurations selon l'environnement (par exemple, `dev`, `prod`).
- `app.config.from_object(...)` charge la configuration dans l'application.
"""

# Importation des routes (pour ne pas créer une dépendance circulaire, elles sont importées après la configuration)
from app.routes import *  # Cette ligne importe toutes les routes définies dans le fichier routes.py


# Teardown de l'application après chaque requête
@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    Cette fonction est appelée après chaque requête pour s'assurer que la session de base de données est fermée correctement.
    Elle est enregistrée via le décorateur `teardown_appcontext`, qui permet d'exécuter du code après la fin de la requête.
    """
    db_session.remove(
    )  # Ferme la session de la base de données pour éviter des fuites de connexion.


"""
- `@app.teardown_appcontext` : Décorateur qui permet de définir des actions à effectuer après chaque requête HTTP.
- `db_session.remove()` : Permet de fermer la session de base de données après la fin de la requête, ce qui libère les ressources.
"""

# Lancement de l'application Flask en mode développement (debug activé)
if __name__ == "__main__":
    app.run(
        debug=True
    )  # Lancer l'application Flask en mode debug pour afficher les erreurs
