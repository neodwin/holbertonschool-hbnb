from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, email):
        """Get a user by email"""
        return self.get_by_attribute('email', email)
    
    def create_user(self, user_data):
        """Create a new user with validation"""
        # Check if email already exists
        if self.get_by_email(user_data.get('email')):
            raise ValueError('Email already registered')
        
        # Create and add the user
        user = User(**user_data)
        self.add(user)
        return user
    
    def update_user(self, user_id, user_data):
        """Update a user with validation"""
        user = self.get(user_id)
        if not user:
            return None
            
        # Check email uniqueness if email is being updated
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = self.get_by_email(user_data['email'])
            if existing_user:
                raise ValueError('Email already registered')
                
        # Update the user
        user.update(user_data)
        return user 