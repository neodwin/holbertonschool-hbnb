#!/usr/bin/env python3
"""
Tests pour l'API des utilisateurs de l'application HolbertonBnB.
Ce module teste les endpoints REST pour la gestion des utilisateurs,
y compris la création, la récupération, et la mise à jour.
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

def test_create_user(client):
    """
    Teste l'endpoint de création d'utilisateur.
    
    Ce test vérifie:
    1. La création réussie d'un utilisateur avec des données valides
    2. Le rejet des tentatives de création d'utilisateurs avec un email déjà utilisé
    
    Args:
        client: Le client de test Flask fourni par la fixture
    """
    # Test de création réussie d'un utilisateur
    response = client.post('/api/v1/users/', json={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['first_name'] == 'John'
    assert data['last_name'] == 'Doe'
    assert data['email'] == 'john.doe@example.com'
    assert 'id' in data

    # Test d'email en doublon
    response = client.post('/api/v1/users/', json={
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'john.doe@example.com'
    })
    assert response.status_code == 400
    assert b'Email already registered' in response.data

def test_get_users(client):
    """
    Teste l'endpoint de récupération de tous les utilisateurs.
    
    Ce test vérifie que l'API retourne correctement la liste de tous
    les utilisateurs enregistrés dans l'application.
    
    Args:
        client: Le client de test Flask fourni par la fixture
    """
    # Création d'un utilisateur de test
    client.post('/api/v1/users/', json={
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test.user@example.com'
    })

    # Test de récupération de tous les utilisateurs
    response = client.get('/api/v1/users/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_user_by_id(client):
    """
    Teste l'endpoint de récupération d'un utilisateur par son identifiant.
    
    Ce test vérifie:
    1. La récupération correcte d'un utilisateur existant
    2. La gestion appropriée des requêtes pour des utilisateurs inexistants
    
    Args:
        client: Le client de test Flask fourni par la fixture
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
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == user_id

    # Test de récupération d'un utilisateur inexistant
    response = client.get('/api/v1/users/nonexistent-id')
    assert response.status_code == 404

def test_update_user(client):
    """
    Teste l'endpoint de mise à jour d'un utilisateur.
    
    Ce test vérifie:
    1. La mise à jour réussie d'un utilisateur existant
    2. La gestion des tentatives de mise à jour d'utilisateurs inexistants
    3. Le rejet de données invalides lors de la mise à jour
    
    Args:
        client: Le client de test Flask fourni par la fixture
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
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['first_name'] == 'Updated'
    assert data['last_name'] == 'Name'
    assert data['email'] == 'updated.user@example.com'

    # Test de mise à jour d'un utilisateur inexistant
    response = client.put('/api/v1/users/nonexistent-id', json={
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com'
    })
    assert response.status_code == 404

    # Test de mise à jour avec des données invalides
    response = client.put(f'/api/v1/users/{user_id}', json={
        'first_name': '',  # Un prénom vide devrait être invalide
        'last_name': 'Test',
        'email': 'test@example.com'
    })
    assert response.status_code == 400 