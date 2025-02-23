"""
Module de gestion des points de terminaison API pour les lieux (places).
Ce module définit les routes et les modèles pour la gestion CRUD des lieux
dans l'application HBnB, incluant les relations avec les utilisateurs,
les équipements et les avis.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade

# Création d'un espace de noms pour les opérations liées aux lieux
api = Namespace('places', description='Opérations sur les lieux')

# Définition des modèles pour les entités liées
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Identifiant de l\'équipement'),
    'name': fields.String(description='Nom de l\'équipement'),
    'created_at': fields.String(description='Date et heure de création'),
    'updated_at': fields.String(description='Date et heure de dernière modification')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='Identifiant de l\'utilisateur'),
    'first_name': fields.String(description='Prénom du propriétaire'),
    'last_name': fields.String(description='Nom du propriétaire'),
    'email': fields.String(description='Adresse email'),
    'created_at': fields.String(description='Date et heure de création'),
    'updated_at': fields.String(description='Date et heure de dernière modification')
})

# Définition du modèle d'avis pour les réponses des lieux
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Identifiant de l\'avis'),
    'text': fields.String(description='Texte de l\'avis'),
    'rating': fields.Integer(description='Note du lieu (1-5)'),
    'user': fields.Nested(user_model, description='Utilisateur ayant rédigé l\'avis'),
    'place': fields.Nested(api.model('ReviewPlace', {
        'id': fields.String(description='Identifiant du lieu'),
        'title': fields.String(description='Titre du lieu')
    }), description='Lieu concerné par l\'avis'),
    'created_at': fields.String(description='Date et heure de création'),
    'updated_at': fields.String(description='Date et heure de dernière modification')
})

# Définition du modèle de validation pour les lieux
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Titre du lieu'),
    'description': fields.String(description='Description du lieu'),
    'price': fields.Float(required=True, description='Prix par nuit'),
    'latitude': fields.Float(required=True, description='Latitude du lieu'),
    'longitude': fields.Float(required=True, description='Longitude du lieu'),
    'owner_id': fields.String(required=True, description='Identifiant du propriétaire'),
    'amenities': fields.List(fields.String, description="Liste des identifiants d'équipements")
})

# Définition du modèle de réponse pour les lieux
place_response_model = api.model('PlaceResponse', {
    'id': fields.String(description='Identifiant unique du lieu'),
    'title': fields.String(description='Titre du lieu'),
    'description': fields.String(description='Description du lieu'),
    'price': fields.Float(description='Prix par nuit'),
    'latitude': fields.Float(description='Latitude du lieu'),
    'longitude': fields.Float(description='Longitude du lieu'),
    'owner': fields.Nested(user_model, description='Détails du propriétaire'),
    'amenities': fields.List(fields.Nested(amenity_model), description='Liste des équipements'),
    'reviews': fields.List(fields.Nested(review_model), description='Liste des avis'),
    'created_at': fields.String(description='Date et heure de création'),
    'updated_at': fields.String(description='Date et heure de dernière modification')
})

@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_response_model)
    def get(self):
        """
        Liste tous les lieux disponibles.
        Retourne une liste complète des lieux enregistrés dans le système,
        incluant leurs propriétaires, équipements et avis associés.
        """
        places = facade.get_all_places()
        return [place.to_dict() for place in places]

    @api.doc('create_place')
    @api.expect(place_model, validate=True)
    @api.response(201, 'Lieu créé avec succès', place_response_model)
    @api.response(400, 'Données d\'entrée invalides')
    @api.response(404, 'Propriétaire ou équipement non trouvé')
    @api.marshal_with(place_response_model, code=201)
    def post(self):
        """
        Enregistre un nouveau lieu.
        Crée un nouveau lieu avec les données fournies, incluant les relations
        avec le propriétaire et les équipements. Vérifie la validité des données
        et l'existence des entités référencées.
        """
        place_data = api.payload

        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<place_id>')
@api.param('place_id', 'Identifiant du lieu')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.response(200, 'Succès', place_response_model)
    @api.response(404, 'Lieu non trouvé')
    @api.marshal_with(place_response_model)
    def get(self, place_id):
        """
        Récupère les détails d'un lieu par son ID.
        Retourne les informations complètes du lieu spécifié,
        incluant le propriétaire, les équipements et les avis.
        """
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Lieu non trouvé')
        return place.to_dict()

    @api.doc('update_place')
    @api.expect(place_model)
    @api.response(200, 'Lieu mis à jour avec succès', place_response_model)
    @api.response(404, 'Lieu non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    @api.marshal_with(place_response_model)
    def put(self, place_id):
        """
        Met à jour les détails d'un lieu.
        Modifie les informations du lieu spécifié avec les nouvelles données,
        incluant les relations avec les équipements. Vérifie la validité des
        données et l'existence des entités référencées.
        """
        place_data = api.payload
        
        try:
            place = facade.update_place(place_id, place_data)
            if not place:
                api.abort(404, 'Lieu non trouvé')
            return place.to_dict()
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<place_id>/reviews')
@api.param('place_id', 'Identifiant du lieu')
class PlaceReviewList(Resource):
    @api.doc('get_place_reviews')
    @api.response(200, 'Liste des avis du lieu récupérée avec succès')
    @api.response(404, 'Lieu non trouvé')
    @api.marshal_list_with(review_model)
    def get(self, place_id):
        """
        Récupère tous les avis pour un lieu spécifique.
        Retourne la liste complète des avis associés au lieu,
        incluant les détails des utilisateurs ayant rédigé les avis.
        """
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews]
        except ValueError:
            api.abort(404, 'Lieu non trouvé')
