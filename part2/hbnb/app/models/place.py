"""
Module définissant le modèle des lieux (places) de l'application.
Un lieu représente un hébergement proposé à la location,
avec ses caractéristiques, équipements et avis associés.
"""

from app.models.base import BaseModel

class Place(BaseModel):
    """
    Classe représentant un lieu dans l'application.
    
    Cette classe hérite de BaseModel et ajoute :
    - La gestion des informations du lieu (titre, description, prix)
    - La gestion de la localisation géographique
    - Les relations avec le propriétaire, les équipements et les avis
    - La validation des données du lieu
    
    Attributes:
        title (str): Titre du lieu (max 100 caractères)
        description (str): Description détaillée du lieu (optionnelle)
        price (float): Prix par nuit (positif)
        latitude (float): Latitude du lieu (-90 à 90)
        longitude (float): Longitude du lieu (-180 à 180)
        owner (User): Propriétaire du lieu
        reviews (list): Liste des avis sur le lieu
        amenities (list): Liste des équipements disponibles
    """

    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Initialise un nouveau lieu.
        
        Args:
            title (str): Titre du lieu
            description (str): Description du lieu (optionnelle)
            price (float): Prix par nuit
            latitude (float): Latitude du lieu
            longitude (float): Longitude du lieu
            owner (User): Propriétaire du lieu
        
        Raises:
            ValueError: Si l'un des champs est invalide.
        """
        super().__init__()
        self.validate_title(title)
        self.validate_price(price)
        self.validate_coordinates(latitude, longitude)
        
        self.title = title
        self.description = description or ""  # Champ optionnel
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner = owner
        self.reviews = []  # Liste pour stocker les avis
        self.amenities = []  # Liste pour stocker les équipements
        
        # Ajoute ce lieu à la liste des lieux du propriétaire
        owner.add_place(self)

    @staticmethod
    def validate_title(title):
        """
        Valide le titre du lieu.
        
        Args:
            title (str): Titre à valider
        
        Raises:
            ValueError: Si le titre est vide, n'est pas une chaîne de caractères,
                      ou dépasse 100 caractères.
        """
        if not title or not isinstance(title, str):
            raise ValueError("Le titre est requis et doit être une chaîne de caractères")
        if len(title) > 100:
            raise ValueError("Le titre ne doit pas dépasser 100 caractères")

    @staticmethod
    def validate_price(price):
        """
        Valide le prix du lieu.
        
        Args:
            price (float): Prix à valider
        
        Raises:
            ValueError: Si le prix n'est pas un nombre positif.
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
        Valide les coordonnées géographiques du lieu.
        
        Args:
            latitude (float): Latitude à valider (-90 à 90)
            longitude (float): Longitude à valider (-180 à 180)
        
        Raises:
            ValueError: Si les coordonnées sont hors des plages valides.
        """
        try:
            lat = float(latitude)
            lon = float(longitude)
            if not (-90.0 <= lat <= 90.0) or not (-180.0 <= lon <= 180.0):
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError("Coordonnées invalides. La latitude doit être entre -90 et 90, la longitude entre -180 et 180")

    def add_review(self, review):
        """
        Ajoute un avis au lieu.
        
        Args:
            review: Instance de la classe Review à ajouter aux avis du lieu.
        """
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Ajoute un équipement au lieu s'il n'est pas déjà présent.
        
        Args:
            amenity: Instance de la classe Amenity à ajouter aux équipements.
        """
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """
        Retire un équipement du lieu s'il est présent.
        
        Args:
            amenity: Instance de la classe Amenity à retirer des équipements.
        """
        if amenity in self.amenities:
            self.amenities.remove(amenity)

    def update(self, data):
        """
        Met à jour les attributs du lieu avec validation.
        
        Args:
            data (dict): Dictionnaire contenant les nouvelles valeurs.
                        Les clés 'title', 'price', 'latitude' et 'longitude'
                        sont validées si présentes.
        
        Raises:
            ValueError: Si l'une des nouvelles valeurs est invalide.
        """
        if 'title' in data:
            self.validate_title(data['title'])
        if 'price' in data:
            self.validate_price(data['price'])
        if 'latitude' in data or 'longitude' in data:
            lat = data.get('latitude', self.latitude)
            lon = data.get('longitude', self.longitude)
            self.validate_coordinates(lat, lon)
        
        super().update(data)

    def to_dict(self):
        """
        Convertit l'objet en dictionnaire pour la sérialisation.
        
        Returns:
            dict: Dictionnaire contenant tous les attributs du lieu,
                  avec les objets liés (propriétaire, équipements, avis)
                  également convertis en dictionnaires.
        """
        result = super().to_dict()
        # Convertit le propriétaire en dictionnaire
        if hasattr(self, 'owner'):
            result['owner'] = self.owner.to_dict()
        # Convertit les équipements en liste de dictionnaires
        if hasattr(self, 'amenities'):
            result['amenities'] = [amenity.to_dict() for amenity in self.amenities]
        # Convertit les avis en liste de dictionnaires
        if hasattr(self, 'reviews'):
            result['reviews'] = [review.to_dict() for review in self.reviews]
        return result
