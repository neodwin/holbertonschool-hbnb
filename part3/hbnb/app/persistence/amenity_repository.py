from app.persistence.repository import SQLAlchemyRepository
from app.models.amenity import Amenity

"""
Module amenity_repository.py - Gestion de la persistance des équipements
Ce module implémente les opérations spécifiques pour la gestion des équipements (amenities)
dans la base de données, notamment la recherche par nom et les validations d'unicité.
"""

class AmenityRepository(SQLAlchemyRepository):
    """
    Repository pour la gestion des équipements dans la base de données.
    Étend le SQLAlchemyRepository en ajoutant des méthodes spécifiques aux équipements,
    notamment la validation de l'unicité des noms d'équipements.
    """
    def __init__(self):
        """
        Initialise le repository des équipements avec le modèle Amenity.
        """
        super().__init__(Amenity)
    
    def get_by_name(self, name):
        """
        Récupère un équipement par son nom.
        
        Args:
            name (str): Le nom de l'équipement à rechercher
            
        Returns:
            Amenity: L'équipement correspondant au nom ou None si aucun équipement trouvé
        """
        return Amenity.query.filter_by(name=name).first()
    
    def create_amenity(self, amenity_data):
        """
        Crée un nouvel équipement avec validation.
        Vérifie que le nom n'est pas déjà utilisé avant de créer l'équipement.
        
        Args:
            amenity_data (dict): Dictionnaire contenant les données de l'équipement
            
        Returns:
            Amenity: L'équipement créé
            
        Raises:
            ValueError: Si un équipement avec ce nom existe déjà
        """
        # Vérification si un équipement avec le même nom existe déjà
        if 'name' in amenity_data and self.get_by_name(amenity_data['name']):
            raise ValueError('Amenity with this name already exists')
            
        # Création et ajout de l'équipement
        amenity = Amenity(**amenity_data)
        self.add(amenity)
        return amenity
    
    def update_amenity(self, amenity_id, amenity_data):
        """
        Met à jour un équipement existant avec validation.
        Vérifie que le nouveau nom n'est pas déjà utilisé par un autre équipement.
        
        Args:
            amenity_id (str): L'identifiant de l'équipement à mettre à jour
            amenity_data (dict): Dictionnaire contenant les nouvelles données
            
        Returns:
            Amenity: L'équipement mis à jour ou None si l'équipement n'existe pas
            
        Raises:
            ValueError: Si le nouveau nom est déjà utilisé par un autre équipement
        """
        amenity = self.get(amenity_id)
        if not amenity:
            return None
            
        # Vérification d'unicité du nom si celui-ci est modifié
        if 'name' in amenity_data and amenity_data['name'] != amenity.name:
            existing_amenity = self.get_by_name(amenity_data['name'])
            if existing_amenity:
                raise ValueError('Amenity with this name already exists')
                
        # Mise à jour de l'équipement
        amenity.update(amenity_data)
        return amenity 