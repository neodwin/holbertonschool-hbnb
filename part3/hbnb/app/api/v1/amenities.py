#!/usr/bin/env python3
"""
API pour la gestion des équipements (amenities) dans l'application HolbertonBnB.
Ce module définit les endpoints REST pour créer, lire, mettre à jour et supprimer
des équipements qui peuvent être associés aux logements.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade

# Création du namespace pour les équipements
api = Namespace('amenities', description='Opérations liées aux équipements')

# Définition du modèle équipement pour la validation des entrées et la documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Nom de l\'équipement')
})

# Définition du modèle de réponse équipement
amenity_response_model = api.inherit('AmenityResponse', amenity_model, {
    'id': fields.String(description='Identifiant unique de l\'équipement'),
    'created_at': fields.String(description='Date de création'),
    'updated_at': fields.String(description='Date de dernière mise à jour')
})

@api.route('/')
class AmenityList(Resource):
    """
    Collection d'équipements.
    Permet de lister tous les équipements et d'en créer de nouveaux.
    """
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_response_model)
    def get(self):
        """
        Récupère la liste de tous les équipements disponibles.
        
        Returns:
            list: Liste des équipements enregistrés
        """
        return facade.get_all_amenities()
    
    @api.doc('create_amenity')
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Équipement créé avec succès', amenity_response_model)
    @api.response(400, 'Données d\'entrée invalides')
    def post(self):
        """
        Crée un nouvel équipement.
        
        Returns:
            dict: Informations de l'équipement créé
            
        Raises:
            400: Si les données fournies sont invalides ou si le nom est déjà utilisé
        """
        try:
            amenity = facade.create_amenity(api.payload)
            return amenity, 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<amenity_id>')
@api.param('amenity_id', 'Identifiant de l\'équipement')
class AmenityResource(Resource):
    """
    Ressource équipement individuelle.
    Permet de récupérer, mettre à jour ou supprimer un équipement spécifique.
    """
    @api.doc('get_amenity')
    @api.response(200, 'Succès', amenity_response_model)
    @api.response(404, 'Équipement non trouvé')
    def get(self, amenity_id):
        """
        Récupère les informations d'un équipement par son ID.
        
        Args:
            amenity_id (str): Identifiant de l'équipement
            
        Returns:
            dict: Informations de l'équipement
            
        Raises:
            404: Si l'équipement n'existe pas
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, f"Équipement avec l'id {amenity_id} non trouvé")
        return amenity
    
    @api.doc('update_amenity')
    @api.expect(amenity_model)
    @api.response(200, 'Équipement mis à jour avec succès', amenity_response_model)
    @api.response(404, 'Équipement non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    def put(self, amenity_id):
        """
        Met à jour les informations d'un équipement.
        
        Args:
            amenity_id (str): Identifiant de l'équipement à mettre à jour
            
        Returns:
            dict: Informations de l'équipement mises à jour
            
        Raises:
            404: Si l'équipement n'existe pas
            400: Si les données fournies sont invalides
        """
        try:
            amenity = facade.update_amenity(amenity_id, api.payload)
            if not amenity:
                api.abort(404, f"Équipement avec l'id {amenity_id} non trouvé")
            return amenity
        except ValueError as e:
            api.abort(400, str(e))
