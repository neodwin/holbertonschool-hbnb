"""
Module définissant le modèle des avis (reviews) de l'application.
Un avis représente l'évaluation d'un lieu par un utilisateur,
comprenant un texte descriptif et une note sur 5.
"""

from app.models.base import BaseModel

class Review(BaseModel):
    """
    Classe représentant un avis dans l'application.
    
    Cette classe hérite de BaseModel et ajoute :
    - La gestion du contenu de l'avis (texte et note)
    - La validation des données de l'avis
    - Les relations avec l'utilisateur et le lieu concerné
    
    Attributes:
        text (str): Texte de l'avis
        rating (int): Note attribuée au lieu (1 à 5)
        place (Place): Lieu concerné par l'avis
        user (User): Utilisateur ayant rédigé l'avis
    """

    def __init__(self, text, rating, place, user):
        """
        Initialise un nouvel avis.
        
        Args:
            text (str): Texte de l'avis
            rating (int): Note attribuée (1 à 5)
            place (Place): Lieu évalué
            user (User): Auteur de l'avis
        
        Raises:
            ValueError: Si le texte est vide ou si la note est invalide.
        """
        super().__init__()
        self.validate_text(text)
        self.validate_rating(rating)
        
        self.text = text
        self.rating = int(rating)
        self.place = place
        self.user = user
        
        # Ajoute cet avis à la liste des avis du lieu
        place.add_review(self)

    @staticmethod
    def validate_text(text):
        """
        Valide le texte de l'avis.
        
        Args:
            text (str): Texte à valider
        
        Raises:
            ValueError: Si le texte est vide ou n'est pas une chaîne de caractères.
        """
        if not text or not isinstance(text, str):
            raise ValueError("Le texte de l'avis est requis et doit être une chaîne de caractères")

    @staticmethod
    def validate_rating(rating):
        """
        Valide la note attribuée.
        
        Args:
            rating (int): Note à valider (doit être entre 1 et 5)
        
        Raises:
            ValueError: Si la note n'est pas un entier entre 1 et 5.
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
            data (dict): Dictionnaire contenant les nouvelles valeurs.
                        Les clés 'text' et 'rating' sont validées si présentes.
        
        Raises:
            ValueError: Si l'une des nouvelles valeurs est invalide.
        """
        if 'text' in data:
            self.validate_text(data['text'])
        if 'rating' in data:
            self.validate_rating(data['rating'])
        
        super().update(data)

    def to_dict(self):
        """
        Convertit l'objet en dictionnaire pour la sérialisation.
        
        Returns:
            dict: Dictionnaire contenant tous les attributs de l'avis,
                  avec l'utilisateur converti en dictionnaire complet
                  et le lieu en version simplifiée pour éviter les
                  références circulaires.
        """
        result = super().to_dict()
        # Convertit l'utilisateur en dictionnaire
        if hasattr(self, 'user'):
            result['user'] = self.user.to_dict()
        # Convertit le lieu en dictionnaire minimal pour éviter les références circulaires
        if hasattr(self, 'place'):
            result['place'] = {
                'id': self.place.id,
                'title': self.place.title
            }
        return result
