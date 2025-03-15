import json
import pytest
from app import create_app

def test_debug_user_creation():
    """Debug test for user creation"""
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        # Create a user with the same data as in the test fixtures
        response = client.post('/api/v1/users/', json={
            'first_name': 'Test',
            'last_name': 'Owner',
            'email': 'test.owner@example.com'
        })
        
        # Print response status and data
        print(f"Status code: {response.status_code}")
        print(f"Response data: {response.data}")
        
        # Try to parse the JSON
        try:
            data = json.loads(response.data)
            print(f"Parsed JSON: {data}")
            print(f"Keys in response: {data.keys()}")
            
            # Try to access the 'id' key
            user_id = data.get('id')
            print(f"User ID: {user_id}")
            
            if 'id' not in data:
                print("WARNING: 'id' key is missing from the response!")
        except Exception as e:
            print(f"Error parsing JSON: {e}")
        
        # Assert something to make the test pass
        assert response.status_code == 201

if __name__ == "__main__":
    test_debug_user_creation() 