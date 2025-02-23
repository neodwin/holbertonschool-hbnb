"""
Module définissant le modèle des utilisateurs de l'application.
Un utilisateur représente une personne inscrite sur la plateforme,
pouvant être propriétaire de lieux et rédiger des avis.
"""

import re
from app.models.base import BaseModel

class User(BaseModel):
    """
    Classe représentant un utilisateur dans l'application.
    
    Cette classe hérite de BaseModel et ajoute :
    - La gestion des informations personnelles (nom, prénom, email)
    - La validation des données utilisateur
    - La gestion des lieux possédés par l'utilisateur
    - La distinction entre utilisateurs normaux et administrateurs
    
    Attributes:
        first_name (str): Prénom de l'utilisateur (max 50 caractères)
        last_name (str): Nom de l'utilisateur (max 50 caractères)
        email (str): Adresse email unique de l'utilisateur
        is_admin (bool): Indique si l'utilisateur est administrateur
        places (list): Liste des lieux possédés par l'utilisateur
    """

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialise un nouvel utilisateur.
        
        Args:
            first_name (str): Prénom de l'utilisateur
            last_name (str): Nom de l'utilisateur
            email (str): Adresse email de l'utilisateur
            is_admin (bool, optional): Statut administrateur. Défaut à False.
        
        Raises:
            ValueError: Si l'un des champs est invalide (vide, format incorrect).
        """
        super().__init__()
        self.validate_name(first_name, "prénom")
        self.validate_name(last_name, "nom")
        self.validate_email(email)
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []  # Liste pour stocker les lieux possédés

    @staticmethod
    def validate_name(name, field):
        """
        Valide les champs de type nom (prénom et nom).
        
        Args:
            name (str): Valeur à valider
            field (str): Nom du champ pour les messages d'erreur
        
        Raises:
            ValueError: Si le nom est vide, n'est pas une chaîne de caractères,
                      ou dépasse 50 caractères.
        """
        if not name or not isinstance(name, str):
            raise ValueError(f"Le {field} est requis et doit être une chaîne de caractères")
        if len(name) > 50:
            raise ValueError(f"Le {field} ne doit pas dépasser 50 caractères")

    @staticmethod
    def validate_email(email):
        """
        Valide le format de l'adresse email.
        
        Args:
            email (str): Adresse email à valider
        
        Raises:
            ValueError: Si l'email est vide, n'est pas une chaîne de caractères,
                      ou ne respecte pas le format attendu.
        """
        if not email or not isinstance(email, str):
            raise ValueError("L'adresse email est requise et doit être une chaîne de caractères")
        
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            raise ValueError("Format d'adresse email invalide")

    def add_place(self, place):
        """
        Ajoute un lieu à la liste des lieux possédés par l'utilisateur.
        
        Args:
            place: Instance de la classe Place à ajouter aux possessions
                  de l'utilisateur.
        """
        self.places.append(place)

    def update(self, data):
        """
        Met à jour les attributs de l'utilisateur avec validation.
        
        Args:
            data (dict): Dictionnaire contenant les nouvelles valeurs.
                        Les clés 'first_name', 'last_name' et 'email'
                        sont validées si présentes.
        
        Raises:
            ValueError: Si l'une des nouvelles valeurs est invalide.
        """
        if 'first_name' in data:
            self.validate_name(data['first_name'], "prénom")
        if 'last_name' in data:
            self.validate_name(data['last_name'], "nom")
        if 'email' in data:
            self.validate_email(data['email'])
        
        super().update(data)
