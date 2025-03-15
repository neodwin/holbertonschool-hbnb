#!/usr/bin/env python3
"""
Module définissant le modèle de base pour tous les modèles de l'application HolbertonBnB.
Ce module fournit une classe abstraite BaseModel qui sera héritée par tous les
autres modèles afin de partager des fonctionnalités communes.
"""

import uuid
from datetime import datetime
from app.extensions import db
from sqlalchemy.ext.declarative import declared_attr

class BaseModel(db.Model):
    """
    Modèle de base abstrait pour tous les modèles de l'application.
    
    Fournit des attributs et méthodes communs à tous les modèles :
    - Identifiant unique (UUID)
    - Horodatage de création et de mise à jour
    - Méthodes pour la persistance et la sérialisation
    
    Cette classe ne doit pas être instanciée directement, mais héritée
    par les classes de modèle concrètes.
    """
    __abstract__ = True  # Indique à SQLAlchemy que cette classe est abstraite
    
    # Attributs communs à tous les modèles
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # Identifiant unique UUID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Date et heure de création
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Date et heure de mise à jour
    
    def __init__(self, **kwargs):
        """
        Initialise une nouvelle instance de modèle avec des valeurs par défaut pour les champs
        obligatoires si non fournis.
        
        Args:
            **kwargs: Attributs à définir sur l'instance
        """
        # Appel au constructeur parent (db.Model)
        super().__init__(**kwargs)
        
        # Génération des valeurs par défaut si non fournies
        if not self.id:
            self.id = str(uuid.uuid4())  # Génère un nouvel UUID si non fourni
        if not self.created_at:
            self.created_at = datetime.utcnow()  # Utilise le temps actuel si non fourni
        if not self.updated_at:
            self.updated_at = datetime.utcnow()  # Utilise le temps actuel si non fourni

    def save(self):
        """
        Enregistre l'instance en base de données.
        
        Ajoute l'objet à la session SQLAlchemy et effectue un commit.
        """
        db.session.add(self)  # Ajoute l'objet à la session
        db.session.commit()   # Persiste les changements en base de données

    def update(self, data):
        """
        Met à jour les attributs de l'objet à partir d'un dictionnaire.
        
        Args:
            data (dict): Dictionnaire contenant les attributs à mettre à jour
            
        Note:
            Les attributs 'id', 'created_at' et 'updated_at' sont protégés et ne peuvent
            pas être modifiés par cette méthode.
        """
        # Mise à jour des attributs autorisés
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
                
        # Mise à jour de la date de modification
        self.updated_at = datetime.utcnow()
        
        # Persiste les changements en base de données
        db.session.commit()

    def to_dict(self):
        """
        Convertit l'objet en représentation dictionnaire.
        
        Returns:
            dict: Représentation dictionnaire de l'objet avec tous ses attributs
                  Les dates sont converties en format ISO.
        """
        result = {}
        
        # Récupère tous les attributs de l'objet qui sont des colonnes SQLAlchemy
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            
            # Conversion des dates en format ISO pour la sérialisation JSON
            if isinstance(value, datetime):
                value = value.isoformat()
                
            result[column.name] = value
            
        return result 