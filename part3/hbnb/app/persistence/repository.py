from abc import ABC, abstractmethod
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError

"""
Module repository.py - Définit les classes de base pour le pattern Repository
Ce module implémente le pattern Repository qui fournit une abstraction pour
les opérations de persistance des données, indépendamment du stockage sous-jacent.
"""

class Repository(ABC):
    """
    Classe abstraite Repository définissant l'interface commune pour toutes les implémentations de repository.
    Chaque repository spécifique à une entité devra hériter de cette classe et implémenter ces méthodes.
    """
    @abstractmethod
    def add(self, obj):
        """
        Ajoute un nouvel objet au repository.
        
        Args:
            obj: L'objet à ajouter au repository
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Récupère un objet par son identifiant.
        
        Args:
            obj_id: L'identifiant unique de l'objet à récupérer
            
        Returns:
            L'objet correspondant à l'identifiant ou None s'il n'existe pas
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Récupère tous les objets du repository.
        
        Returns:
            Une liste contenant tous les objets du repository
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Met à jour un objet existant dans le repository.
        
        Args:
            obj_id: L'identifiant unique de l'objet à mettre à jour
            data: Dictionnaire contenant les données de mise à jour
            
        Returns:
            L'objet mis à jour ou None si l'objet n'existe pas
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Supprime un objet du repository.
        
        Args:
            obj_id: L'identifiant unique de l'objet à supprimer
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Récupère un objet par la valeur d'un de ses attributs.
        
        Args:
            attr_name: Le nom de l'attribut à filtrer
            attr_value: La valeur recherchée pour cet attribut
            
        Returns:
            L'objet correspondant ou None si aucun objet ne correspond
        """
        pass


class InMemoryRepository(Repository):
    """
    Implémentation en mémoire du Repository.
    Cette classe stocke les objets dans un dictionnaire en mémoire.
    Utile pour les tests ou les prototypes rapides sans base de données.
    """
    def __init__(self):
        """
        Initialise un repository en mémoire avec un dictionnaire vide.
        """
        self._storage = {}

    def add(self, obj):
        """
        Ajoute un objet au dictionnaire de stockage en utilisant son ID comme clé.
        
        Args:
            obj: L'objet à ajouter
        """
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """
        Récupère un objet par son ID dans le dictionnaire de stockage.
        
        Args:
            obj_id: L'identifiant de l'objet à récupérer
            
        Returns:
            L'objet s'il existe, None sinon
        """
        return self._storage.get(obj_id)

    def get_all(self):
        """
        Récupère tous les objets du dictionnaire de stockage.
        
        Returns:
            Une liste de tous les objets stockés
        """
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Met à jour un objet existant avec les nouvelles données.
        
        Args:
            obj_id: L'identifiant de l'objet à mettre à jour
            data: Dictionnaire contenant les nouvelles valeurs
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """
        Supprime un objet du dictionnaire de stockage.
        
        Args:
            obj_id: L'identifiant de l'objet à supprimer
        """
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """
        Récupère le premier objet dont l'attribut spécifié correspond à la valeur recherchée.
        
        Args:
            attr_name: Le nom de l'attribut à vérifier
            attr_value: La valeur recherchée pour cet attribut
            
        Returns:
            Le premier objet correspondant ou None si aucun objet ne correspond
        """
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)


class SQLAlchemyRepository(Repository):
    """
    Implémentation SQLAlchemy du Repository.
    Cette classe utilise SQLAlchemy ORM pour interagir avec la base de données.
    """
    def __init__(self, model_class):
        """
        Initialise un repository SQLAlchemy pour une classe de modèle spécifique.
        
        Args:
            model_class: La classe de modèle SQLAlchemy pour ce repository
        """
        self.model_class = model_class

    def add(self, obj):
        """
        Ajoute un objet à la base de données.
        
        Args:
            obj: L'objet à ajouter à la base de données
            
        Raises:
            SQLAlchemyError: En cas d'erreur lors de l'ajout à la base de données
        """
        try:
            db.session.add(obj)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def get(self, obj_id):
        """
        Récupère un objet par son ID dans la base de données.
        
        Args:
            obj_id: L'identifiant de l'objet à récupérer
            
        Returns:
            L'objet s'il existe, None sinon
        """
        return self.model_class.query.get(obj_id)

    def get_all(self):
        """
        Récupère tous les objets de la table correspondante.
        
        Returns:
            Une liste de tous les objets de cette table
        """
        return self.model_class.query.all()

    def update(self, obj_id, data):
        """
        Met à jour un objet existant dans la base de données.
        
        Args:
            obj_id: L'identifiant de l'objet à mettre à jour
            data: Dictionnaire contenant les nouvelles valeurs
            
        Returns:
            L'objet mis à jour ou None si l'objet n'existe pas
            
        Raises:
            SQLAlchemyError: En cas d'erreur lors de la mise à jour
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            try:
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                raise e
        return obj

    def delete(self, obj_id):
        """
        Supprime un objet de la base de données.
        
        Args:
            obj_id: L'identifiant de l'objet à supprimer
            
        Returns:
            True si la suppression a réussi, False sinon
            
        Raises:
            SQLAlchemyError: En cas d'erreur lors de la suppression
        """
        obj = self.get(obj_id)
        if obj:
            try:
                db.session.delete(obj)
                db.session.commit()
                return True
            except SQLAlchemyError as e:
                db.session.rollback()
                raise e
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """
        Récupère le premier objet dont l'attribut spécifié correspond à la valeur recherchée.
        
        Args:
            attr_name: Le nom de l'attribut à filtrer
            attr_value: La valeur recherchée pour cet attribut
            
        Returns:
            Le premier objet correspondant ou None si aucun objet ne correspond
        """
        return self.model_class.query.filter_by(**{attr_name: attr_value}).first() 