import json
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_user(client):
    """Test user creation endpoint"""
    # Test successful user creation
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

    # Test duplicate email
    response = client.post('/api/v1/users/', json={
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'john.doe@example.com'
    })
    assert response.status_code == 400
    assert b'Email already registered' in response.data

def test_get_users(client):
    """Test get users endpoint"""
    # Create a test user first
    client.post('/api/v1/users/', json={
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test.user@example.com'
    })

    # Test get all users
    response = client.get('/api/v1/users/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_user_by_id(client):
    """Test get user by ID endpoint"""
    # Create a test user
    response = client.post('/api/v1/users/', json={
        'first_name': 'Get',
        'last_name': 'User',
        'email': 'get.user@example.com'
    })
    user_id = json.loads(response.data)['id']

    # Test get existing user
    response = client.get(f'/api/v1/users/{user_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == user_id

    # Test get non-existent user
    response = client.get('/api/v1/users/nonexistent-id')
    assert response.status_code == 404

def test_update_user(client):
    """Test update user endpoint"""
    # Create a test user
    response = client.post('/api/v1/users/', json={
        'first_name': 'Update',
        'last_name': 'User',
        'email': 'update.user@example.com'
    })
    user_id = json.loads(response.data)['id']

    # Test successful update
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

    # Test update non-existent user
    response = client.put('/api/v1/users/nonexistent-id', json={
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com'
    })
    assert response.status_code == 404

    # Test update with invalid data
    response = client.put(f'/api/v1/users/{user_id}', json={
        'first_name': '',  # Empty name should be invalid
        'last_name': 'Test',
        'email': 'test@example.com'
    })
    assert response.status_code == 400 