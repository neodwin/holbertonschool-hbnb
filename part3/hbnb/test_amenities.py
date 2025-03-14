import json
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_amenity(client):
    """Test amenity creation endpoint"""
    # Test successful amenity creation
    response = client.post('/api/v1/amenities/', json={
        'name': 'Wi-Fi'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Wi-Fi'
    assert 'id' in data
    assert 'created_at' in data
    assert 'updated_at' in data

    # Test invalid data (empty name)
    response = client.post('/api/v1/amenities/', json={
        'name': ''
    })
    assert response.status_code == 400

def test_get_amenities(client):
    """Test get amenities endpoint"""
    # Create test amenities
    client.post('/api/v1/amenities/', json={'name': 'Parking'})
    client.post('/api/v1/amenities/', json={'name': 'Pool'})

    # Test get all amenities
    response = client.get('/api/v1/amenities/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 2
    assert any(amenity['name'] == 'Parking' for amenity in data)
    assert any(amenity['name'] == 'Pool' for amenity in data)

def test_get_amenity_by_id(client):
    """Test get amenity by ID endpoint"""
    # Create a test amenity
    response = client.post('/api/v1/amenities/', json={
        'name': 'Air Conditioning'
    })
    amenity_id = json.loads(response.data)['id']

    # Test get existing amenity
    response = client.get(f'/api/v1/amenities/{amenity_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == amenity_id
    assert data['name'] == 'Air Conditioning'

    # Test get non-existent amenity
    response = client.get('/api/v1/amenities/nonexistent-id')
    assert response.status_code == 404

def test_update_amenity(client):
    """Test update amenity endpoint"""
    # Create a test amenity
    response = client.post('/api/v1/amenities/', json={
        'name': 'Kitchen'
    })
    amenity_id = json.loads(response.data)['id']

    # Test successful update
    response = client.put(f'/api/v1/amenities/{amenity_id}', json={
        'name': 'Full Kitchen'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Full Kitchen'

    # Test update non-existent amenity
    response = client.put('/api/v1/amenities/nonexistent-id', json={
        'name': 'Test'
    })
    assert response.status_code == 404

    # Test update with invalid data
    response = client.put(f'/api/v1/amenities/{amenity_id}', json={
        'name': ''  # Empty name should be invalid
    })
    assert response.status_code == 400

if __name__ == '__main__':
    pytest.main(['-v']) 