from app.persistence.repository import SQLAlchemyRepository
from app.models.place import Place
from app.extensions import db

"""
Module place_repository.py - Gestion de la persistance des logements
Ce module implémente les opérations spécifiques pour la gestion des logements (places)
dans la base de données, notamment la recherche par propriétaire et la gestion des
associations avec les équipements (amenities).
"""

class PlaceRepository(SQLAlchemyRepository):
    """
    Repository pour la gestion des logements dans la base de données.
    Étend le SQLAlchemyRepository en ajoutant des méthodes spécifiques aux logements,
    notamment la gestion des relations avec les propriétaires et les équipements.
    """
    def __init__(self):
        """
        Initialise le repository des logements avec le modèle Place.
        """
        super().__init__(Place)
    
    def get_by_owner(self, owner_id):
        """
        Récupère tous les logements appartenant à un utilisateur spécifique.
        
        Args:
            owner_id (str): L'identifiant du propriétaire
            
        Returns:
            list: Liste des logements appartenant au propriétaire
        """
        return Place.query.filter_by(owner_id=owner_id).all()
    
    def create_place(self, place_data):
        """
        Crée un nouveau logement dans la base de données.
        
        Args:
            place_data (dict): Dictionnaire contenant les données du logement
            
        Returns:
            Place: Le logement créé
        """
        # Création et ajout du logement
        place = Place(**place_data)
        self.add(place)
        return place
    
    def update_place(self, place_id, place_data):
        """
        Met à jour un logement existant.
        Gère spécialement le cas des équipements associés qui nécessitent un traitement particulier.
        
        Args:
            place_id (str): L'identifiant du logement à mettre à jour
            place_data (dict): Dictionnaire contenant les nouvelles données
            
        Returns:
            Place: Le logement mis à jour ou None si le logement n'existe pas
        """
        place = self.get(place_id)
        if not place:
            return None
        
        # Traitement spécial pour la mise à jour des équipements si fournis
        if 'amenities' in place_data:
            amenities = place_data.pop('amenities')
            # Suppression des équipements actuels et ajout des nouveaux
            place.amenities = amenities
        
        # Mise à jour du logement
        place.update(place_data)
        return place
    
    def add_amenity_to_place(self, place_id, amenity):
        """
        Ajoute un équipement à un logement.
        
        Args:
            place_id (str): L'identifiant du logement
            amenity: L'objet équipement à ajouter
            
        Returns:
            Place: Le logement mis à jour ou None si le logement n'existe pas
        """
        place = self.get(place_id)
        if not place:
            return None
        
        place.add_amenity(amenity)
        db.session.commit()
        return place
    
    def remove_amenity_from_place(self, place_id, amenity):
        """
        Retire un équipement d'un logement.
        
        Args:
            place_id (str): L'identifiant du logement
            amenity: L'objet équipement à retirer
            
        Returns:
            Place: Le logement mis à jour ou None si le logement n'existe pas
        """
        place = self.get(place_id)
        if not place:
            return None
        
        place.remove_amenity(amenity)
        db.session.commit()
        return place 