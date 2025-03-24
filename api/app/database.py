from sqlalchemy import create_engine  # Pour créer une connexion avec la base de données
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base  # Modules pour gérer les sessions et les modèles ORM

# Définition de l'engine SQLAlchemy
# Remarque : Ce paramètre pourrait être déplacé dans un fichier de configuration, mais ici, il est codé en dur.
engine = create_engine('sqlite:///cnam_projet.db')
"""
L'engine représente la connexion avec la base de données.
- Ici, la base est SQLite et le fichier s'appelle "cnam_projet.db".
- Si tu veux utiliser une autre base (PostgreSQL, MySQL, etc.), tu peux modifier l'URL ici.
"""

# Configuration de la session de base de données
db_session = scoped_session(
    sessionmaker(
        autocommit=
        False,  # Les modifications ne seront pas automatiquement validées (commit).
        autoflush=
        False,  # Empêche le "flush" automatique des modifications avant les requêtes.
        bind=engine  # L'engine est utilisé pour établir les connexions.
    ))
"""
La session permet de gérer les interactions avec la base de données.
- `scoped_session` : Assure que chaque thread (ou processus) utilise une session indépendante.
"""

# Définition de la base de données pour les modèles ORM
Base = declarative_base()
"""
`Base` est la classe de base pour tous les modèles définis avec SQLAlchemy.
Elle contient les métadonnées nécessaires pour mapper les classes Python aux tables de la base de données.
"""

# Ajout d'une propriété de requête aux classes héritant de Base
Base.query = db_session.query_property()
"""
Cette ligne ajoute une méthode de requête directement accessible sur les modèles.
Par exemple : `User.query.filter_by(name='Alice')`
"""


# Fonction pour initialiser la base de données
def init_db():
    """
    Initialise la base de données en créant toutes les tables définies dans les modèles.
    - Cette fonction importe les modèles pour s'assurer qu'ils sont enregistrés dans les métadonnées.
    - Ensuite, elle crée les tables dans la base de données si elles n'existent pas encore.
    """
    # Import des modèles pour enregistrer les tables dans les métadonnées
    from app.models import user, test
    # Création des tables dans la base de données
    Base.metadata.create_all(bind=engine)
    """
    - `Base.metadata.create_all` : Parcourt toutes les tables définies dans les modèles et les crée si elles n'existent pas.
    - `bind=engine` : Indique à SQLAlchemy d'utiliser la connexion définie dans `engine`.
    """
