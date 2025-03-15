from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User

"""
Module user_repository.py - Gestion de la persistance des utilisateurs
Ce module implémente les opérations spécifiques pour la gestion des utilisateurs
dans la base de données, notamment la recherche par email et les validations d'unicité.
"""

class UserRepository(SQLAlchemyRepository):
    """
    Repository pour la gestion des utilisateurs dans la base de données.
    Étend le SQLAlchemyRepository en ajoutant des méthodes spécifiques aux utilisateurs.
    """
    def __init__(self):
        """
        Initialise le repository des utilisateurs avec le modèle User.
        """
        super().__init__(User)
    
    def get_by_email(self, email):
        """
        Récupère un utilisateur par son adresse email.
        
        Args:
            email (str): L'adresse email à rechercher
            
        Returns:
            User: L'utilisateur correspondant à l'email ou None si aucun utilisateur trouvé
        """
        return self.get_by_attribute('email', email)
    
    def create_user(self, user_data):
        """
        Crée un nouvel utilisateur avec validation.
        Vérifie que l'email n'est pas déjà utilisé avant de créer l'utilisateur.
        
        Args:
            user_data (dict): Dictionnaire contenant les données de l'utilisateur
            
        Returns:
            User: L'utilisateur créé
            
        Raises:
            ValueError: Si l'email est déjà enregistré
        """
        # Vérification si l'email existe déjà
        if self.get_by_email(user_data.get('email')):
            raise ValueError('Email already registered')
        
        # Création et ajout de l'utilisateur
        user = User(**user_data)
        self.add(user)
        return user
    
    def update_user(self, user_id, user_data):
        """
        Met à jour un utilisateur existant avec validation.
        Vérifie que le nouvel email n'est pas déjà utilisé par un autre utilisateur.
        
        Args:
            user_id (str): L'identifiant de l'utilisateur à mettre à jour
            user_data (dict): Dictionnaire contenant les nouvelles données
            
        Returns:
            User: L'utilisateur mis à jour ou None si l'utilisateur n'existe pas
            
        Raises:
            ValueError: Si le nouvel email est déjà enregistré par un autre utilisateur
        """
        user = self.get(user_id)
        if not user:
            return None
            
        # Vérification d'unicité de l'email si celui-ci est modifié
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = self.get_by_email(user_data['email'])
            if existing_user:
                raise ValueError('Email already registered')
                
        # Mise à jour de l'utilisateur
        user.update(user_data)
        return user 