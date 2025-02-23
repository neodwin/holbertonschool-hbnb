"""
Module de tests pour les endpoints API liés aux avis (reviews).
Ce module contient tous les tests unitaires pour vérifier le bon fonctionnement
des opérations CRUD (Create, Read, Update, Delete) sur les avis, ainsi que
leurs relations avec les utilisateurs et les lieux.
"""

import json
import pytest
from app import create_app
import time
import uuid

@pytest.fixture
def client():
    """
    Fixture pytest qui configure un client de test.
    
    Cette fixture:
    1. Crée une instance de l'application en mode test
    2. Configure le client de test
    3. Fournit le client pour les tests
    
    Returns:
        FlaskClient: Client de test Flask configuré
    """
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_user(client):
    """
    Fixture pytest qui crée un utilisateur de test.
    
    Cette fixture:
    1. Génère un email unique avec UUID pour éviter les conflits
    2. Crée un nouvel utilisateur via l'API
    3. Retourne l'ID de l'utilisateur créé
    
    Args:
        client (FlaskClient): Client de test Flask
    
    Returns:
        str: ID de l'utilisateur de test créé
    """
    # Utilisation d'un UUID pour garantir l'unicité de l'email
    unique_id = str(uuid.uuid4())
    unique_email = f"test.user.{unique_id}@example.com"
    
    response = client.post('/api/v1/users/', json={
        'first_name': 'Test',
        'last_name': 'User',
        'email': unique_email
    })
    
    # Sortie de débogage pour faciliter le diagnostic
    print(f"User creation response status: {response.status_code}")
    print(f"User creation response data: {response.data}")
    
    # Analyse de la réponse
    data = json.loads(response.data)
    print(f"Parsed user data: {data}")
    print(f"Keys in user data: {data.keys()}")
    
    return data['id']

@pytest.fixture
def test_place(client, test_user):
    """
    Fixture pytest qui crée un lieu de test.
    
    Cette fixture:
    1. Crée un nouveau lieu via l'API
    2. Associe le lieu à l'utilisateur de test
    3. Retourne l'ID du lieu créé
    
    Args:
        client (FlaskClient): Client de test Flask
        test_user (str): ID de l'utilisateur de test
    
    Returns:
        str: ID du lieu de test créé
    """
    response = client.post('/api/v1/places/', json={
        'title': 'Test Place',
        'description': 'A place for testing',
        'price': 100.0,
        'latitude': 37.7749,
        'longitude': -122.4194,
        'owner_id': test_user,
        'amenities': []
    })
    return json.loads(response.data)['id']

def test_create_review(client, test_user, test_place):
    """
    Test de l'endpoint de création d'un avis.
    
    Scénarios testés:
    1. Création réussie d'un avis avec données valides
    2. Tentative de création avec une note invalide
    3. Tentative de création avec un utilisateur inexistant
    
    Args:
        client (FlaskClient): Client de test Flask
        test_user (str): ID de l'utilisateur de test
        test_place (str): ID du lieu de test
    """
    # Test de création réussie d'un avis
    response = client.post('/api/v1/reviews/', json={
        'text': 'Great place to stay!',
        'rating': 5,
        'user_id': test_user,
        'place_id': test_place
    })
    assert response.status_code == 201  # Vérifie le code de statut Created
    data = json.loads(response.data)
    assert data['text'] == 'Great place to stay!'  # Vérifie le texte de l'avis
    assert data['rating'] == 5                     # Vérifie la note
    assert data['user']['id'] == test_user        # Vérifie l'ID de l'utilisateur
    assert data['place']['id'] == test_place      # Vérifie l'ID du lieu

    # Test avec une note invalide
    response = client.post('/api/v1/reviews/', json={
        'text': 'Test review',
        'rating': 6,  # Note invalide (doit être entre 1 et 5)
        'user_id': test_user,
        'place_id': test_place
    })
    assert response.status_code == 400  # Vérifie le code de statut Bad Request

    # Test avec un utilisateur inexistant
    response = client.post('/api/v1/reviews/', json={
        'text': 'Test review',
        'rating': 5,
        'user_id': 'nonexistent-id',
        'place_id': test_place
    })
    assert response.status_code == 400  # Vérifie le code de statut Bad Request

def test_get_reviews(client, test_user, test_place):
    """
    Test de l'endpoint de récupération des avis.
    
    Scénarios testés:
    1. Création de plusieurs avis de test
    2. Récupération et vérification de la liste des avis
    
    Args:
        client (FlaskClient): Client de test Flask
        test_user (str): ID de l'utilisateur de test
        test_place (str): ID du lieu de test
    """
    # Création des avis de test
    client.post('/api/v1/reviews/', json={
        'text': 'First review',
        'rating': 4,
        'user_id': test_user,
        'place_id': test_place
    })
    client.post('/api/v1/reviews/', json={
        'text': 'Second review',
        'rating': 5,
        'user_id': test_user,
        'place_id': test_place
    })

    # Test de récupération de tous les avis
    response = client.get('/api/v1/reviews/')
    assert response.status_code == 200  # Vérifie le code de statut OK
    data = json.loads(response.data)
    assert isinstance(data, list)       # Vérifie que le résultat est une liste
    assert len(data) >= 2              # Vérifie qu'il y a au moins 2 avis
    # Vérifie la présence des champs requis pour chaque avis
    assert all('text' in review for review in data)
    assert all('rating' in review for review in data)
    assert all('user' in review for review in data)
    assert all('place' in review for review in data)

