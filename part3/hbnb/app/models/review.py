#!/usr/bin/env python3
"""
Modèle Review pour l'application HolbertonBnB.
Ce module définit la classe Review qui représente les avis/commentaires
laissés par les utilisateurs sur les logements.
"""

from app.models.base import BaseModel
from app.extensions import db

class Review(BaseModel):
    """
    Modèle représentant un avis d'utilisateur sur un logement.
    
    Hérite de BaseModel qui fournit id, created_at, updated_at.
    Contient le texte de l'avis, la note attribuée, et les références
    vers le logement concerné et l'utilisateur qui a laissé l'avis.
    """
    __tablename__ = 'reviews'  # Nom de la table dans la base de données
    
    # Attributs de l'avis
    text = db.Column(db.Text, nullable=False)  # Texte du commentaire (obligatoire)
    rating = db.Column(db.Integer, nullable=False)  # Note de 1 à 5 (obligatoire)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)  # Référence au logement
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  # Référence à l'utilisateur
    
    # Les relations sont définies dans les modèles User et Place avec backref
    
    def __init__(self, text, rating, place, user, **kwargs):
        """
        Initialise un nouvel avis avec validation des données.
        
        Args:
            text (str): Texte du commentaire
            rating (int): Note de 1 à 5
            place (Place): Logement concerné par l'avis
            user (User): Utilisateur qui laisse l'avis
            **kwargs: Attributs supplémentaires pour la classe parente
            
        Raises:
            ValueError: Si les informations fournies ne sont pas valides
        """
        # Validation des données avant de les passer au constructeur parent
        self.validate_text(text)
        self.validate_rating(rating)
        
        # Appel au constructeur de la classe parente (BaseModel)
        super().__init__(
            text=text,
            rating=int(rating),  # Conversion explicite en entier
            place_id=place.id,   # Stockage de l'ID du logement
            user_id=user.id,     # Stockage de l'ID de l'utilisateur
            **kwargs
        )
        
        # Références temporaires, utilisées avant l'introduction des relations ORM
        # Ces attributs ne sont pas stockés directement en base de données
        self._place = place  # Référence temporaire au logement
        self._user = user    # Référence temporaire à l'utilisateur
        
        # Ajoute cet avis à la liste des avis du logement
        # Cette étape sera automatisée par les relations ORM plus tard
        if hasattr(place, 'add_review'):
            place.add_review(self)

    @staticmethod
    def validate_text(text):
        """
        Valide le texte de l'avis.
        
        Args:
            text (str): Texte à valider
            
        Raises:
            ValueError: Si le texte n'est pas valide
        """
        if not text or not isinstance(text, str):
            raise ValueError("Le texte de l'avis est requis et doit être une chaîne de caractères")

    @staticmethod
    def validate_rating(rating):
        """
        Valide la note attribuée au logement.
        
        Args:
            rating (int/str): Note à valider, sera convertie en entier
            
        Raises:
            ValueError: Si la note n'est pas un entier entre 1 et 5
        """
        try:
            rating = int(rating)
            if not (1 <= rating <= 5):
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError("La note doit être un entier entre 1 et 5")

    def update(self, data):
        """
        Met à jour les attributs de l'avis avec validation.
        
        Args:
            data (dict): Dictionnaire des attributs à mettre à jour
            
        Raises:
            ValueError: Si les données fournies ne sont pas valides
        """
        # Validation des données mises à jour
        if 'text' in data:
            self.validate_text(data['text'])
        if 'rating' in data:
            self.validate_rating(data['rating'])
        
        # Appel à la méthode de la classe parente pour la mise à jour
        super().update(data)

    def to_dict(self):
        """
        Convertit l'objet en dictionnaire, incluant des informations simplifiées sur les relations.
        
        Returns:
            dict: Représentation dictionnaire de l'avis avec informations sur l'utilisateur et le logement
        """
        # Utilise d'abord la méthode to_dict de la classe parente
        result = super().to_dict()
        
        # Ajoute les informations de l'utilisateur (version simplifiée)
        result['user'] = {
            'id': self.user_rel.id,
            'first_name': self.user_rel.first_name,
            'last_name': self.user_rel.last_name
        } if hasattr(self, 'user_rel') else None
        
        # Ajoute les informations du logement (version simplifiée)
        result['place'] = {
            'id': self.place_rel.id,
            'title': self.place_rel.title
        } if hasattr(self, 'place_rel') else None
        
        return result
