#!/usr/bin/env python3
"""
Module d'authentification de l'API HolbertonBnB.
Ce module définit les endpoints d'authentification permettant
aux utilisateurs de se connecter et d'obtenir un token JWT.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade  # Façade qui encapsule la logique métier
from flask import request

# Création d'un namespace pour regrouper les routes d'authentification
# Sera monté à l'URL /api/v1/auth
api = Namespace('auth', description='Opérations d\'authentification')

# Définition du modèle de données pour la requête de login
# Utilisé pour valider les données reçues et générer la documentation Swagger
login_model = api.model('Login', {
    'email': fields.String(required=True, description='Adresse email'),
    'password': fields.String(required=True, description='Mot de passe de l\'utilisateur')
})

# Définition du modèle de réponse contenant le token JWT
# Utilisé pour générer la documentation Swagger
token_model = api.model('Token', {
    'access_token': fields.String(description='Token JWT d\'accès')
})

@api.route('/login')
class Login(Resource):
    """
    Endpoint d'authentification permettant aux utilisateurs de se connecter.
    Vérifie les identifiants et renvoie un token JWT en cas de succès.
    """
    
    @api.doc('user_login')  # Documentation Swagger pour cette opération
    @api.expect(login_model, validate=True)  # Attendu : corps de requête validé contre login_model
    @api.response(200, 'Connexion réussie', token_model)  # Documentation de la réponse en cas de succès
    @api.response(401, 'Identifiants invalides')  # Documentation de la réponse en cas d'échec d'authentification
    def post(self):
        """
        Endpoint de connexion utilisateur.
        
        Reçoit email et mot de passe, vérifie les identifiants et renvoie un token JWT.
        
        Returns:
            dict: Contenant le token JWT d'accès si la connexion est réussie
            
        Raises:
            401: Si les identifiants sont invalides
            500: En cas d'erreur serveur
        """
        # Récupère les données envoyées dans le corps de la requête
        data = api.payload
        
        try:
            # Appel à la façade pour authentifier l'utilisateur
            # La façade encapsule la logique métier et renvoie un token si les identifiants sont valides
            token = facade.authenticate_user(data['email'], data['password'])
            
            # Si l'authentification échoue (token est None)
            if not token:
                # Renvoie une erreur 401 Unauthorized
                api.abort(401, 'Identifiants invalides')
                
            # Authentification réussie : renvoie le token JWT
            return {'access_token': token}
            
        except Exception as e:
            # En cas d'erreur inattendue, renvoie une erreur 500 avec le message d'erreur
            api.abort(500, str(e)) 