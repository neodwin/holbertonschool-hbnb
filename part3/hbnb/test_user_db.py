from app import create_app
from app.extensions import db
from app.models.user import User
from app.db_init import init_db
import json

def test_user_crud():
    """Test CRUD operations for User model"""
    app = create_app('testing')
    
    with app.app_context():
        # Initialize the database
        db.create_all()
        
        # Create a test user
        test_user = User(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='testpassword'
        )
        db.session.add(test_user)
        db.session.commit()
        
        # Retrieve the user
        user = User.query.filter_by(email='test@example.com').first()
        assert user is not None
        assert user.first_name == 'Test'
        assert user.last_name == 'User'
        assert user.check_password('testpassword')
        
        # Update the user
        user.first_name = 'Updated'
        db.session.commit()
        
        # Verify update
        updated_user = User.query.get(user.id)
        assert updated_user.first_name == 'Updated'
        
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        
        # Verify deletion
        deleted_user = User.query.get(user.id)
        assert deleted_user is None
        
        print("All User CRUD tests passed!")
        
        # Clean up
        db.drop_all()

if __name__ == '__main__':
    test_user_crud() 