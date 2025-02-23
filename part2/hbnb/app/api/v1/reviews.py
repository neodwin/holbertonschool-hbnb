"""
Module de gestion des points de terminaison API pour les avis (reviews).
Ce module définit les routes et les modèles pour la gestion CRUD des avis
dans l'application HBnB, permettant aux utilisateurs de donner leur opinion
sur les lieux qu'ils ont visités.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade

# Création d'un espace de noms pour les opérations liées aux avis
api = Namespace('reviews', description='Opérations sur les avis')

# Définition du modèle utilisateur pour les réponses imbriquées
user_model = api.model('ReviewUser', {
    'id': fields.String(description='Identifiant de l\'utilisateur'),
    'first_name': fields.String(description='Prénom de l\'utilisateur'),
    'last_name': fields.String(description='Nom de l\'utilisateur'),
    'email': fields.String(description='Adresse email')
})

# Définition du modèle de lieu pour les réponses imbriquées
place_model = api.model('ReviewPlace', {
    'id': fields.String(description='Identifiant du lieu'),
    'title': fields.String(description='Titre du lieu')
})

# Définition du modèle de validation pour les avis
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Texte de l\'avis'),
    'rating': fields.Integer(required=True, description='Note du lieu (1-5)'),
    'user_id': fields.String(required=True, description='Identifiant de l\'utilisateur'),
    'place_id': fields.String(required=True, description='Identifiant du lieu')
})

# Définition du modèle de réponse pour les avis
review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Identifiant de l\'avis'),
    'text': fields.String(description='Texte de l\'avis'),
    'rating': fields.Integer(description='Note du lieu (1-5)'),
    'user': fields.Nested(user_model, description='Utilisateur ayant rédigé l\'avis'),
    'place': fields.Nested(place_model, description='Lieu concerné par l\'avis'),
    'created_at': fields.String(description='Date et heure de création'),
    'updated_at': fields.String(description='Date et heure de dernière modification')
})

@api.route('/')
class ReviewList(Resource):
    @api.doc('create_review')
    @api.expect(review_model, validate=True)
    @api.response(201, 'Avis créé avec succès', review_response_model)
    @api.response(400, 'Données d\'entrée invalides')
    @api.response(404, 'Utilisateur ou lieu non trouvé')
    @api.marshal_with(review_response_model, code=201)
    def post(self):
        """
        Enregistre un nouvel avis.
        Crée un nouvel avis avec les données fournies, en vérifiant
        l'existence de l'utilisateur et du lieu concernés.
        """
        try:
            new_review = facade.create_review(api.payload)
            return new_review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('list_reviews')
    @api.response(200, 'Liste des avis récupérée avec succès')
    @api.marshal_list_with(review_response_model)
    def get(self):
        """
        Récupère la liste de tous les avis.
        Retourne l'ensemble des avis enregistrés dans le système,
        avec les détails des utilisateurs et des lieux associés.
        """
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews]

@api.route('/<review_id>')
@api.param('review_id', 'Identifiant de l\'avis')
class ReviewResource(Resource):
    @api.doc('get_review')
    @api.response(200, 'Détails de l\'avis récupérés avec succès', review_response_model)
    @api.response(404, 'Avis non trouvé')
    @api.marshal_with(review_response_model)
    def get(self, review_id):
        """
        Récupère les détails d'un avis par son ID.
        Retourne les informations complètes de l'avis spécifié,
        incluant les détails de l'utilisateur et du lieu concerné.
        """
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Avis non trouvé')
        return review.to_dict()

    @api.doc('update_review')
    @api.expect(review_model)
    @api.response(200, 'Avis mis à jour avec succès', review_response_model)
    @api.response(404, 'Avis non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    @api.marshal_with(review_response_model)
    def put(self, review_id):
        """
        Met à jour les informations d'un avis.
        Modifie le texte et/ou la note d'un avis existant,
        en vérifiant la validité des nouvelles données.
        """
        try:
            review = facade.update_review(review_id, api.payload)
            if not review:
                api.abort(404, 'Avis non trouvé')
            return review.to_dict()
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_review')
    @api.response(200, 'Avis supprimé avec succès')
    @api.response(404, 'Avis non trouvé')
    def delete(self, review_id):
        """
        Supprime un avis.
        Efface définitivement l'avis spécifié du système.
        """
        if facade.delete_review(review_id):
            return {'message': 'Avis supprimé avec succès'}
        api.abort(404, 'Avis non trouvé')

@api.route('/places/<place_id>/reviews')
@api.param('place_id', 'Identifiant du lieu')
class PlaceReviewList(Resource):
    @api.doc('get_place_reviews')
    @api.response(200, 'Liste des avis du lieu récupérée avec succès')
    @api.response(404, 'Lieu non trouvé')
    @api.marshal_list_with(review_response_model)
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
