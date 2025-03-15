#!/usr/bin/env python3
"""
Modèle Amenity pour l'application HolbertonBnB.
Ce module définit la classe Amenity qui représente les commodités/équipements
disponibles dans les logements (WiFi, cuisine, piscine, etc.).
"""

from app.models.base import BaseModel
from app.extensions import db

class Amenity(BaseModel):
    """
    Modèle représentant une commodité/équipement dans l'application HolbertonBnB.
    
    Hérite de BaseModel qui fournit id, created_at, updated_at.
    Une commodité est un service ou équipement disponible dans un logement,
    comme le WiFi, une cuisine, une piscine, etc.
    """
    __tablename__ = 'amenities'  # Nom de la table dans la base de données
    
    # Le nom est l'attribut principal et doit être unique
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    # La relation avec les logements est définie dans le modèle Place
    # via la table d'association place_amenity
    
    def __init__(self, name, **kwargs):
        """
        Initialise une nouvelle commodité avec validation du nom.
        
        Args:
            name (str): Le nom de la commodité
            **kwargs: Attributs supplémentaires pour la classe parente
            
        Raises:
            ValueError: Si le nom fourni n'est pas valide
        """
        # Validation du nom avant de le passer au constructeur parent
        self.validate_name(name)
        # Appel au constructeur de la classe parente (BaseModel)
        super().__init__(name=name, **kwargs)

    @staticmethod
    def validate_name(name):
        """
        Valide le nom de la commodité.
        
        Args:
            name (str): Nom à valider
            
        Raises:
            ValueError: Si le nom n'est pas valide ou trop long
        """
        if not name or not isinstance(name, str):
            raise ValueError("Le nom de la commodité est requis et doit être une chaîne de caractères")
        if len(name) > 50:
            raise ValueError("Le nom de la commodité ne doit pas dépasser 50 caractères")

    def update(self, data):
        """
        Met à jour les attributs de la commodité avec validation.
        
        Args:
            data (dict): Dictionnaire des attributs à mettre à jour
            
        Raises:
            ValueError: Si les données fournies ne sont pas valides
        """
        # Validation du nom s'il est fourni dans les données
        if 'name' in data:
            self.validate_name(data['name'])
        
        # Appel à la méthode de la classe parente pour la mise à jour
        super().update(data)
        
    def to_dict(self):
        """
        Convertit l'objet en dictionnaire.
        
        Returns:
            dict: Représentation dictionnaire de la commodité
            
        Note:
            N'inclut pas la liste des logements pour éviter les références circulaires.
        """
        # Utilise d'abord la méthode to_dict de la classe parente
        result = super().to_dict()
        # On n'inclut pas la liste des logements pour éviter les références circulaires
        return result
