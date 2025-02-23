"""
Module de gestion des points de terminaison API pour les équipements (amenities).
Ce module définit les routes et les modèles pour la gestion CRUD des équipements
dans l'application HBnB, utilisant Flask-RESTX pour la documentation et la validation.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade

# Création d'un espace de noms pour les opérations liées aux équipements
api = Namespace('amenities', description='Opérations sur les équipements')

# Définition du modèle de validation pour les équipements
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Nom de l\'équipement')
})

# Définition du modèle de réponse incluant les champs générés automatiquement
amenity_response_model = api.inherit('AmenityResponse', amenity_model, {
    'id': fields.String(description='Identifiant unique de l\'équipement'),
    'created_at': fields.String(description='Date et heure de création'),
    'updated_at': fields.String(description='Date et heure de dernière modification')
})

@api.route('/')
class AmenityList(Resource):
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_response_model)
    def get(self):
        """
        Liste tous les équipements disponibles.
        Retourne une liste complète des équipements enregistrés dans le système.
        """
        return facade.get_all_amenities()

    @api.doc('create_amenity')
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Équipement créé avec succès', amenity_response_model)
    @api.response(400, 'Données d\'entrée invalides')
    def post(self):
        """
        Enregistre un nouvel équipement.
        Crée un nouvel équipement avec les données fournies et retourne l'objet créé.
        En cas d'erreur de validation, retourne une erreur 400.
        """
        amenity_data = api.payload

        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<amenity_id>')
@api.param('amenity_id', 'Identifiant de l\'équipement')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    @api.response(200, 'Succès', amenity_response_model)
    @api.response(404, 'Équipement non trouvé')
    def get(self, amenity_id):
        """
        Récupère les détails d'un équipement par son ID.
        Retourne les informations complètes de l'équipement spécifié.
        Si l'équipement n'existe pas, retourne une erreur 404.
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, 'Équipement non trouvé')
        return amenity.to_dict()

    @api.doc('update_amenity')
    @api.expect(amenity_model)
    @api.response(200, 'Équipement mis à jour avec succès', amenity_response_model)
    @api.response(404, 'Équipement non trouvé')
    @api.response(400, 'Données d\'entrée invalides')
    def put(self, amenity_id):
        """
        Met à jour les détails d'un équipement.
        Modifie les informations de l'équipement spécifié avec les nouvelles données.
        Retourne une erreur 404 si l'équipement n'existe pas ou 400 si les données sont invalides.
        """
        amenity_data = api.payload
        
        try:
            amenity = facade.update_amenity(amenity_id, amenity_data)
            if not amenity:
                api.abort(404, 'Équipement non trouvé')
            return amenity.to_dict()
        except ValueError as e:
            api.abort(400, str(e))
