#!/usr/bin/env python3
"""
Tests pour les modèles de l'application HolbertonBnB.
Ce module teste les opérations CRUD (Create, Read, Update, Delete) 
pour tous les modèles principaux de l'application.
"""

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.db_init import init_db
import json

def test_models():
    """
    Teste les opérations CRUD pour tous les modèles.
    
    Ce test effectue les opérations suivantes:
    1. Création d'instances de tous les modèles (User, Place, Review, Amenity)
    2. Lecture et vérification des données des instances créées
    3. Mise à jour des attributs des instances et vérification des changements
    4. Suppression des instances et vérification de leur absence en base de données
    """
    # Création d'une application en mode test
    app = create_app('testing')
    
    with app.app_context():
        # Initialisation de la base de données
        db.create_all()
        
        # Création d'un utilisateur de test
        test_user = User(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='testpassword'
        )
        db.session.add(test_user)
        db.session.commit()
        
        # Création d'un équipement de test
        test_amenity = Amenity(name='Test Amenity')
        db.session.add(test_amenity)
        db.session.commit()
        
        # Création d'un logement de test
        test_place = Place(
            title='Test Place',
            description='A test place description',
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=test_user
        )
        db.session.add(test_place)
        db.session.commit()
        
        # Création d'un second utilisateur pour les avis
        reviewer = User(
            first_name='Reviewer',
            last_name='User',
            email='reviewer@example.com',
            password='reviewerpassword'
        )
        db.session.add(reviewer)
        db.session.commit()
        
        # Création d'un avis de test
        test_review = Review(
            text='This is a test review',
            rating=5,
            place=test_place,
            user=reviewer
        )
        db.session.add(test_review)
        db.session.commit()
        
        # Test de récupération des données
        print("\n--- Testing Place Retrieval ---")
        # Récupération d'un logement par son titre
        place = Place.query.filter_by(title='Test Place').first()
        assert place is not None
        print(f"Place: {place.title}, Price: {place.price}, Owner ID: {place.owner_id}")
        
        print("\n--- Testing Amenity Retrieval ---")
        # Récupération d'un équipement par son nom
        amenity = Amenity.query.filter_by(name='Test Amenity').first()
        assert amenity is not None
        print(f"Amenity: {amenity.name}")
        
        print("\n--- Testing Review Retrieval ---")
        # Récupération d'un avis par l'ID du logement
        review = Review.query.filter_by(place_id=place.id).first()
        assert review is not None
        print(f"Review: {review.text}, Rating: {review.rating}, User ID: {review.user_id}")
        
        # Test de mise à jour des données
        print("\n--- Testing Updates ---")
        # Modification du prix du logement
        place.price = 150.0
        # Modification du nom de l'équipement
        amenity.name = 'Updated Amenity'
        # Modification de la note de l'avis
        review.rating = 4
        db.session.commit()
        
        # Vérification des mises à jour
        updated_place = Place.query.get(place.id)
        assert updated_place.price == 150.0
        print(f"Updated Place Price: {updated_place.price}")
        
        updated_amenity = Amenity.query.get(amenity.id)
        assert updated_amenity.name == 'Updated Amenity'
        print(f"Updated Amenity Name: {updated_amenity.name}")
        
        updated_review = Review.query.get(review.id)
        assert updated_review.rating == 4
        print(f"Updated Review Rating: {updated_review.rating}")
        
        # Test de suppression des données
        print("\n--- Testing Deletion ---")
        # Suppression de l'avis, du logement, de l'équipement et des utilisateurs
        db.session.delete(review)
        db.session.delete(place)
        db.session.delete(amenity)
        db.session.delete(reviewer)
        db.session.delete(test_user)
        db.session.commit()
        
        # Vérification de la suppression
        assert Place.query.get(place.id) is None
        assert Amenity.query.get(amenity.id) is None
        assert Review.query.get(review.id) is None
        
        print("All model tests passed!")
        
        # Nettoyage de la base de données
        db.drop_all()

if __name__ == '__main__':
    test_models() 