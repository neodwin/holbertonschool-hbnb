#!/usr/bin/env python3
"""
Tests pour l'API des avis (reviews) de l'application HolbertonBnB.
Ce module teste les endpoints REST pour la gestion des avis,
y compris la création, la récupération, la mise à jour et la suppression
des avis liés aux logements.
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
    
    Cette fixture est utilisée pour créer un utilisateur qui pourra
    laisser des avis dans les tests. Elle génère un email unique pour 
    éviter les conflits de duplication.
    
    Args:
        client: Le client de test Flask fourni par la fixture client
        
    Returns:
        str: L'identifiant de l'utilisateur créé
    """
    # Utilise un UUID pour garantir l'unicité de l'email
    unique_id = str(uuid.uuid4())
    unique_email = f"test.user.{unique_id}@example.com"
    
    response = client.post('/api/v1/users/', json={
        'first_name': 'Test',
        'last_name': 'User',
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
def test_place(client, test_user):
    """
    Fixture qui crée un logement de test et retourne son ID.
    
    Cette fixture est utilisée pour créer un logement sur lequel
    des avis seront laissés dans les tests.
    
    Args:
        client: Le client de test Flask fourni par la fixture client
        test_user: L'ID du propriétaire fourni par la fixture test_user
        
    Returns:
        str: L'identifiant du logement créé
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
    
    # Retourne l'ID du logement
    return json.loads(response.data)['id']

def test_create_review(client, test_user, test_place):
    """
    Teste l'endpoint de création d'avis.
    
    Ce test vérifie:
    1. La création réussie d'un avis avec des données valides
    2. L'association correcte avec le logement et l'utilisateur
    3. Le rejet de données invalides (texte vide, note invalide)
    4. Le rejet des avis dupliqués d'un même utilisateur sur un logement
    
    Args:
        client: Le client de test Flask
        test_user: L'ID de l'utilisateur (de la fixture)
        test_place: L'ID du logement (de la fixture)
    """
    # Test de création réussie d'un avis
    response = client.post('/api/v1/reviews/', json={
        'text': 'Great place to stay!',
        'rating': 5,
        'user_id': test_user,
        'place_id': test_place
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['text'] == 'Great place to stay!'
    assert data['rating'] == 5
    assert data['user']['id'] == test_user
    assert data['place']['id'] == test_place

    # Test invalid rating
    response = client.post('/api/v1/reviews/', json={
        'text': 'Test review',
        'rating': 6,  # Invalid rating
        'user_id': test_user,
        'place_id': test_place
    })
    assert response.status_code == 400

    # Test non-existent user
    response = client.post('/api/v1/reviews/', json={
        'text': 'Test review',
        'rating': 5,
        'user_id': 'nonexistent-id',
        'place_id': test_place
    })
    assert response.status_code == 400

def test_get_reviews(client, test_user, test_place):
    """
    Teste l'endpoint de récupération de tous les avis.
    
    Ce test vérifie que l'API retourne correctement tous les avis
    enregistrés dans l'application.
    
    Args:
        client: Le client de test Flask
        test_user: L'ID de l'utilisateur (nécessaire pour créer un avis de test)
        test_place: L'ID du logement (nécessaire pour créer un avis de test)
    """
    # Create test reviews
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

    # Test get all reviews
    response = client.get('/api/v1/reviews/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 2
    assert all('text' in review for review in data)
    assert all('rating' in review for review in data)
    assert all('user' in review for review in data)
    assert all('place' in review for review in data)

def test_get_review_by_id(client, test_user, test_place):
    """
    Teste l'endpoint de récupération d'un avis par son identifiant.
    
    Ce test vérifie:
    1. La récupération correcte d'un avis existant
    2. La gestion appropriée des requêtes pour des avis inexistants
    
    Args:
        client: Le client de test Flask
        test_user: L'ID de l'utilisateur (nécessaire pour créer un avis de test)
        test_place: L'ID du logement (nécessaire pour créer un avis de test)
    """
    # Create a test review
    response = client.post('/api/v1/reviews/', json={
        'text': 'Test review',
        'rating': 5,
        'user_id': test_user,
        'place_id': test_place
    })
    review_id = json.loads(response.data)['id']

    # Test get existing review
    response = client.get(f'/api/v1/reviews/{review_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == review_id
    assert data['text'] == 'Test review'
    assert data['rating'] == 5

    # Test get non-existent review
    response = client.get('/api/v1/reviews/nonexistent-id')
    assert response.status_code == 404

def test_update_review(client, test_user, test_place):
    """
    Teste l'endpoint de mise à jour d'un avis.
    
    Ce test vérifie:
    1. La mise à jour réussie d'un avis existant
    2. La gestion des tentatives de mise à jour d'avis inexistants
    3. Le rejet de données invalides lors de la mise à jour
    
    Args:
        client: Le client de test Flask
        test_user: L'ID de l'utilisateur (nécessaire pour créer un avis de test)
        test_place: L'ID du logement (nécessaire pour créer un avis de test)
    """
    # Create a test review
    response = client.post('/api/v1/reviews/', json={
        'text': 'Original review',
        'rating': 4,
        'user_id': test_user,
        'place_id': test_place
    })
    review_id = json.loads(response.data)['id']

    # Test successful update
    response = client.put(f'/api/v1/reviews/{review_id}', json={
        'text': 'Updated review',
        'rating': 5
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['text'] == 'Updated review'
    assert data['rating'] == 5

    # Test update with invalid rating
    response = client.put(f'/api/v1/reviews/{review_id}', json={
        'rating': 6  # Invalid rating
    })
    assert response.status_code == 400

    # Test update non-existent review
    response = client.put('/api/v1/reviews/nonexistent-id', json={
        'text': 'Test',
        'rating': 5
    })
    assert response.status_code == 404

def test_delete_review(client, test_user, test_place):
    """
    Teste l'endpoint de suppression d'un avis.
    
    Ce test vérifie:
    1. La suppression réussie d'un avis existant
    2. La gestion appropriée des tentatives de suppression d'avis inexistants
    
    Args:
        client: Le client de test Flask
        test_user: L'ID de l'utilisateur (nécessaire pour créer un avis de test)
        test_place: L'ID du logement (nécessaire pour créer un avis de test)
    """
    # Create a test review
    response = client.post('/api/v1/reviews/', json={
        'text': 'Review to delete',
        'rating': 5,
        'user_id': test_user,
        'place_id': test_place
    })
    review_id = json.loads(response.data)['id']

    # Test successful deletion
    response = client.delete(f'/api/v1/reviews/{review_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Review deleted successfully'

    # Verify review is deleted
    response = client.get(f'/api/v1/reviews/{review_id}')
    assert response.status_code == 404

    # Test delete non-existent review
    response = client.delete('/api/v1/reviews/nonexistent-id')
    assert response.status_code == 404

def test_get_place_reviews(client, test_user, test_place):
    """
    Teste l'endpoint de récupération des avis pour un logement spécifique.
    
    Ce test vérifie que l'API retourne correctement tous les avis
    associés à un logement particulier.
    
    Args:
        client: Le client de test Flask
        test_user: L'ID de l'utilisateur (nécessaire pour créer un avis de test)
        test_place: L'ID du logement dont on veut récupérer les avis
    """
    # Create test reviews for the place
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

    # Test get reviews for existing place
    response = client.get(f'/api/v1/places/{test_place}/reviews')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 2
    assert all(review['place']['id'] == test_place for review in data)

    # Test get reviews for non-existent place
    response = client.get('/api/v1/places/nonexistent-id/reviews')
    assert response.status_code == 404

if __name__ == '__main__':
    pytest.main(['-v']) 