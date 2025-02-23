"""
Module définissant les interfaces et implémentations pour la persistance des données.
Ce module fournit une abstraction pour le stockage et la récupération des objets
du domaine, permettant de changer facilement l'implémentation du stockage.
"""

from abc import ABC, abstractmethod

class Repository(ABC):
    """
    Interface abstraite définissant les opérations de base pour la persistance.
    
    Cette classe définit le contrat que toute implémentation de stockage
    doit respecter, assurant ainsi une interface uniforme pour la manipulation
    des données, indépendamment du système de stockage sous-jacent.
    """

    @abstractmethod
    def add(self, obj):
        """
        Ajoute un nouvel objet au stockage.
        
        Args:
            obj: L'objet à stocker, doit avoir un attribut 'id'.
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Récupère un objet par son identifiant.
        
        Args:
            obj_id: L'identifiant de l'objet à récupérer.
        
        Returns:
            L'objet correspondant à l'identifiant ou None s'il n'existe pas.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Récupère tous les objets stockés.
        
        Returns:
            Une liste contenant tous les objets stockés.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Met à jour un objet existant.
        
        Args:
            obj_id: L'identifiant de l'objet à mettre à jour.
            data: Dictionnaire contenant les nouvelles valeurs.
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Supprime un objet du stockage.
        
        Args:
            obj_id: L'identifiant de l'objet à supprimer.
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Recherche un objet par la valeur d'un de ses attributs.
        
        Args:
            attr_name: Le nom de l'attribut à vérifier.
            attr_value: La valeur recherchée pour cet attribut.
        
        Returns:
            Le premier objet correspondant aux critères ou None.
        """
        pass


class InMemoryRepository(Repository):
    """
    Implémentation en mémoire du Repository.
    
    Cette classe fournit une implémentation simple utilisant un dictionnaire
    pour stocker les objets en mémoire. Utile pour les tests et le développement,
    mais ne persiste pas les données entre les redémarrages de l'application.
    """

    def __init__(self):
        """
        Initialise un nouveau repository avec un stockage vide.
        """
        self._storage = {}

    def add(self, obj):
        """
        Ajoute un objet au stockage en mémoire.
        
        Args:
            obj: L'objet à stocker, son ID servira de clé.
        """
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """
        Récupère un objet par son ID.
        
        Args:
            obj_id: L'identifiant de l'objet recherché.
        
        Returns:
            L'objet correspondant ou None s'il n'existe pas.
        """
        return self._storage.get(obj_id)

    def get_all(self):
        """
        Récupère tous les objets stockés.
        
        Returns:
            Une liste de tous les objets dans le stockage.
        """
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Met à jour un objet existant.
        
        Args:
            obj_id: L'identifiant de l'objet à mettre à jour.
            data: Dictionnaire contenant les nouvelles valeurs.
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """
        Supprime un objet du stockage.
        
        Args:
            obj_id: L'identifiant de l'objet à supprimer.
        """
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """
        Recherche le premier objet ayant un attribut spécifique.
        
        Args:
            attr_name: Le nom de l'attribut à vérifier.
            attr_value: La valeur recherchée pour cet attribut.
        
        Returns:
            Le premier objet correspondant ou None si aucun ne correspond.
        """
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None) 