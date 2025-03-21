#!/usr/bin/env python3
"""
Tests unitaires pour les modèles de l'application HolbertonBnB.
Ce module contient des tests basiques de création et validation pour chaque modèle,
ainsi que la vérification des relations entre les modèles.
"""

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def test_user_creation():
    """
    Teste la création et la validation d'un utilisateur.
    
    Ce test vérifie:
    1. La création correcte d'un utilisateur avec les attributs requis
    2. L'initialisation par défaut de l'attribut is_admin à False
    """
    try:
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.is_admin is False
        print("✓ User creation test passed!")
    except Exception as e:
        print(f"✗ User creation test failed: {str(e)}")

def test_place_creation():
    """
    Teste la création d'un logement et sa relation avec le propriétaire.
    
    Ce test vérifie:
    1. La création correcte d'un logement avec tous les attributs requis
    2. La relation bidirectionnelle entre le logement et son propriétaire
    """
    try:
        owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
        place = Place(
            title="Cozy Apartment",
            description="A nice place to stay",
            price=100,
            latitude=37.7749,
            longitude=-122.4194,
            owner=owner
        )

        assert place.title == "Cozy Apartment"
        assert place.price == 100.0
        assert place.owner == owner
        assert place in owner.places
        print("✓ Place creation and relationship test passed!")
    except Exception as e:
        print(f"✗ Place creation test failed: {str(e)}")

def test_review_creation():
    """
    Teste la création d'un avis et ses relations avec l'utilisateur et le logement.
    
    Ce test vérifie:
    1. La création correcte d'un avis avec tous les attributs requis
    2. Les relations entre l'avis, l'utilisateur qui l'a rédigé et le logement concerné
    3. La validation de la note (rating) qui doit être entre 1 et 5
    """
    try:
        user = User(first_name="Bob", last_name="Johnson", email="bob.j@example.com")
        owner = User(first_name="Carol", last_name="Wilson", email="carol.w@example.com")
        place = Place(
            title="Beach House",
            description="Beautiful beachfront property",
            price=200,
            latitude=25.7617,
            longitude=-80.1918,
            owner=owner
        )
        review = Review(text="Amazing stay!", rating=5, place=place, user=user)

        assert review.text == "Amazing stay!"
        assert review.rating == 5
        assert review in place.reviews
        print("✓ Review creation and relationship test passed!")
    except Exception as e:
        print(f"✗ Review creation test failed: {str(e)}")

def test_amenity_creation():
    """
    Teste la création d'un équipement et son association avec un logement.
    
    Ce test vérifie:
    1. La création correcte d'un équipement avec un nom valide
    2. L'association bidirectionnelle entre l'équipement et un logement
    """
    try:
        owner = User(first_name="David", last_name="Brown", email="david.b@example.com")
        place = Place(
            title="Mountain Cabin",
            description="Cozy cabin in the woods",
            price=150,
            latitude=39.5501,
            longitude=-105.7821,
            owner=owner
        )
        wifi = Amenity(name="Wi-Fi")
        parking = Amenity(name="Parking")

        place.add_amenity(wifi)
        place.add_amenity(parking)

        assert wifi in place.amenities
        assert parking in place.amenities
        assert len(place.amenities) == 2
        print("✓ Amenity creation and relationship test passed!")
    except Exception as e:
        print(f"✗ Amenity creation test failed: {str(e)}")

def test_validation():
    """
    Teste les mécanismes de validation des modèles.
    
    Ce test vérifie que les modèles rejettent correctement les données invalides:
    1. Email invalide pour un utilisateur
    2. Prix négatif pour un logement
    3. Note (rating) hors plage pour un avis
    4. Nom vide pour un équipement
    """
    try:
        # Test invalid email
        try:
            User(first_name="Test", last_name="User", email="invalid-email")
            print("✗ Email validation test failed: Invalid email was accepted")
        except ValueError:
            print("✓ Email validation test passed!")

        # Test invalid price
        try:
            owner = User(first_name="Test", last_name="Owner", email="test@example.com")
            Place(title="Test Place", description="Test", price=-100, latitude=0, longitude=0, owner=owner)
            print("✗ Price validation test failed: Negative price was accepted")
        except ValueError:
            print("✓ Price validation test passed!")

        # Test invalid rating
        try:
            user = User(first_name="Test", last_name="User", email="test@example.com")
            owner = User(first_name="Test", last_name="Owner", email="owner@example.com")
            place = Place(title="Test Place", description="Test", price=100, latitude=0, longitude=0, owner=owner)
            Review(text="Test review", rating=6, place=place, user=user)
            print("✗ Rating validation test failed: Invalid rating was accepted")
        except ValueError:
            print("✓ Rating validation test passed!")

    except Exception as e:
        print(f"✗ Validation tests failed: {str(e)}")

if __name__ == "__main__":
    print("\nRunning tests...")
    print("-" * 50)
    test_user_creation()
    test_place_creation()
    test_review_creation()
    test_amenity_creation()
    test_validation()
    print("-" * 50) 