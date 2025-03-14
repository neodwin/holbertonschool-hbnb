import json
import pytest
from app import create_app
import time
import uuid

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_user(client):
    """Create a test user and return their ID"""
    # Use a UUID to ensure email uniqueness
    unique_id = str(uuid.uuid4())
    unique_email = f"test.user.{unique_id}@example.com"
    
    response = client.post('/api/v1/users/', json={
        'first_name': 'Test',
        'last_name': 'User',
        'email': unique_email
    })
    
    # Debug output
    print(f"User creation response status: {response.status_code}")
    print(f"User creation response data: {response.data}")
    
    # Parse the response data
    data = json.loads(response.data)
    print(f"Parsed user data: {data}")
    print(f"Keys in user data: {data.keys()}")
    
    # Return the user ID
    return data['id']

@pytest.fixture
def test_place(client, test_user):
    """Create a test place and return its ID"""
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
    """Test review creation endpoint"""
    # Test successful review creation
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
    """Test get reviews endpoint"""
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
    """Test get review by ID endpoint"""
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
    """Test update review endpoint"""
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
    """Test delete review endpoint"""
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
    """Test get reviews by place endpoint"""
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