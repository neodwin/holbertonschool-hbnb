"""
Module de tests pour les endpoints API liés aux lieux (places).
Ce module contient tous les tests unitaires pour vérifier le bon fonctionnement
des opérations CRUD (Create, Read, Update, Delete) sur les lieux, ainsi que
leurs relations avec les utilisateurs et les commodités.
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
    unique_email = f"test.owner.{unique_id}@example.com"
    
    response = client.post('/api/v1/users/', json={
        'first_name': 'Test',
        'last_name': 'Owner',
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
def test_amenities(client):
    """
    Fixture pytest qui crée des commodités de test.
    
    Cette fixture:
    1. Crée plusieurs commodités via l'API
    2. Retourne leurs IDs pour utilisation dans les tests
    
    Args:
        client (FlaskClient): Client de test Flask
    
    Returns:
        list: Liste des IDs des commodités créées
    """
    amenities = []
    for name in ['Wi-Fi', 'Parking']:
        response = client.post('/api/v1/amenities/', json={'name': name})
        amenities.append(json.loads(response.data)['id'])
    return amenities

def test_create_place(client, test_user, test_amenities):
    """
    Test de l'endpoint de création d'un lieu.
    
    Scénarios testés:
    1. Création réussie d'un lieu avec toutes les données valides
    2. Tentative de création avec un prix invalide (négatif)
    3. Tentative de création avec des coordonnées invalides
    
    Args:
        client (FlaskClient): Client de test Flask
        test_user (str): ID de l'utilisateur de test
        test_amenities (list): Liste des IDs des commodités de test
    """
    # Test de création réussie
    response = client.post('/api/v1/places/', json={
        'title': 'Cozy Apartment',
        'description': 'A nice place to stay',
        'price': 100.0,
        'latitude': 37.7749,
        'longitude': -122.4194,
        'owner_id': test_user,
        'amenities': test_amenities
    })
    assert response.status_code == 201  # Vérifie le code de statut Created
    data = json.loads(response.data)
    assert data['title'] == 'Cozy Apartment'  # Vérifie le titre
    assert data['price'] == 100.0             # Vérifie le prix
    assert data['owner']['id'] == test_user   # Vérifie l'ID du propriétaire
    assert len(data['amenities']) == 2        # Vérifie le nombre de commodités

    # Test avec prix invalide
    response = client.post('/api/v1/places/', json={
        'title': 'Test Place',
        'description': 'Test',
        'price': -100,  # Prix négatif invalide
        'latitude': 0,
        'longitude': 0,
        'owner_id': test_user
    })
    assert response.status_code == 400  # Vérifie le code de statut Bad Request

    # Test avec coordonnées invalides
    response = client.post('/api/v1/places/', json={
        'title': 'Test Place',
        'description': 'Test',
        'price': 100,
        'latitude': 100,  # Latitude invalide (doit être entre -90 et 90)
        'longitude': 0,
        'owner_id': test_user
    })
    assert response.status_code == 400  # Vérifie le code de statut Bad Request

def test_get_places(client, test_user, test_amenities):
    """
    Test de l'endpoint de récupération des lieux.
    
    Scénarios testés:
    1. Création d'un lieu de test
    2. Récupération et vérification de la liste des lieux
    
    Args:
        client (FlaskClient): Client de test Flask
        test_user (str): ID de l'utilisateur de test
        test_amenities (list): Liste des IDs des commodités de test
    """
    # Création d'un lieu de test
    client.post('/api/v1/places/', json={
        'title': 'Beach House',
        'description': 'Beautiful beachfront property',
        'price': 200.0,
        'latitude': 25.7617,
        'longitude': -80.1918,
        'owner_id': test_user,
        'amenities': test_amenities
    })

    # Test de récupération de tous les lieux
    response = client.get('/api/v1/places/')
    assert response.status_code == 200  # Vérifie le code de statut OK
    data = json.loads(response.data)
    assert isinstance(data, list)       # Vérifie que le résultat est une liste
    assert len(data) > 0               # Vérifie qu'il y a au moins un lieu
    # Vérifie la présence des champs requis pour chaque lieu
    assert all('title' in place for place in data)
    assert all('owner' in place for place in data)
    assert all('amenities' in place for place in data)

def test_get_place_by_id(client, test_user, test_amenities):
    """
    Test de l'endpoint de récupération d'un lieu par son ID.
    
    Scénarios testés:
    1. Récupération d'un lieu existant
    2. Tentative de récupération d'un lieu inexistant
    
    Args:
        client (FlaskClient): Client de test Flask
        test_user (str): ID de l'utilisateur de test
        test_amenities (list): Liste des IDs des commodités de test
    """
    # Création d'un lieu de test
    response = client.post('/api/v1/places/', json={
        'title': 'Mountain Cabin',
        'description': 'Cozy cabin in the woods',
        'price': 150.0,
        'latitude': 39.5501,
        'longitude': -105.7821,
        'owner_id': test_user,
        'amenities': test_amenities
    })
    place_id = json.loads(response.data)['id']

    # Test de récupération d'un lieu existant
    response = client.get(f'/api/v1/places/{place_id}')
    assert response.status_code == 200  # Vérifie le code de statut OK
    data = json.loads(response.data)
    assert data['id'] == place_id           # Vérifie l'ID du lieu
    assert data['title'] == 'Mountain Cabin' # Vérifie le titre
    assert data['owner']['id'] == test_user  # Vérifie l'ID du propriétaire
    assert len(data['amenities']) == 2       # Vérifie le nombre de commodités

    # Test de récupération d'un lieu inexistant
    response = client.get('/api/v1/places/nonexistent-id')
    assert response.status_code == 404  # Vérifie le code de statut Not Found

def test_update_place(client, test_user, test_amenities):
    """
    Test de l'endpoint de mise à jour d'un lieu.
    
    Scénarios testés:
    1. Mise à jour réussie d'un lieu existant
    2. Tentative de mise à jour d'un lieu inexistant
    3. Tentative de mise à jour avec données invalides
    
    Args:
        client (FlaskClient): Client de test Flask
        test_user (str): ID de l'utilisateur de test
        test_amenities (list): Liste des IDs des commodités de test
    """
    # Création d'un lieu de test
    response = client.post('/api/v1/places/', json={
        'title': 'City Loft',
        'description': 'Urban living space',
        'price': 175.0,
        'latitude': 40.7128,
        'longitude': -74.0060,
        'owner_id': test_user,
        'amenities': test_amenities
    })
    place_id = json.loads(response.data)['id']

    # Test de mise à jour réussie
    response = client.put(f'/api/v1/places/{place_id}', json={
        'title': 'Luxury City Loft',
        'price': 200.0,
        'amenities': [test_amenities[0]]  # Mise à jour avec une seule commodité
    })
    assert response.status_code == 200  # Vérifie le code de statut OK
    data = json.loads(response.data)
    assert data['title'] == 'Luxury City Loft'  # Vérifie la mise à jour du titre
    assert data['price'] == 200.0               # Vérifie la mise à jour du prix
    assert len(data['amenities']) == 1          # Vérifie la mise à jour des commodités

    # Test de mise à jour d'un lieu inexistant
    response = client.put('/api/v1/places/nonexistent-id', json={
        'title': 'Test',
        'price': 100.0
    })
    assert response.status_code == 404  # Vérifie le code de statut Not Found

    # Test de mise à jour avec données invalides
    response = client.put(f'/api/v1/places/{place_id}', json={
        'price': -100  # Prix négatif invalide
    })
    assert response.status_code == 400  # Vérifie le code de statut Bad Request

if __name__ == '__main__':
    pytest.main(['-v'])  # Exécution des tests en mode verbeux 