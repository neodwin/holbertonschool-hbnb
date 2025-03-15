#!/usr/bin/env python3
"""
API pour la gestion des avis (reviews) dans l'application HolbertonBnB.
Ce module définit les endpoints REST pour créer, lire, mettre à jour et supprimer
des avis sur les logements, ainsi que pour lister les avis par logement.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade

# Création du namespace pour les avis
api = Namespace('reviews', description='Opérations liées aux avis')

# Définition du modèle utilisateur pour les réponses imbriquées
user_model = api.model('ReviewUser', {
    'id': fields.String(description='Identifiant de l\'utilisateur'),
    'first_name': fields.String(description='Prénom de l\'utilisateur'),
    'last_name': fields.String(description='Nom de famille de l\'utilisateur'),
    'email': fields.String(description='Adresse email')
})

# Définition du modèle logement pour les réponses imbriquées
place_model = api.model('ReviewPlace', {
    'id': fields.String(description='Identifiant du logement'),
    'title': fields.String(description='Titre du logement')
})

# Définition du modèle avis pour la validation des entrées et la documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Texte de l\'avis'),
    'rating': fields.Integer(required=True, description='Note (1-5)', min=1, max=5),
    'place_id': fields.String(required=True, description='Identifiant du logement concerné'),
    'user_id': fields.String(required=True, description='Identifiant de l\'utilisateur qui donne l\'avis')
})

# Définition du modèle de réponse avis
review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Identifiant unique de l\'avis'),
    'text': fields.String(description='Texte de l\'avis'),
    'rating': fields.Integer(description='Note attribuée (1-5)'),
    'place': fields.Nested(place_model, description='Informations sur le logement'),
    'user': fields.Nested(user_model, description='Informations sur l\'utilisateur'),
    'created_at': fields.String(description='Date de création de l\'avis'),
    'updated_at': fields.String(description='Date de dernière mise à jour')
})

@api.route('/')
class ReviewList(Resource):
    """
    Collection d'avis.
    Permet de créer de nouveaux avis et de lister tous les avis.
    """
    @api.doc('create_review')
    @api.expect(review_model, validate=True)
    @api.response(201, 'Avis créé avec succès', review_response_model)
    @api.response(400, 'Données d\'entrée invalides')
    @api.response(404, 'Utilisateur ou logement non trouvé')
    @api.marshal_with(review_response_model, code=201)
    def post(self):
        """
        Crée un nouvel avis sur un logement.
        
        Returns:
            dict: Informations de l'avis créé
            
        Raises:
            400: Si les données fournies sont invalides
            404: Si l'utilisateur ou le logement n'existe pas
        """
        try:
            review = facade.create_review(api.payload)
            return review, 201
        except ValueError as e:
            api.abort(400, str(e))
        except KeyError as e:
            api.abort(404, str(e))
    
    @api.doc('list_reviews')
    @api.response(200, 'Liste des avis récupérée avec succès')
    @api.marshal_list_with(review_response_model)
    def get(self):
        """
        Récupère la liste de tous les avis.
        
        Returns:
            list: Liste des avis enregistrés
        """
        return facade.get_all_reviews()

@api.route('/<review_id>')
@api.param('review_id', 'Identifiant de l\'avis')
class ReviewResource(Resource):
    """
    Ressource avis individuelle.
    Permet de récupérer, mettre à jour ou supprimer un avis spécifique.
    """
    @api.doc('get_review')
    @api.response(200, 'Détails de l\'avis récupérés avec succès', review_response_model)
    @api.response(404, 'Avis non trouvé')
    @api.marshal_with(review_response_model)
    def get(self, review_id):
        """
        Récupère les informations d'un avis par son ID.
        
        Args:
            review_id (str): Identifiant de l'avis
            
        Returns:
            dict: Informations de l'avis
            
        Raises:
            404: Si l'avis n'existe pas
        """
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, f"Avis avec l'id {review_id} non trouvé")
        return review
    
    @api.doc('update_review')
    @api.expect(review_model)
    @api.response(200, 'Avis mis à jour avec succès', review_response_model)
    @api.response(404, 'Avis non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    @api.marshal_with(review_response_model)
    def put(self, review_id):
        """
        Met à jour les informations d'un avis.
        
        Args:
            review_id (str): Identifiant de l'avis à mettre à jour
            
        Returns:
            dict: Informations de l'avis mises à jour
            
        Raises:
            404: Si l'avis n'existe pas
            400: Si les données fournies sont invalides
        """
        try:
            review = facade.update_review(review_id, api.payload)
            if not review:
                api.abort(404, f"Avis avec l'id {review_id} non trouvé")
            return review
        except ValueError as e:
            api.abort(400, str(e))
        except KeyError as e:
            api.abort(404, str(e))
    
    @api.doc('delete_review')
    @api.response(200, 'Avis supprimé avec succès')
    @api.response(404, 'Avis non trouvé')
    def delete(self, review_id):
        """
        Supprime un avis.
        
        Args:
            review_id (str): Identifiant de l'avis à supprimer
            
        Returns:
            dict: Message de confirmation
            
        Raises:
            404: Si l'avis n'existe pas
        """
        success = facade.delete_review(review_id)
        if not success:
            api.abort(404, f"Avis avec l'id {review_id} non trouvé")
        return {"message": "Avis supprimé avec succès"}

@api.route('/places/<place_id>/reviews')
@api.param('place_id', 'Identifiant du logement')
class PlaceReviewList(Resource):
    """
    Collection d'avis pour un logement spécifique.
    Permet de lister tous les avis pour un logement donné.
    """
    @api.doc('get_place_reviews')
    @api.response(200, 'Liste des avis pour le logement récupérée avec succès')
    @api.response(404, 'Logement non trouvé')
    @api.marshal_list_with(review_response_model)
    def get(self, place_id):
        """
        Récupère la liste des avis pour un logement spécifique.
        
        Args:
            place_id (str): Identifiant du logement
            
        Returns:
            list: Liste des avis pour ce logement
            
        Raises:
            404: Si le logement n'existe pas
        """
        # Vérifier d'abord si le logement existe
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Logement avec l'id {place_id} non trouvé")
            
        return facade.get_reviews_by_place(place_id)