def test_get_review_by_id(client, test_user, test_place):
    """
    Test de l'endpoint de récupération d'un avis par son ID.
    
    Scénarios testés:
    1. Récupération d'un avis existant
    2. Tentative de récupération d'un avis inexistant
    
    Args:
        client (FlaskClient): Client de test Flask
        test_user (str): ID de l'utilisateur de test
        test_place (str): ID du lieu de test
    """
    # Création d'un avis de test
    response = client.post('/api/v1/reviews/', json={
        'text': 'Test review',
        'rating': 5,
        'user_id': test_user,
        'place_id': test_place
    })
    review_id = json.loads(response.data)['id']

    # Test de récupération d'un avis existant
    response = client.get(f'/api/v1/reviews/{review_id}')
    assert response.status_code == 200  # Vérifie le code de statut OK
    data = json.loads(response.data)
    assert data['id'] == review_id      # Vérifie l'ID de l'avis
    assert data['text'] == 'Test review' # Vérifie le texte de l'avis
    assert data['rating'] == 5           # Vérifie la note

    # Test de récupération d'un avis inexistant
    response = client.get('/api/v1/reviews/nonexistent-id')
    assert response.status_code == 404  # Vérifie le code de statut Not Found

def test_update_review(client, test_user, test_place):
    """
    Test de l'endpoint de mise à jour d'un avis.
    
    Scénarios testés:
    1. Mise à jour réussie d'un avis existant
    2. Tentative de mise à jour avec une note invalide
    3. Tentative de mise à jour d'un avis inexistant
    
    Args:
        client (FlaskClient): Client de test Flask
        test_user (str): ID de l'utilisateur de test
        test_place (str): ID du lieu de test
    """
    # Création d'un avis de test
    response = client.post('/api/v1/reviews/', json={
        'text': 'Original review',
        'rating': 4,
        'user_id': test_user,
        'place_id': test_place
    })
    review_id = json.loads(response.data)['id']

    # Test de mise à jour réussie
    response = client.put(f'/api/v1/reviews/{review_id}', json={
        'text': 'Updated review',
        'rating': 5
    })
    assert response.status_code == 200  # Vérifie le code de statut OK
    data = json.loads(response.data)
    assert data['text'] == 'Updated review'  # Vérifie la mise à jour du texte
    assert data['rating'] == 5               # Vérifie la mise à jour de la note

    # Test de mise à jour avec une note invalide
    response = client.put(f'/api/v1/reviews/{review_id}', json={
        'rating': 6  # Note invalide (doit être entre 1 et 5)
    })
    assert response.status_code == 400  # Vérifie le code de statut Bad Request

    # Test de mise à jour d'un avis inexistant
    response = client.put('/api/v1/reviews/nonexistent-id', json={
        'text': 'Test',
        'rating': 5
    })
    assert response.status_code == 404  # Vérifie le code de statut Not Found

def test_delete_review(client, test_user, test_place):
    """
    Test de l'endpoint de suppression d'un avis.
    
    Scénarios testés:
    1. Suppression réussie d'un avis existant
    2. Vérification que l'avis a bien été supprimé
    3. Tentative de suppression d'un avis inexistant
    
    Args:
        client (FlaskClient): Client de test Flask
        test_user (str): ID de l'utilisateur de test
        test_place (str): ID du lieu de test
    """
    # Création d'un avis de test
    response = client.post('/api/v1/reviews/', json={
        'text': 'Review to delete',
        'rating': 5,
        'user_id': test_user,
        'place_id': test_place
    })
    review_id = json.loads(response.data)['id']

    # Test de suppression réussie
    response = client.delete(f'/api/v1/reviews/{review_id}')
    assert response.status_code == 200  # Vérifie le code de statut OK
    data = json.loads(response.data)
    assert data['message'] == 'Review deleted successfully'  # Vérifie le message de confirmation

    # Vérification de la suppression de l'avis
    response = client.get(f'/api/v1/reviews/{review_id}')
    assert response.status_code == 404  # Vérifie que l'avis n'existe plus

    # Test de suppression d'un avis inexistant
    response = client.delete('/api/v1/reviews/nonexistent-id')
    assert response.status_code == 404  # Vérifie le code de statut Not Found

def test_get_place_reviews(client, test_user, test_place):
    """
    Test de l'endpoint de récupération des avis d'un lieu.
    
    Scénarios testés:
    1. Création de plusieurs avis pour un lieu
    2. Récupération et vérification des avis du lieu
    3. Tentative de récupération des avis d'un lieu inexistant
    
    Args:
        client (FlaskClient): Client de test Flask
        test_user (str): ID de l'utilisateur de test
        test_place (str): ID du lieu de test
    """
    # Création des avis de test pour le lieu
    client.post('/api/v1/reviews/', json={
        'text': 'First place review',
        'rating': 4,
        'user_id': test_user,
        'place_id': test_place
    })
    client.post('/api/v1/reviews/', json={
        'text': 'Second place review',
        'rating': 5,
        'user_id': test_user,
        'place_id': test_place
    })

    # Test de récupération des avis d'un lieu existant
    response = client.get(f'/api/v1/places/{test_place}/reviews')
    assert response.status_code == 200  # Vérifie le code de statut OK
    data = json.loads(response.data)
    assert isinstance(data, list)       # Vérifie que le résultat est une liste
    assert len(data) >= 2              # Vérifie qu'il y a au moins 2 avis
    # Vérifie que tous les avis appartiennent au bon lieu
    assert all(review['place']['id'] == test_place for review in data)

    # Test de récupération des avis d'un lieu inexistant
    response = client.get('/api/v1/places/nonexistent-id/reviews')
    assert response.status_code == 404  # Vérifie le code de statut Not Found

if __name__ == '__main__':
    pytest.main(['-v'])  # Exécution des tests en mode verbeux 