#!/usr/bin/env python3
"""
API pour la gestion des utilisateurs dans l'application HolbertonBnB.
Ce module définit les endpoints REST pour créer, lire, mettre à jour et supprimer
des utilisateurs, ainsi que pour gérer l'authentification des utilisateurs.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

# Création du namespace pour les utilisateurs
api = Namespace('users', description='Opérations liées aux utilisateurs')

# Définition du modèle utilisateur pour la validation des entrées et la documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='Prénom de l\'utilisateur'),
    'last_name': fields.String(required=True, description='Nom de famille de l\'utilisateur'),
    'email': fields.String(required=True, description='Adresse email'),
    'password': fields.String(required=True, description='Mot de passe de l\'utilisateur')
})

# Définition du modèle de mise à jour d'utilisateur (mot de passe optionnel)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='Prénom de l\'utilisateur'),
    'last_name': fields.String(description='Nom de famille de l\'utilisateur'),
    'email': fields.String(description='Adresse email'),
    'password': fields.String(description='Mot de passe de l\'utilisateur')
})

# Définition du modèle de réponse utilisateur (sans exposer le mot de passe)
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='Identifiant unique de l\'utilisateur'),
    'first_name': fields.String(description='Prénom de l\'utilisateur'),
    'last_name': fields.String(description='Nom de famille de l\'utilisateur'),
    'email': fields.String(description='Adresse email'),
    'is_admin': fields.Boolean(description='Indique si l\'utilisateur est administrateur'),
    'created_at': fields.String(description='Date de création du compte'),
    'updated_at': fields.String(description='Date de dernière mise à jour')
})

# Modèle de connexion utilisateur
login_model = api.model('UserLoginModel', {
    'email': fields.String(required=True, description='Adresse email'),
    'password': fields.String(required=True, description='Mot de passe')
})

# Modèle de réponse pour le token
token_model = api.model('TokenModel', {
    'access_token': fields.String(description='Token JWT d\'accès')
})

@api.route('/login')
class UserLogin(Resource):
    """
    Endpoint de connexion utilisateur.
    Authentifie l'utilisateur et renvoie un token JWT.
    """
    @api.doc('user_login')
    @api.expect(login_model, validate=True)
    @api.response(200, 'Connexion réussie', token_model)
    @api.response(401, 'Identifiants invalides')
    def post(self):
        """
        Authentifie un utilisateur et génère un token JWT.
        
        Returns:
            dict: Contenant le token JWT si l'authentification réussit
            
        Raises:
            401: Si les identifiants sont invalides
        """
        data = api.payload
        token = facade.authenticate_user(data['email'], data['password'])
        if not token:
            api.abort(401, 'Identifiants invalides')
        return {'access_token': token}

@api.route('/')
class UserList(Resource):
    """
    Collection d'utilisateurs.
    Permet de lister tous les utilisateurs et d'en créer de nouveaux.
    """
    @api.doc('list_users')
    @api.marshal_list_with(user_response_model)
    def get(self):
        """
        Récupère la liste de tous les utilisateurs.
        
        Returns:
            list: Liste des utilisateurs enregistrés
        """
        return facade.get_all_users()
    
    @api.doc('create_user')
    @api.expect(user_model, validate=True)
    @api.response(201, 'Utilisateur créé avec succès', user_response_model)
    @api.response(400, 'Données d\'entrée invalides')
    def post(self):
        """
        Crée un nouvel utilisateur.
        
        Returns:
            dict: Informations de l'utilisateur créé
            
        Raises:
            400: Si les données fournies sont invalides ou si l'email est déjà utilisé
        """
        try:
            user = facade.create_user(api.payload)
            return user, 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<user_id>')
@api.param('user_id', 'Identifiant de l\'utilisateur')
class UserResource(Resource):
    """
    Ressource utilisateur individuelle.
    Permet de récupérer, mettre à jour ou supprimer un utilisateur spécifique.
    """
    @api.doc('get_user')
    @api.response(200, 'Succès', user_response_model)
    @api.response(404, 'Utilisateur non trouvé')
    def get(self, user_id):
        """
        Récupère les informations d'un utilisateur par son ID.
        
        Args:
            user_id (str): Identifiant de l'utilisateur
            
        Returns:
            dict: Informations de l'utilisateur
            
        Raises:
            404: Si l'utilisateur n'existe pas
        """
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"Utilisateur avec l'id {user_id} non trouvé")
        return user
    
    @api.doc('update_user')
    @api.expect(user_update_model)
    @api.response(200, 'Utilisateur mis à jour avec succès', user_response_model)
    @api.response(404, 'Utilisateur non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    @api.response(403, 'Permission refusée')
    @jwt_required()
    def put(self, user_id):
        """
        Met à jour les informations d'un utilisateur.
        Nécessite d'être connecté comme l'utilisateur concerné ou comme administrateur.
        
        Args:
            user_id (str): Identifiant de l'utilisateur à mettre à jour
            
        Returns:
            dict: Informations de l'utilisateur mises à jour
            
        Raises:
            404: Si l'utilisateur n'existe pas
            400: Si les données fournies sont invalides
            403: Si l'utilisateur connecté n'a pas les permissions nécessaires
        """
        # Vérification des permissions
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Vérifier si l'utilisateur est admin ou s'il modifie son propre profil
        if not is_admin and current_user_id != user_id:
            api.abort(403, "Vous n'avez pas la permission de modifier cet utilisateur")
        
        try:
            user = facade.update_user(user_id, api.payload)
            if not user:
                api.abort(404, f"Utilisateur avec l'id {user_id} non trouvé")
            return user
        except ValueError as e:
            api.abort(400, str(e))
            
    @api.doc('delete_user')
    @api.response(200, 'Utilisateur supprimé avec succès')
    @api.response(404, 'Utilisateur non trouvé')
    @api.response(403, 'Permission refusée')
    @jwt_required()
    def delete(self, user_id):
        """
        Supprime un utilisateur.
        Nécessite d'être connecté comme l'utilisateur concerné ou comme administrateur.
        
        Args:
            user_id (str): Identifiant de l'utilisateur à supprimer
            
        Returns:
            dict: Message de confirmation
            
        Raises:
            404: Si l'utilisateur n'existe pas
            403: Si l'utilisateur connecté n'a pas les permissions nécessaires
        """
        # Vérification des permissions
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Vérifier si l'utilisateur est admin ou s'il supprime son propre profil
        if not is_admin and current_user_id != user_id:
            api.abort(403, "Vous n'avez pas la permission de supprimer cet utilisateur")
        
        success = facade.delete_user(user_id)
        if not success:
            api.abort(404, f"Utilisateur avec l'id {user_id} non trouvé")
            
        return {"message": "Utilisateur supprimé avec succès"}
