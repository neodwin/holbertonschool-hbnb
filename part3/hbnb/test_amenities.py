#!/usr/bin/env python3
"""
Tests pour l'API des équipements (amenities) de l'application HolbertonBnB.
Ce module teste les endpoints REST permettant de gérer les équipements,
y compris la création, la récupération, la mise à jour et la suppression.
"""

import json
import pytest
from app import create_app

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

def test_create_amenity(client):
    """
    Teste l'endpoint de création d'équipement.
    
    Ce test vérifie:
    1. La création réussie d'un équipement avec des données valides
    2. Le rejet approprié des données invalides (nom vide)
    
    Args:
        client: Le client de test Flask fourni par la fixture
    """
    # Test de création réussie d'un équipement
    response = client.post('/api/v1/amenities/', json={
        'name': 'Wi-Fi'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Wi-Fi'
    assert 'id' in data
    assert 'created_at' in data
    assert 'updated_at' in data

    # Test avec données invalides (nom vide)
    response = client.post('/api/v1/amenities/', json={
        'name': ''
    })
    assert response.status_code == 400

def test_get_amenities(client):
    """
    Teste l'endpoint de récupération de tous les équipements.
    
    Ce test vérifie que l'API retourne correctement la liste de tous
    les équipements enregistrés en base de données.
    
    Args:
        client: Le client de test Flask fourni par la fixture
    """
    # Création d'équipements de test
    client.post('/api/v1/amenities/', json={'name': 'Parking'})
    client.post('/api/v1/amenities/', json={'name': 'Pool'})

    # Test de récupération de tous les équipements
    response = client.get('/api/v1/amenities/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 2
    assert any(amenity['name'] == 'Parking' for amenity in data)
    assert any(amenity['name'] == 'Pool' for amenity in data)

def test_get_amenity_by_id(client):
    """
    Teste l'endpoint de récupération d'un équipement par son identifiant.
    
    Ce test vérifie:
    1. La récupération correcte d'un équipement existant
    2. La gestion appropriée des requêtes pour des équipements inexistants
    
    Args:
        client: Le client de test Flask fourni par la fixture
    """
    # Création d'un équipement de test
    response = client.post('/api/v1/amenities/', json={
        'name': 'Air Conditioning'
    })
    amenity_id = json.loads(response.data)['id']

    # Test de récupération d'un équipement existant
    response = client.get(f'/api/v1/amenities/{amenity_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == amenity_id
    assert data['name'] == 'Air Conditioning'

    # Test de récupération d'un équipement inexistant
    response = client.get('/api/v1/amenities/nonexistent-id')
    assert response.status_code == 404

def test_update_amenity(client):
    """
    Teste l'endpoint de mise à jour d'un équipement.
    
    Ce test vérifie:
    1. La mise à jour réussie d'un équipement existant
    2. La gestion des tentatives de mise à jour d'équipements inexistants
    3. Le rejet de données invalides lors de la mise à jour
    
    Args:
        client: Le client de test Flask fourni par la fixture
    """
    # Création d'un équipement de test
    response = client.post('/api/v1/amenities/', json={
        'name': 'Kitchen'
    })
    amenity_id = json.loads(response.data)['id']

    # Test de mise à jour réussie
    response = client.put(f'/api/v1/amenities/{amenity_id}', json={
        'name': 'Full Kitchen'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Full Kitchen'

    # Test de mise à jour d'un équipement inexistant
    response = client.put('/api/v1/amenities/nonexistent-id', json={
        'name': 'Test'
    })
    assert response.status_code == 404

    # Test de mise à jour avec des données invalides
    response = client.put(f'/api/v1/amenities/{amenity_id}', json={
        'name': ''  # Un nom vide devrait être invalide
    })
    assert response.status_code == 400

if __name__ == '__main__':
    pytest.main(['-v']) 