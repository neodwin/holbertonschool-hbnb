"""
Module implémentant le point d'entrée principal des services de l'application.
Ce module fournit une façade qui encapsule toute la logique métier et coordonne
les interactions entre les différents composants (modèles et persistance).
"""

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    """
    Façade principale de l'application HBnB.
    
    Cette classe centralise toutes les opérations de l'application et fournit
    une interface unifiée pour :
    - La gestion des utilisateurs
    - La gestion des lieux
    - La gestion des équipements
    - La gestion des avis
    
    Elle assure également la cohérence des données et les relations entre
    les différentes entités.
    """

    def __init__(self):
        """
        Initialise la façade avec des repositories en mémoire pour
        chaque type d'entité.
        """
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Méthodes liées aux utilisateurs

    def create_user(self, user_data):
        """
        Crée un nouvel utilisateur.
        
        Args:
            user_data (dict): Données de l'utilisateur (email, nom, prénom)
        
        Returns:
            User: L'utilisateur créé
        
        Raises:
            ValueError: Si l'email est déjà utilisé
        """
        # Vérifie si l'email existe déjà
        if 'email' in user_data:
            existing_user = self.get_user_by_email(user_data['email'])
            if existing_user:
                raise ValueError('Cette adresse email est déjà enregistrée')
        
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Récupère un utilisateur par son ID.
        
        Args:
            user_id: L'identifiant de l'utilisateur
        
        Returns:
            User: L'utilisateur trouvé ou None
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Récupère un utilisateur par son email.
        
        Args:
            email: L'adresse email recherchée
        
        Returns:
            User: L'utilisateur trouvé ou None
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """
        Récupère tous les utilisateurs.
        
        Returns:
            list: Liste de tous les utilisateurs
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """
        Met à jour les informations d'un utilisateur.
        
        Args:
            user_id: L'identifiant de l'utilisateur
            user_data (dict): Nouvelles données
        
        Returns:
            User: L'utilisateur mis à jour ou None
        
        Raises:
            ValueError: Si le nouvel email est déjà utilisé
        """
        user = self.get_user(user_id)
        if user:
            # Vérifie l'unicité de l'email si modifié
            if 'email' in user_data and user_data['email'] != user.email:
                existing_user = self.get_user_by_email(user_data['email'])
                if existing_user:
                    raise ValueError('Cette adresse email est déjà enregistrée')
            user.update(user_data)
        return user

    # Méthodes liées aux lieux

    def create_place(self, place_data):
        """
        Crée un nouveau lieu.
        
        Args:
            place_data (dict): Données du lieu incluant owner_id et amenities
        
        Returns:
            Place: Le lieu créé
        
        Raises:
            ValueError: Si le propriétaire ou un équipement n'existe pas
        """
        # Récupère le propriétaire
        owner_id = place_data.pop('owner_id')
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError('Propriétaire non trouvé')

        # Récupère les équipements si fournis
        amenity_ids = place_data.pop('amenities', [])
        amenities = []
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f'Équipement avec ID {amenity_id} non trouvé')
            amenities.append(amenity)

        # Crée le lieu
        place = Place(owner=owner, **place_data)
        
        # Ajoute les équipements
        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """
        Récupère un lieu par son ID.
        
        Args:
            place_id: L'identifiant du lieu
        
        Returns:
            Place: Le lieu trouvé ou None
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Récupère tous les lieux.
        
        Returns:
            list: Liste de tous les lieux
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Met à jour les informations d'un lieu.
        
        Args:
            place_id: L'identifiant du lieu
            place_data (dict): Nouvelles données
        
        Returns:
            Place: Le lieu mis à jour ou None
        
        Raises:
            ValueError: Si un équipement ou le propriétaire n'existe pas
        """
        place = self.get_place(place_id)
        if not place:
            return None

        # Gère la mise à jour des équipements
        if 'amenities' in place_data:
            amenity_ids = place_data.pop('amenities')
            # Efface les équipements actuels
            place.amenities.clear()
            # Ajoute les nouveaux équipements
            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f'Équipement avec ID {amenity_id} non trouvé')
                place.add_amenity(amenity)

        # Gère le changement de propriétaire
        if 'owner_id' in place_data:
            owner_id = place_data.pop('owner_id')
            owner = self.get_user(owner_id)
            if not owner:
                raise ValueError('Propriétaire non trouvé')
            place_data['owner'] = owner

        place.update(place_data)
        return place

    # Méthodes liées aux équipements

    def create_amenity(self, amenity_data):
        """
        Crée un nouvel équipement.
        
        Args:
            amenity_data (dict): Données de l'équipement
        
        Returns:
            Amenity: L'équipement créé
        """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Récupère un équipement par son ID.
        
        Args:
            amenity_id: L'identifiant de l'équipement
        
        Returns:
            Amenity: L'équipement trouvé ou None
        """
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, name):
        """
        Récupère un équipement par son nom.
        
        Args:
            name: Le nom de l'équipement
        
        Returns:
            Amenity: L'équipement trouvé ou None
        """
        return self.amenity_repo.get_by_attribute('name', name)

    def get_all_amenities(self):
        """
        Récupère tous les équipements.
        
        Returns:
            list: Liste de tous les équipements
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Met à jour les informations d'un équipement.
        
        Args:
            amenity_id: L'identifiant de l'équipement
            amenity_data (dict): Nouvelles données
        
        Returns:
            Amenity: L'équipement mis à jour ou None
        """
        amenity = self.get_amenity(amenity_id)
        if amenity:
            amenity.update(amenity_data)
        return amenity

    # Méthodes liées aux avis

    def create_review(self, review_data):
        """
        Crée un nouvel avis.
        
        Args:
            review_data (dict): Données de l'avis incluant user_id et place_id
        
        Returns:
            Review: L'avis créé
        
        Raises:
            ValueError: Si l'utilisateur ou le lieu n'existe pas
        """
        # Récupère l'utilisateur et le lieu
        user_id = review_data.pop('user_id')
        place_id = review_data.pop('place_id')
        
        user = self.get_user(user_id)
        if not user:
            raise ValueError('Utilisateur non trouvé')
            
        place = self.get_place(place_id)
        if not place:
            raise ValueError('Lieu non trouvé')

        # Crée l'avis
        review = Review(user=user, place=place, **review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """
        Récupère un avis par son ID.
        
        Args:
            review_id: L'identifiant de l'avis
        
        Returns:
            Review: L'avis trouvé ou None
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Récupère tous les avis.
        
        Returns:
            list: Liste de tous les avis
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Récupère tous les avis pour un lieu spécifique.
        
        Args:
            place_id: L'identifiant du lieu
        
        Returns:
            list: Liste des avis du lieu
        
        Raises:
            ValueError: Si le lieu n'existe pas
        """
        place = self.get_place(place_id)
        if not place:
            raise ValueError('Lieu non trouvé')
        return place.reviews

    def update_review(self, review_id, review_data):
        """
        Met à jour les informations d'un avis.
        
        Args:
            review_id: L'identifiant de l'avis
            review_data (dict): Nouvelles données
        
        Returns:
            Review: L'avis mis à jour ou None
        """
        review = self.get_review(review_id)
        if review:
            review.update(review_data)
        return review

    def delete_review(self, review_id):
        """
        Supprime un avis.
        
        Args:
            review_id: L'identifiant de l'avis
        
        Returns:
            bool: True si l'avis a été supprimé, False sinon
        """
        review = self.get_review(review_id)
        if review:
            # Retire l'avis de la liste des avis du lieu
            review.place.reviews.remove(review)
            # Supprime du repository
            self.review_repo.delete(review_id)
            return True
        return False 