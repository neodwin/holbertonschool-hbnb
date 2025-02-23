"""
Module de gestion des points de terminaison API pour les utilisateurs.
Ce module définit les routes et les modèles pour la gestion CRUD des utilisateurs
dans l'application HBnB, permettant l'inscription, la modification et la
consultation des informations des utilisateurs.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request

# Création d'un espace de noms pour les opérations liées aux utilisateurs
api = Namespace('users', description='Opérations sur les utilisateurs')

# Définition du modèle de validation pour les utilisateurs
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='Prénom de l\'utilisateur'),
    'last_name': fields.String(required=True, description='Nom de l\'utilisateur'),
    'email': fields.String(required=True, description='Adresse email')
})

# Définition du modèle de réponse pour les utilisateurs
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='Identifiant unique de l\'utilisateur'),
    'first_name': fields.String(description='Prénom de l\'utilisateur'),
    'last_name': fields.String(description='Nom de l\'utilisateur'),
    'email': fields.String(description='Adresse email'),
    'created_at': fields.String(description='Date et heure de création'),
    'updated_at': fields.String(description='Date et heure de dernière modification')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_response_model)
    def get(self):
        """
        Liste tous les utilisateurs.
        Retourne une liste complète des utilisateurs enregistrés dans le système,
        avec leurs informations personnelles.
        """
        users = facade.get_all_users()
        return [user.to_dict() for user in users]

    @api.doc('create_user')
    @api.expect(user_model, validate=True)
    @api.response(201, 'Utilisateur créé avec succès', user_response_model)
    @api.response(400, 'Données d\'entrée invalides')
    def post(self):
        """
        Crée un nouvel utilisateur.
        Enregistre un nouvel utilisateur dans le système avec les informations
        fournies, en vérifiant la validité de l'adresse email et l'unicité
        des données.
        """
        try:
            user_data = api.payload
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, str(e))

@api.route('/<user_id>')
@api.param('user_id', 'Identifiant de l\'utilisateur')
class UserResource(Resource):
    @api.doc('get_user')
    @api.response(200, 'Succès', user_response_model)
    @api.response(404, 'Utilisateur non trouvé')
    def get(self, user_id):
        """
        Récupère les détails d'un utilisateur par son ID.
        Retourne les informations complètes de l'utilisateur spécifié,
        incluant ses données personnelles et les horodatages.
        """
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'Utilisateur non trouvé')
        return user.to_dict()

    @api.doc('update_user')
    @api.expect(user_model)
    @api.response(200, 'Utilisateur mis à jour avec succès', user_response_model)
    @api.response(404, 'Utilisateur non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    def put(self, user_id):
        """
        Met à jour les détails d'un utilisateur.
        Modifie les informations de l'utilisateur spécifié avec les nouvelles
        données fournies, en vérifiant leur validité et l'unicité de l'email.
        """
        user_data = api.payload
        try:
            user = facade.update_user(user_id, user_data)
            if not user:
                api.abort(404, 'Utilisateur non trouvé')
            return user.to_dict()
        except ValueError as e:
            api.abort(400, str(e))
