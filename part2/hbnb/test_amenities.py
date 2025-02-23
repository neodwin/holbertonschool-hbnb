"""
Module de tests pour les endpoints API liés aux commodités (amenities).
Ce module contient tous les tests unitaires pour vérifier le bon fonctionnement
des opérations CRUD (Create, Read, Update, Delete) sur les commodités.
"""

import json
import pytest
from app import create_app

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

def test_create_amenity(client):
    """
    Test de l'endpoint de création d'une commodité.
    
    Scénarios testés:
    1. Création réussie d'une commodité avec données valides
    2. Tentative de création avec un nom vide (doit échouer)
    
    Args:
        client (FlaskClient): Client de test Flask (fixture)
    """
    # Test de création réussie d'une commodité
    response = client.post('/api/v1/amenities/', json={
        'name': 'Wi-Fi'
    })
    assert response.status_code == 201  # Vérifie le code de statut Created
    data = json.loads(response.data)
    assert data['name'] == 'Wi-Fi'     # Vérifie le nom de la commodité
    assert 'id' in data                 # Vérifie la présence d'un ID
    assert 'created_at' in data         # Vérifie la présence de la date de création
    assert 'updated_at' in data         # Vérifie la présence de la date de mise à jour

    # Test avec données invalides (nom vide)
    response = client.post('/api/v1/amenities/', json={
        'name': ''
    })
    assert response.status_code == 400  # Vérifie le code de statut Bad Request

def test_get_amenities(client):
    """
    Test de l'endpoint de récupération de toutes les commodités.
    
    Scénarios testés:
    1. Création de commodités de test
    2. Récupération et vérification de la liste complète
    
    Args:
        client (FlaskClient): Client de test Flask (fixture)
    """
    # Création des commodités de test
    client.post('/api/v1/amenities/', json={'name': 'Parking'})
    client.post('/api/v1/amenities/', json={'name': 'Pool'})

    # Test de récupération de toutes les commodités
    response = client.get('/api/v1/amenities/')
    assert response.status_code == 200  # Vérifie le code de statut OK
    data = json.loads(response.data)
    assert isinstance(data, list)       # Vérifie que le résultat est une liste
    assert len(data) >= 2              # Vérifie qu'il y a au moins les 2 commodités créées
    # Vérifie la présence des commodités créées
    assert any(amenity['name'] == 'Parking' for amenity in data)
    assert any(amenity['name'] == 'Pool' for amenity in data)

def test_get_amenity_by_id(client):
    """
    Test de l'endpoint de récupération d'une commodité par son ID.
    
    Scénarios testés:
    1. Récupération d'une commodité existante
    2. Tentative de récupération d'une commodité inexistante
    
    Args:
        client (FlaskClient): Client de test Flask (fixture)
    """
    # Création d'une commodité de test
    response = client.post('/api/v1/amenities/', json={
        'name': 'Air Conditioning'
    })
    amenity_id = json.loads(response.data)['id']

    # Test de récupération d'une commodité existante
    response = client.get(f'/api/v1/amenities/{amenity_id}')
    assert response.status_code == 200  # Vérifie le code de statut OK
    data = json.loads(response.data)
    assert data['id'] == amenity_id    # Vérifie l'ID de la commodité
    assert data['name'] == 'Air Conditioning'  # Vérifie le nom de la commodité

    # Test de récupération d'une commodité inexistante
    response = client.get('/api/v1/amenities/nonexistent-id')
    assert response.status_code == 404  # Vérifie le code de statut Not Found

def test_update_amenity(client):
    """
    Test de l'endpoint de mise à jour d'une commodité.
    
    Scénarios testés:
    1. Mise à jour réussie d'une commodité existante
    2. Tentative de mise à jour d'une commodité inexistante
    3. Tentative de mise à jour avec données invalides
    
    Args:
        client (FlaskClient): Client de test Flask (fixture)
    """
    # Création d'une commodité de test
    response = client.post('/api/v1/amenities/', json={
        'name': 'Kitchen'
    })
    amenity_id = json.loads(response.data)['id']

    # Test de mise à jour réussie
    response = client.put(f'/api/v1/amenities/{amenity_id}', json={
        'name': 'Full Kitchen'
    })
    assert response.status_code == 200  # Vérifie le code de statut OK
    data = json.loads(response.data)
    assert data['name'] == 'Full Kitchen'  # Vérifie la mise à jour du nom

    # Test de mise à jour d'une commodité inexistante
    response = client.put('/api/v1/amenities/nonexistent-id', json={
        'name': 'Test'
    })
    assert response.status_code == 404  # Vérifie le code de statut Not Found

    # Test de mise à jour avec données invalides
    response = client.put(f'/api/v1/amenities/{amenity_id}', json={
        'name': ''  # Nom vide invalide
    })
    assert response.status_code == 400  # Vérifie le code de statut Bad Request

if __name__ == '__main__':
    pytest.main(['-v'])  # Exécution des tests en mode verbeux 