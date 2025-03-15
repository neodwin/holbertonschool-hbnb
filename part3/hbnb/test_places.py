#!/usr/bin/env python3
"""
Tests pour l'API des logements (places) de l'application HolbertonBnB.
Ce module teste les endpoints REST pour la gestion des logements,
y compris la création, la récupération, la mise à jour et l'association
avec des utilisateurs et des équipements.
"""

import json
import pytest
from app import create_app
import time
import uuid

@pytest.fixture
def client():
    """
    Fixture pytest qui fournit un client de test pour les requêtes HTTP.
    
    Cette fixture crée une instance de l'application en mode test,
    et retourne un client qui peut être utilisé pour simuler des 
    requêtes HTTP vers les endpoints de l'API.
    
    Returns:
        FlaskClient: Un client Flask configuré pour les tests
    """
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_user(client):
    """
    Fixture qui crée un utilisateur de test et retourne son ID.
    
    Cette fixture est utilisée pour créer un propriétaire pour les logements
    dans les tests. Elle génère un email unique pour éviter les conflits de duplication.
    
    Args:
        client: Le client de test Flask fourni par la fixture client
        
    Returns:
        str: L'identifiant de l'utilisateur créé
    """
    # Utilise un UUID pour garantir l'unicité de l'email
    unique_id = str(uuid.uuid4())
    unique_email = f"test.owner.{unique_id}@example.com"
    
    response = client.post('/api/v1/users/', json={
        'first_name': 'Test',
        'last_name': 'Owner',
        'email': unique_email
    })
    
    # Informations de débogage
    print(f"User creation response status: {response.status_code}")
    print(f"User creation response data: {response.data}")
    
    # Analyse de la réponse
    data = json.loads(response.data)
    print(f"Parsed user data: {data}")
    print(f"Keys in user data: {data.keys()}")
    
    # Retourne l'ID de l'utilisateur
    return data['id']

@pytest.fixture
def test_amenities(client):
    """
    Fixture qui crée des équipements de test et retourne leurs IDs.
    
    Cette fixture est utilisée pour créer des équipements qui pourront
    être associés aux logements dans les tests.
    
    Args:
        client: Le client de test Flask fourni par la fixture client
        
    Returns:
        list: Liste d'identifiants des équipements créés
    """
    amenities = []
    for name in ['Wi-Fi', 'Parking']:
        response = client.post('/api/v1/amenities/', json={'name': name})
        amenities.append(json.loads(response.data)['id'])
    return amenities

def test_create_place(client, test_user, test_amenities):
    """
    Teste l'endpoint de création de logement.
    
    Ce test vérifie:
    1. La création réussie d'un logement avec des données valides
    2. L'association du logement avec son propriétaire
    3. L'association du logement avec des équipements
    4. Le rejet de données invalides
    
    Args:
        client: Le client de test Flask
        test_user: L'ID de l'utilisateur propriétaire (de la fixture)
        test_amenities: Liste d'IDs d'équipements (de la fixture)
    """
    # Test de création réussie d'un logement
    response = client.post('/api/v1/places/', json={
        'title': 'Cozy Apartment',
        'description': 'A nice place to stay',
        'price': 100.0,
        'latitude': 37.7749,
        'longitude': -122.4194,
        'owner_id': test_user,
        'amenities': test_amenities
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Cozy Apartment'
    assert data['price'] == 100.0
    assert data['owner']['id'] == test_user
    assert len(data['amenities']) == 2

    # Test invalid price
    response = client.post('/api/v1/places/', json={
        'title': 'Test Place',
        'description': 'Test',
        'price': -100,
        'latitude': 0,
        'longitude': 0,
        'owner_id': test_user
    })
    assert response.status_code == 400

    # Test invalid coordinates
    response = client.post('/api/v1/places/', json={
        'title': 'Test Place',
        'description': 'Test',
        'price': 100,
        'latitude': 100,  # Invalid latitude
        'longitude': 0,
        'owner_id': test_user
    })
    assert response.status_code == 400

def test_get_places(client, test_user, test_amenities):
    """Test get places endpoint"""
    # Create test places
    client.post('/api/v1/places/', json={
        'title': 'Beach House',
        'description': 'Beautiful beachfront property',
        'price': 200.0,
        'latitude': 25.7617,
        'longitude': -80.1918,
        'owner_id': test_user,
        'amenities': test_amenities
    })

    # Test get all places
    response = client.get('/api/v1/places/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert all('title' in place for place in data)
    assert all('owner' in place for place in data)
    assert all('amenities' in place for place in data)

def test_get_place_by_id(client, test_user, test_amenities):
    """Test get place by ID endpoint"""
    # Create a test place
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

    # Test get existing place
    response = client.get(f'/api/v1/places/{place_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == place_id
    assert data['title'] == 'Mountain Cabin'
    assert data['owner']['id'] == test_user
    assert len(data['amenities']) == 2

    # Test get non-existent place
    response = client.get('/api/v1/places/nonexistent-id')
    assert response.status_code == 404

def test_update_place(client, test_user, test_amenities):
    """Test update place endpoint"""
    # Create a test place
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

    # Test successful update
    response = client.put(f'/api/v1/places/{place_id}', json={
        'title': 'Luxury City Loft',
        'price': 200.0,
        'amenities': [test_amenities[0]]  # Update with only one amenity
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Luxury City Loft'
    assert data['price'] == 200.0
    assert len(data['amenities']) == 1

    # Test update non-existent place
    response = client.put('/api/v1/places/nonexistent-id', json={
        'title': 'Test',
        'price': 100.0
    })
    assert response.status_code == 404

    # Test update with invalid data
    response = client.put(f'/api/v1/places/{place_id}', json={
        'price': -100  # Invalid price
    })
    assert response.status_code == 400

if __name__ == '__main__':
    pytest.main(['-v']) 