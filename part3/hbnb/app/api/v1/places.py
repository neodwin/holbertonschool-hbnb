#!/usr/bin/env python3
"""
API pour la gestion des logements (Places) dans l'application HolbertonBnB.
Ce module définit les endpoints REST pour créer, lire, mettre à jour et 
lister les logements ainsi que leurs avis (reviews).
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade

# Création du namespace pour les logements
api = Namespace('places', description='Opérations liées aux logements')

# Définition des modèles pour les entités liées
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Identifiant unique de l\'équipement'),
    'name': fields.String(description='Nom de l\'équipement'),
    'created_at': fields.String(description='Date de création'),
    'updated_at': fields.String(description='Date de dernière mise à jour')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='Identifiant unique de l\'utilisateur'),
    'first_name': fields.String(description='Prénom du propriétaire'),
    'last_name': fields.String(description='Nom de famille du propriétaire'),
    'email': fields.String(description='Adresse email'),
    'created_at': fields.String(description='Date de création'),
    'updated_at': fields.String(description='Date de dernière mise à jour')
})

# Définition du modèle d'avis pour les réponses des logements
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Identifiant unique de l\'avis'),
    'text': fields.String(description='Texte de l\'avis'),
    'rating': fields.Integer(description='Note du logement (1-5)'),
    'user': fields.Nested(user_model, description='Utilisateur ayant rédigé l\'avis'),
    'place': fields.Nested(api.model('ReviewPlace', {
        'id': fields.String(description='Identifiant unique du logement'),
        'title': fields.String(description='Titre du logement')
    }), description='Logement concerné par l\'avis'),
    'created_at': fields.String(description='Date de création'),
    'updated_at': fields.String(description='Date de dernière mise à jour')
})

# Définition du modèle de logement pour la validation des entrées
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Titre du logement'),
    'description': fields.String(description='Description du logement'),
    'price': fields.Float(required=True, description='Prix par nuit'),
    'latitude': fields.Float(required=True, description='Latitude du logement'),
    'longitude': fields.Float(required=True, description='Longitude du logement'),
    'owner_id': fields.String(required=True, description='Identifiant du propriétaire'),
    'amenities': fields.List(fields.String, description="Liste des identifiants d'équipements")
})

# Définition du modèle de réponse pour les logements
place_response_model = api.model('PlaceResponse', {
    'id': fields.String(description='Identifiant unique du logement'),
    'title': fields.String(description='Titre du logement'),
    'description': fields.String(description='Description du logement'),
    'price': fields.Float(description='Prix par nuit'),
    'latitude': fields.Float(description='Latitude du logement'),
    'longitude': fields.Float(description='Longitude du logement'),
    'owner': fields.Nested(user_model, description='Détails du propriétaire'),
    'amenities': fields.List(fields.Nested(amenity_model), description='Liste des équipements'),
    'reviews': fields.List(fields.Nested(review_model), description='Liste des avis'),
    'created_at': fields.String(description='Date de création'),
    'updated_at': fields.String(description='Date de dernière mise à jour')
})

@api.route('/')
class PlaceList(Resource):
    """
    Ressource pour gérer la collection de logements.
    Permet de lister tous les logements et d'en créer de nouveaux.
    """
    @api.doc('list_places')
    @api.marshal_list_with(place_response_model)
    def get(self):
        """
        Liste tous les logements disponibles.
        
        Returns:
            list: Liste des logements avec tous leurs détails
        """
        places = facade.get_all_places()
        return [place.to_dict() for place in places]

    @api.doc('create_place')
    @api.expect(place_model, validate=True)
    @api.response(201, 'Logement créé avec succès', place_response_model)
    @api.response(400, 'Données d\'entrée invalides')
    @api.response(404, 'Propriétaire ou équipement non trouvé')
    @api.marshal_with(place_response_model, code=201)
    def post(self):
        """
        Enregistre un nouveau logement.
        
        Les données fournies sont validées selon le modèle place_model.
        Le propriétaire doit exister pour pouvoir créer un logement.
        
        Returns:
            dict: Détails du logement créé
            
        Raises:
            400: Si les données sont invalides
            404: Si le propriétaire ou un équipement n'existe pas
        """
        place_data = api.payload

        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<place_id>')
@api.param('place_id', 'Identifiant du logement')
class PlaceResource(Resource):
    """
    Ressource pour gérer un logement spécifique.
    Permet de récupérer, modifier ou supprimer un logement par son identifiant.
    """
    @api.doc('get_place')
    @api.response(200, 'Succès', place_response_model)
    @api.response(404, 'Logement non trouvé')
    @api.marshal_with(place_response_model)
    def get(self, place_id):
        """
        Récupère les détails d'un logement par son identifiant.
        
        Args:
            place_id (str): Identifiant unique du logement
            
        Returns:
            dict: Détails du logement
            
        Raises:
            404: Si le logement n'existe pas
        """
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Logement non trouvé')
        return place.to_dict()

    @api.doc('update_place')
    @api.expect(place_model)
    @api.response(200, 'Logement mis à jour avec succès', place_response_model)
    @api.response(404, 'Logement non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    @api.marshal_with(place_response_model)
    def put(self, place_id):
        """
        Met à jour les détails d'un logement.
        
        Args:
            place_id (str): Identifiant unique du logement
            
        Returns:
            dict: Détails du logement mis à jour
            
        Raises:
            400: Si les données sont invalides
            404: Si le logement n'existe pas
        """
        place_data = api.payload
        
        try:
            place = facade.update_place(place_id, place_data)
            if not place:
                api.abort(404, 'Logement non trouvé')
            return place.to_dict()
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<place_id>/reviews')
@api.param('place_id', 'Identifiant du logement')
class PlaceReviewList(Resource):
    """
    Ressource pour gérer les avis associés à un logement spécifique.
    Permet de récupérer tous les avis d'un logement.
    """
    @api.doc('get_place_reviews')
    @api.response(200, 'Liste des avis récupérée avec succès')
    @api.response(404, 'Logement non trouvé')
    @api.marshal_list_with(review_model)
    def get(self, place_id):
        """
        Récupère tous les avis pour un logement spécifique.
        
        Args:
            place_id (str): Identifiant unique du logement
            
        Returns:
            list: Liste des avis pour le logement
            
        Raises:
            404: Si le logement n'existe pas
        """
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews]
        except ValueError:
            api.abort(404, 'Logement non trouvé')
