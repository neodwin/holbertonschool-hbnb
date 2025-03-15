#!/usr/bin/env python3
"""
Script de test des relations entre entités de l'application HolbertonBnB.
Ce module teste les relations entre les différentes entités (User, Place, Review, Amenity)
pour vérifier que les associations sont correctement configurées et fonctionnent comme prévu.
"""

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
import json

def test_relationships():
    """
    Teste les relations entre les différentes entités du modèle de données.
    
    Cette fonction vérifie :
    - Les relations un-à-plusieurs entre User et Place (propriétaire -> logements)
    - Les relations un-à-plusieurs entre Place et Review (logement -> avis)
    - Les relations un-à-plusieurs entre User et Review (utilisateur -> avis)
    - Les relations plusieurs-à-plusieurs entre Place et Amenity (logement <-> équipements)
    - Le comportement de suppression en cascade
    """
    # Création d'une instance d'application avec la configuration de test
    app = create_app('testing')
    
    with app.app_context():
        # Initialisation de la base de données
        db.create_all()
        
        print("\n--- Création des données de test ---")
        
        # Création des utilisateurs
        # 1. Un propriétaire qui possédera des logements
        # 2. Deux utilisateurs qui laisseront des avis
        owner = User(
            first_name='Owner',
            last_name='User',
            email='owner@example.com',
            password='ownerpassword'
        )
        
        reviewer1 = User(
            first_name='Reviewer1',
            last_name='User',
            email='reviewer1@example.com',
            password='reviewer1password'
        )
        
        reviewer2 = User(
            first_name='Reviewer2',
            last_name='User',
            email='reviewer2@example.com',
            password='reviewer2password'
        )
        
        # Ajout des utilisateurs à la session et validation des changements
        db.session.add_all([owner, reviewer1, reviewer2])
        db.session.commit()
        
        # Création des équipements (amenities) qui seront associés aux logements
        wifi = Amenity(name='WiFi')
        pool = Amenity(name='Pool')
        parking = Amenity(name='Parking')
        
        # Ajout des équipements à la session et validation des changements
        db.session.add_all([wifi, pool, parking])
        db.session.commit()
        
        # Création des logements (places) appartenant au propriétaire
        place1 = Place(
            title='Beach House',
            description='Beautiful house near the beach',
            price=150.0,
            latitude=34.0522,
            longitude=-118.2437,
            owner=owner  # Association directe avec le propriétaire
        )
        
        place2 = Place(
            title='Mountain Cabin',
            description='Cozy cabin in the mountains',
            price=120.0,
            latitude=39.5501,
            longitude=-105.7821,
            owner=owner  # Association directe avec le propriétaire
        )
        
        # Ajout des logements à la session et validation des changements
        db.session.add_all([place1, place2])
        db.session.commit()
        
        # Ajout des équipements aux logements (relation plusieurs-à-plusieurs)
        # Le premier logement a WiFi et une piscine
        # Le deuxième logement a WiFi et un parking
        place1.add_amenity(wifi)
        place1.add_amenity(pool)
        place2.add_amenity(wifi)
        place2.add_amenity(parking)
        db.session.commit()
        
        # Création des avis laissés par les utilisateurs sur les logements
        review1 = Review(
            text='Great place with amazing views!',
            rating=5,
            place=place1,  # Association directe avec le premier logement
            user=reviewer1  # Association directe avec le premier utilisateur
        )
        
        review2 = Review(
            text='Nice place but a bit expensive',
            rating=4,
            place=place1,  # Association directe avec le premier logement
            user=reviewer2  # Association directe avec le deuxième utilisateur
        )
        
        review3 = Review(
            text='Cozy and comfortable',
            rating=5,
            place=place2,  # Association directe avec le deuxième logement
            user=reviewer1  # Association directe avec le premier utilisateur
        )
        
        # Ajout des avis à la session et validation des changements
        db.session.add_all([review1, review2, review3])
        db.session.commit()
        
        print("Données de test créées avec succès !")
        
        # Test de la relation User-Place (propriétaire et ses logements)
        print("\n--- Test de la relation User-Place ---")
        user_places = owner.places.all()
        print(f"Le propriétaire possède {len(user_places)} logements :")
        for place in user_places:
            print(f"- {place.title}")
        
        # Test de la relation Place-Review (logement et ses avis)
        print("\n--- Test de la relation Place-Review ---")
        place1_reviews = place1.reviews.all()
        print(f"Le logement '{place1.title}' a {len(place1_reviews)} avis :")
        for review in place1_reviews:
            print(f"- {review.rating}/5 étoiles : {review.text}")
        
        # Test de la relation User-Review (utilisateur et ses avis)
        print("\n--- Test de la relation User-Review ---")
        user_reviews = reviewer1.reviews.all()
        print(f"L'utilisateur '{reviewer1.first_name}' a écrit {len(user_reviews)} avis :")
        for review in user_reviews:
            print(f"- {review.rating}/5 étoiles pour '{review.place_rel.title}' : {review.text}")
        
        # Test de la relation Place-Amenity (logement et ses équipements)
        print("\n--- Test de la relation Place-Amenity ---")
        place1_amenities = place1.amenities.all()
        print(f"Le logement '{place1.title}' a {len(place1_amenities)} équipements :")
        for amenity in place1_amenities:
            print(f"- {amenity.name}")
        
        # Test de la relation inverse Amenity-Place (équipement et les logements qui le possèdent)
        print("\n--- Test de la relation Amenity-Place ---")
        wifi_places = wifi.places.all()
        print(f"L'équipement '{wifi.name}' est disponible dans {len(wifi_places)} logements :")
        for place in wifi_places:
            print(f"- {place.title}")
        
        # Test de la suppression en cascade
        # Quand un logement est supprimé, ses avis doivent être supprimés automatiquement
        print("\n--- Test de la suppression en cascade ---")
        print(f"Avant suppression : {len(Review.query.all())} avis au total")
        db.session.delete(place1)
        db.session.commit()
        print(f"Après suppression de '{place1.title}' : {len(Review.query.all())} avis au total")
        
        # Nettoyage de la base de données
        db.drop_all()
        print("\nTous les tests de relations ont été complétés avec succès !")

if __name__ == '__main__':
    # Si ce script est exécuté directement, lance la fonction de test
    test_relationships() 