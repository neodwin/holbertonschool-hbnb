#!/usr/bin/env python3
"""
Modèle Place pour l'application HolbertonBnB.
Ce module définit la classe Place qui représente les logements/hébergements 
disponibles dans l'application. Il gère les relations avec les utilisateurs,
les avis et les commodités.
"""

from app.models.base import BaseModel
from app.extensions import db

# Table d'association pour la relation many-to-many entre Place et Amenity
# Cette table intermédiaire permet de lier les logements et leurs commodités
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """
    Modèle représentant un logement dans l'application HolbertonBnB.
    
    Hérite de BaseModel qui fournit id, created_at, updated_at.
    Contient les informations essentielles d'un logement comme son titre,
    sa description, son prix et sa localisation géographique.
    """
    __tablename__ = 'places'  # Nom de la table dans la base de données
    
    # Attributs du logement
    title = db.Column(db.String(100), nullable=False)  # Titre de l'annonce (obligatoire)
    description = db.Column(db.Text, nullable=True)    # Description détaillée (optionnelle)
    price = db.Column(db.Float, nullable=False)        # Prix par nuit (obligatoire)
    latitude = db.Column(db.Float, nullable=False)     # Coordonnée géographique (obligatoire)
    longitude = db.Column(db.Float, nullable=False)    # Coordonnée géographique (obligatoire)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  # Référence à l'utilisateur propriétaire
    
    # Relations avec d'autres modèles
    # Relation One-to-Many : un logement peut avoir plusieurs avis
    reviews = db.relationship('Review', backref='place_rel', lazy='dynamic', 
                             cascade='all, delete-orphan')  # Cascade: supprime les avis si le logement est supprimé
    
    # Relation Many-to-Many : un logement peut avoir plusieurs commodités
    # et une commodité peut être associée à plusieurs logements
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='dynamic',
                               backref=db.backref('places', lazy='dynamic'))
    
    def __init__(self, title, description, price, latitude, longitude, owner, **kwargs):
        """
        Initialise un nouvel objet Place avec validation des données.
        
        Args:
            title (str): Titre du logement
            description (str, optional): Description détaillée du logement
            price (float): Prix par nuit
            latitude (float): Coordonnée géographique
            longitude (float): Coordonnée géographique
            owner (User): Utilisateur propriétaire du logement
            **kwargs: Attributs supplémentaires pour la classe parente
            
        Raises:
            ValueError: Si les informations fournies ne sont pas valides
        """
        # Validation des données avant de les passer au constructeur parent
        self.validate_title(title)
        self.validate_price(price)
        self.validate_coordinates(latitude, longitude)
        
        # Appel au constructeur de la classe parente (BaseModel)
        super().__init__(
            title=title,
            description=description or "",  # Valeur par défaut si description est None
            price=float(price),  # Conversion explicite en float
            latitude=float(latitude),  # Conversion explicite en float
            longitude=float(longitude),  # Conversion explicite en float
            owner_id=owner.id,  # Stockage de l'ID du propriétaire
            **kwargs
        )
        
        # Références temporaires, utilisées avant l'introduction des relations ORM
        # Ces attributs ne sont pas stockés directement en base de données
        self._owner = owner      # Référence temporaire au propriétaire
        self._reviews = []       # Liste temporaire des avis
        self._amenities = []     # Liste temporaire des commodités
        
        # Ajoute ce logement à la liste des logements du propriétaire
        # Cette étape sera automatisée par les relations ORM plus tard
        if hasattr(owner, 'add_place'):
            owner.add_place(self)

    @staticmethod
    def validate_title(title):
        """
        Valide le titre du logement.
        
        Args:
            title (str): Titre à valider
            
        Raises:
            ValueError: Si le titre n'est pas valide ou trop long
        """
        if not title or not isinstance(title, str):
            raise ValueError("Le titre est requis et doit être une chaîne de caractères")
        if len(title) > 100:
            raise ValueError("Le titre ne doit pas dépasser 100 caractères")

    @staticmethod
    def validate_price(price):
        """
        Valide le prix du logement.
        
        Args:
            price (float/str): Prix à valider, sera converti en float
            
        Raises:
            ValueError: Si le prix n'est pas un nombre positif
        """
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError("Le prix doit être un nombre positif")

    @staticmethod
    def validate_coordinates(latitude, longitude):
        """
        Valide les coordonnées géographiques.
        
        Args:
            latitude (float/str): Latitude à valider (-90 à 90)
            longitude (float/str): Longitude à valider (-180 à 180)
            
        Raises:
            ValueError: Si les coordonnées sont en dehors des plages valides
        """
        try:
            lat = float(latitude)
            lon = float(longitude)
            if not (-90.0 <= lat <= 90.0) or not (-180.0 <= lon <= 180.0):
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError("Coordonnées invalides. La latitude doit être comprise entre -90 et 90, la longitude entre -180 et 180")

    def add_review(self, review):
        """
        Ajoute un avis au logement.
        
        Args:
            review (Review): L'avis à ajouter
        """
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Ajoute une commodité au logement s'il ne l'a pas déjà.
        
        Args:
            amenity (Amenity): La commodité à ajouter
        """
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """
        Supprime une commodité du logement.
        
        Args:
            amenity (Amenity): La commodité à supprimer
        """
        if amenity in self.amenities:
            self.amenities.remove(amenity)

    def update(self, data):
        """
        Met à jour les attributs du logement avec validation.
        
        Args:
            data (dict): Dictionnaire des attributs à mettre à jour
            
        Raises:
            ValueError: Si les données fournies ne sont pas valides
        """
        # Validation des données mises à jour
        if 'title' in data:
            self.validate_title(data['title'])
        if 'price' in data:
            self.validate_price(data['price'])
        if 'latitude' in data or 'longitude' in data:
            # Utilise les valeurs existantes si non fournies
            lat = data.get('latitude', self.latitude)
            lon = data.get('longitude', self.longitude)
            self.validate_coordinates(lat, lon)
        
        # Appel à la méthode de la classe parente pour la mise à jour
        super().update(data)

    def to_dict(self):
        """
        Convertit l'objet en dictionnaire, incluant les relations.
        
        Returns:
            dict: Représentation dictionnaire du logement avec ses relations
        """
        # Utilise d'abord la méthode to_dict de la classe parente
        result = super().to_dict()
        
        # Ajoute les données des relations si disponibles
        # Information du propriétaire
        result['owner'] = self.owner_rel.to_dict() if hasattr(self, 'owner_rel') else None
        
        # Liste des avis
        result['reviews'] = [review.to_dict() for review in self.reviews.all()] if hasattr(self, 'reviews') else []
        
        # Liste des commodités
        result['amenities'] = [amenity.to_dict() for amenity in self.amenities.all()] if hasattr(self, 'amenities') else []
        
        return result
