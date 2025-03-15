from app.persistence.repository import SQLAlchemyRepository
from app.models.review import Review

"""
Module review_repository.py - Gestion de la persistance des avis
Ce module implémente les opérations spécifiques pour la gestion des avis (reviews)
dans la base de données, notamment la recherche par logement ou par utilisateur.
"""

class ReviewRepository(SQLAlchemyRepository):
    """
    Repository pour la gestion des avis dans la base de données.
    Étend le SQLAlchemyRepository en ajoutant des méthodes spécifiques aux avis,
    notamment la recherche par logement et par utilisateur.
    """
    def __init__(self):
        """
        Initialise le repository des avis avec le modèle Review.
        """
        super().__init__(Review)
    
    def get_by_place(self, place_id):
        """
        Récupère tous les avis pour un logement spécifique.
        
        Args:
            place_id (str): L'identifiant du logement
            
        Returns:
            list: Liste des avis pour le logement spécifié
        """
        return Review.query.filter_by(place_id=place_id).all()
    
    def get_by_user(self, user_id):
        """
        Récupère tous les avis écrits par un utilisateur spécifique.
        
        Args:
            user_id (str): L'identifiant de l'utilisateur
            
        Returns:
            list: Liste des avis écrits par l'utilisateur
        """
        return Review.query.filter_by(user_id=user_id).all()
    
    def get_by_place_and_user(self, place_id, user_id):
        """
        Vérifie si un utilisateur a déjà donné un avis pour un logement spécifique.
        Utile pour imposer la contrainte qu'un utilisateur ne peut donner qu'un seul avis par logement.
        
        Args:
            place_id (str): L'identifiant du logement
            user_id (str): L'identifiant de l'utilisateur
            
        Returns:
            Review: L'avis trouvé ou None si aucun avis n'existe pour cette combinaison
        """
        return Review.query.filter_by(place_id=place_id, user_id=user_id).first()
    
    def create_review(self, review_data):
        """
        Crée un nouvel avis dans la base de données.
        
        Args:
            review_data (dict): Dictionnaire contenant les données de l'avis
            
        Returns:
            Review: L'avis créé
        """
        # Création et ajout de l'avis
        review = Review(**review_data)
        self.add(review)
        return review
    
    def update_review(self, review_id, review_data):
        """
        Met à jour un avis existant.
        
        Args:
            review_id (str): L'identifiant de l'avis à mettre à jour
            review_data (dict): Dictionnaire contenant les nouvelles données
            
        Returns:
            Review: L'avis mis à jour ou None si l'avis n'existe pas
        """
        review = self.get(review_id)
        if not review:
            return None
                
        # Mise à jour de l'avis
        review.update(review_data)
        return review 