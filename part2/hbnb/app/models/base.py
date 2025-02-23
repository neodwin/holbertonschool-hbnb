"""
Module définissant la classe de base pour tous les modèles de l'application.
Cette classe fournit les fonctionnalités communes à tous les modèles,
notamment la gestion des identifiants uniques et des horodatages.
"""

import uuid
from datetime import datetime

class BaseModel:
    """
    Classe de base pour tous les modèles de l'application.
    
    Cette classe implémente les fonctionnalités communes à tous les modèles :
    - Génération automatique d'un identifiant unique (UUID)
    - Gestion des horodatages de création et de modification
    - Méthodes de sérialisation et de mise à jour des objets
    """

    def __init__(self):
        """
        Initialise un nouveau modèle avec un identifiant unique
        et les horodatages de création et de modification.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Met à jour l'horodatage de dernière modification.
        Cette méthode doit être appelée à chaque modification de l'objet.
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Met à jour les attributs de l'objet à partir d'un dictionnaire.
        
        Args:
            data (dict): Dictionnaire contenant les nouvelles valeurs des attributs.
                        Les clés doivent correspondre aux noms des attributs.
        
        Note:
            Les attributs 'id', 'created_at' et 'updated_at' ne peuvent pas être modifiés.
            L'horodatage de modification est automatiquement mis à jour.
        """
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
        self.save()  # Met à jour l'horodatage de modification

    def to_dict(self):
        """
        Convertit l'objet en dictionnaire pour la sérialisation.
        
        Returns:
            dict: Dictionnaire contenant tous les attributs publics de l'objet,
                  avec les dates converties en chaînes de caractères ISO.
        
        Note:
            Les attributs commençant par '_' sont considérés comme privés
            et ne sont pas inclus dans le dictionnaire résultant.
        """
        result = {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')  # Exclut les attributs privés
        }
        # Convertit les objets datetime en chaînes de caractères au format ISO
        for key in ['created_at', 'updated_at']:
            if key in result:
                result[key] = result[key].isoformat()
        return result 