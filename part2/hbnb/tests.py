"""
Module de tests unitaires pour les modèles de l'application HBnB.
Ce module teste la création et la validation des différentes entités
(utilisateurs, lieux, avis, commodités) ainsi que leurs relations.
"""

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def test_user_creation():
    """
    Test de la création et de la validation d'un utilisateur.
    
    Vérifie:
    1. La création correcte d'un utilisateur avec des données valides
    2. L'attribution correcte des attributs
    3. La valeur par défaut du statut administrateur
    """
    try:
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        assert user.first_name == "John"          # Vérifie le prénom
        assert user.last_name == "Doe"            # Vérifie le nom
        assert user.email == "john.doe@example.com" # Vérifie l'email
        assert user.is_admin is False             # Vérifie le statut non-admin par défaut
        print("✓ Test de création d'utilisateur réussi!")
    except Exception as e:
        print(f"✗ Échec du test de création d'utilisateur: {str(e)}")

def test_place_creation():
    """
    Test de la création d'un lieu et de ses relations.
    
    Vérifie:
    1. La création correcte d'un lieu avec des données valides
    2. La relation bidirectionnelle avec le propriétaire
    3. L'attribution correcte des attributs
    """
    try:
        # Création d'un propriétaire pour le lieu
        owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
        place = Place(
            title="Cozy Apartment",
            description="A nice place to stay",
            price=100,
            latitude=37.7749,
            longitude=-122.4194,
            owner=owner
        )

        assert place.title == "Cozy Apartment"  # Vérifie le titre
        assert place.price == 100.0            # Vérifie le prix
        assert place.owner == owner            # Vérifie la relation avec le propriétaire
        assert place in owner.places           # Vérifie la relation inverse
        print("✓ Test de création de lieu et de relation réussi!")
    except Exception as e:
        print(f"✗ Échec du test de création de lieu: {str(e)}")

def test_review_creation():
    """
    Test de la création d'un avis et de ses relations.
    
    Vérifie:
    1. La création correcte d'un avis avec des données valides
    2. Les relations avec l'utilisateur et le lieu
    3. L'attribution correcte des attributs
    """
    try:
        # Création des utilisateurs nécessaires
        user = User(first_name="Bob", last_name="Johnson", email="bob.j@example.com")
        owner = User(first_name="Carol", last_name="Wilson", email="carol.w@example.com")
        
        # Création du lieu associé
        place = Place(
            title="Beach House",
            description="Beautiful beachfront property",
            price=200,
            latitude=25.7617,
            longitude=-80.1918,
            owner=owner
        )
        
        # Création de l'avis
        review = Review(text="Amazing stay!", rating=5, place=place, user=user)

        assert review.text == "Amazing stay!"  # Vérifie le texte de l'avis
        assert review.rating == 5             # Vérifie la note
        assert review in place.reviews        # Vérifie la relation avec le lieu
        print("✓ Test de création d'avis et de relations réussi!")
    except Exception as e:
        print(f"✗ Échec du test de création d'avis: {str(e)}")

def test_amenity_creation():
    """
    Test de la création de commodités et de leurs relations avec un lieu.
    
    Vérifie:
    1. La création correcte des commodités
    2. L'ajout des commodités à un lieu
    3. Les relations entre lieu et commodités
    """
    try:
        # Création du propriétaire et du lieu
        owner = User(first_name="David", last_name="Brown", email="david.b@example.com")
        place = Place(
            title="Mountain Cabin",
            description="Cozy cabin in the woods",
            price=150,
            latitude=39.5501,
            longitude=-105.7821,
            owner=owner
        )
        
        # Création des commodités
        wifi = Amenity(name="Wi-Fi")
        parking = Amenity(name="Parking")

        # Ajout des commodités au lieu
        place.add_amenity(wifi)
        place.add_amenity(parking)

        assert wifi in place.amenities      # Vérifie la présence du Wi-Fi
        assert parking in place.amenities   # Vérifie la présence du parking
        assert len(place.amenities) == 2    # Vérifie le nombre total de commodités
        print("✓ Test de création de commodités et de relations réussi!")
    except Exception as e:
        print(f"✗ Échec du test de création de commodités: {str(e)}")

def test_validation():
    """
    Test des validations d'entrée pour les différents modèles.
    
    Vérifie:
    1. La validation des adresses email
    2. La validation des prix (pas de valeurs négatives)
    3. La validation des notes (entre 1 et 5)
    """
    try:
        # Test de validation d'email
        try:
            User(first_name="Test", last_name="User", email="invalid-email")
            print("✗ Échec du test de validation d'email: Email invalide accepté")
        except ValueError:
            print("✓ Test de validation d'email réussi!")

        # Test de validation de prix
        try:
            owner = User(first_name="Test", last_name="Owner", email="test@example.com")
            Place(title="Test Place", description="Test", price=-100, latitude=0, longitude=0, owner=owner)
            print("✗ Échec du test de validation de prix: Prix négatif accepté")
        except ValueError:
            print("✓ Test de validation de prix réussi!")

        # Test de validation de note
        try:
            user = User(first_name="Test", last_name="User", email="test@example.com")
            owner = User(first_name="Test", last_name="Owner", email="owner@example.com")
            place = Place(title="Test Place", description="Test", price=100, latitude=0, longitude=0, owner=owner)
            Review(text="Test review", rating=6, place=place, user=user)
            print("✗ Échec du test de validation de note: Note invalide acceptée")
        except ValueError:
            print("✓ Test de validation de note réussi!")

    except Exception as e:
        print(f"✗ Échec des tests de validation: {str(e)}")

if __name__ == "__main__":
    print("\nExécution des tests...")
    print("-" * 50)
    test_user_creation()
    test_place_creation()
    test_review_creation()
    test_amenity_creation()
    test_validation()
    print("-" * 50) 