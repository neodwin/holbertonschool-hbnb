"""
Module définissant le modèle des équipements (amenities) de l'application.
Un équipement représente une caractéristique ou un service disponible dans un lieu,
comme le Wi-Fi, la climatisation, une piscine, etc.
"""

from app.models.base import BaseModel

class Amenity(BaseModel):
    """
    Classe représentant un équipement dans l'application.
    
    Cette classe hérite de BaseModel et ajoute :
    - La validation du nom de l'équipement
    - La gestion des contraintes de longueur du nom
    
    Attributes:
        name (str): Nom de l'équipement (max 50 caractères)
    """

    def __init__(self, name):
        """
        Initialise un nouvel équipement.
        
        Args:
            name (str): Nom de l'équipement.
                       Doit être une chaîne non vide de 50 caractères maximum.
        
        Raises:
            ValueError: Si le nom est invalide (vide, non-string, ou trop long).
        """
        super().__init__()
        self.validate_name(name)
        self.name = name

    @staticmethod
    def validate_name(name):
        """
        Valide le nom d'un équipement.
        
        Args:
            name (str): Nom à valider.
        
        Raises:
            ValueError: Si le nom est vide, n'est pas une chaîne de caractères,
                      ou dépasse 50 caractères.
        """
        if not name or not isinstance(name, str):
            raise ValueError("Le nom de l'équipement est requis et doit être une chaîne de caractères")
        if len(name) > 50:
            raise ValueError("Le nom de l'équipement ne doit pas dépasser 50 caractères")

    def update(self, data):
        """
        Met à jour les attributs de l'équipement avec validation.
        
        Args:
            data (dict): Dictionnaire contenant les nouvelles valeurs.
                        La clé 'name' est validée si présente.
        
        Raises:
            ValueError: Si le nouveau nom est invalide.
        """
        if 'name' in data:
            self.validate_name(data['name'])
        
        super().update(data)
