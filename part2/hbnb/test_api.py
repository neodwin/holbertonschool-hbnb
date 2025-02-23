"""
Module de tests pour les endpoints API liés aux utilisateurs.
Ce module contient tous les tests unitaires pour vérifier le bon fonctionnement
des opérations CRUD (Create, Read, Update, Delete) sur les utilisateurs.
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

def test_create_user(client):
    """
    Test de l'endpoint de création d'un utilisateur.
    
    Scénarios testés:
    1. Création réussie d'un utilisateur avec données valides
    2. Tentative de création avec un email déjà existant (doit échouer)
    
    Args:
        client (FlaskClient): Client de test Flask (fixture)
    """
    # Test de création réussie d'un utilisateur
    response = client.post('/api/v1/users/', json={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com'
    })
    assert response.status_code == 201  # Vérifie le code de statut Created
    data = json.loads(response.data)
    assert data['first_name'] == 'John'  # Vérifie le prénom
    assert data['last_name'] == 'Doe'    # Vérifie le nom
    assert data['email'] == 'john.doe@example.com'  # Vérifie l'email
    assert 'id' in data                  # Vérifie la présence d'un ID

    # Test avec un email en doublon
    response = client.post('/api/v1/users/', json={
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'john.doe@example.com'  # Email déjà utilisé
    })
    assert response.status_code == 400  # Vérifie le code de statut Bad Request
    assert b'Email already registered' in response.data  # Vérifie le message d'erreur

def test_get_users(client):
    """
    Test de l'endpoint de récupération de tous les utilisateurs.
    
    Scénarios testés:
    1. Création d'un utilisateur de test
    2. Récupération et vérification de la liste des utilisateurs
    
    Args:
        client (FlaskClient): Client de test Flask (fixture)
    """
    # Création d'un utilisateur de test
    client.post('/api/v1/users/', json={
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test.user@example.com'
    })

    # Test de récupération de tous les utilisateurs
    response = client.get('/api/v1/users/')
    assert response.status_code == 200  # Vérifie le code de statut OK
    data = json.loads(response.data)
    assert isinstance(data, list)       # Vérifie que le résultat est une liste
    assert len(data) > 0               # Vérifie qu'il y a au moins un utilisateur

def test_get_user_by_id(client):
    """
    Test de l'endpoint de récupération d'un utilisateur par son ID.
    
    Scénarios testés:
    1. Récupération d'un utilisateur existant
    2. Tentative de récupération d'un utilisateur inexistant
    
    Args:
        client (FlaskClient): Client de test Flask (fixture)
    """
    # Création d'un utilisateur de test
    response = client.post('/api/v1/users/', json={
        'first_name': 'Get',
        'last_name': 'User',
        'email': 'get.user@example.com'
    })
    user_id = json.loads(response.data)['id']

    # Test de récupération d'un utilisateur existant
    response = client.get(f'/api/v1/users/{user_id}')
    assert response.status_code == 200  # Vérifie le code de statut OK
    data = json.loads(response.data)
    assert data['id'] == user_id       # Vérifie l'ID de l'utilisateur

    # Test de récupération d'un utilisateur inexistant
    response = client.get('/api/v1/users/nonexistent-id')
    assert response.status_code == 404  # Vérifie le code de statut Not Found

def test_update_user(client):
    """
    Test de l'endpoint de mise à jour d'un utilisateur.
    
    Scénarios testés:
    1. Mise à jour réussie d'un utilisateur existant
    2. Tentative de mise à jour d'un utilisateur inexistant
    3. Tentative de mise à jour avec données invalides
    
    Args:
        client (FlaskClient): Client de test Flask (fixture)
    """
    # Création d'un utilisateur de test
    response = client.post('/api/v1/users/', json={
        'first_name': 'Update',
        'last_name': 'User',
        'email': 'update.user@example.com'
    })
    user_id = json.loads(response.data)['id']

    # Test de mise à jour réussie
    response = client.put(f'/api/v1/users/{user_id}', json={
        'first_name': 'Updated',
        'last_name': 'Name',
        'email': 'updated.user@example.com'
    })
    assert response.status_code == 200  # Vérifie le code de statut OK
    data = json.loads(response.data)
    assert data['first_name'] == 'Updated'  # Vérifie la mise à jour du prénom
    assert data['last_name'] == 'Name'      # Vérifie la mise à jour du nom
    assert data['email'] == 'updated.user@example.com'  # Vérifie la mise à jour de l'email

    # Test de mise à jour d'un utilisateur inexistant
    response = client.put('/api/v1/users/nonexistent-id', json={
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com'
    })
    assert response.status_code == 404  # Vérifie le code de statut Not Found

    # Test de mise à jour avec données invalides
    response = client.put(f'/api/v1/users/{user_id}', json={
        'first_name': '',  # Prénom vide invalide
        'last_name': 'Test',
        'email': 'test@example.com'
    })
    assert response.status_code == 400  # Vérifie le code de statut Bad Request 