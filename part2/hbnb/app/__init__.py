"""
Module d'initialisation de l'application HBnB.
Ce module configure l'application Flask et l'API REST avec Flask-RESTX.
Il enregistre tous les points d'entrée (endpoints) de l'API et met en place
la documentation Swagger pour faciliter l'utilisation et les tests de l'API.
"""

from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

def create_app():
    """
    Crée et configure l'instance de l'application Flask.
    
    Cette fonction effectue les opérations suivantes :
    1. Initialise une nouvelle application Flask
    2. Configure l'API REST avec Flask-RESTX
    3. Enregistre tous les espaces de noms (namespaces) de l'API :
       - /api/v1/users : Gestion des utilisateurs
       - /api/v1/amenities : Gestion des équipements
       - /api/v1/places : Gestion des lieux
       - /api/v1/reviews : Gestion des avis
    4. Configure la documentation Swagger accessible à /api/v1/
    
    Returns:
        Flask: L'application Flask configurée et prête à être exécutée
    """
    # Création de l'instance Flask avec le nom du module actuel
    app = Flask(__name__)
    
    # Configuration de l'API avec Flask-RESTX
    # Définition des métadonnées de l'API qui apparaîtront dans la documentation
    api = Api(app, 
             version='1.0',  # Version de l'API
             title='HBnB API',  # Titre de l'API
             description='API de l\'application HBnB pour la gestion des hébergements',
             doc='/api/v1/')  # URL de la documentation Swagger

    # Enregistrement des espaces de noms de l'API
    # Chaque espace de noms correspond à une ressource distincte
    api.add_namespace(users_ns, path='/api/v1/users')         # Endpoints pour la gestion des utilisateurs
    api.add_namespace(amenities_ns, path='/api/v1/amenities') # Endpoints pour la gestion des équipements
    api.add_namespace(places_ns, path='/api/v1/places')       # Endpoints pour la gestion des lieux
    api.add_namespace(reviews_ns, path='/api/v1/reviews')     # Endpoints pour la gestion des avis

    return app 