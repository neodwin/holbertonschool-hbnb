import re
from app.models.base import BaseModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()

        # Validate user details
        self.validate_name(first_name, "first_name")
        self.validate_name(last_name, "last_name")
        self.validate_email(email)

        # Assign the user details
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []  # List to store owned places

        if password:
            self.set_password(password)  # Hash and store the password

    @staticmethod
    def validate_name(name, field):
        """Validate name fields"""
        if not name or not isinstance(name, str):
            raise ValueError(f"{field} is required and must be a string")
        if len(name) > 50:
            raise ValueError(f"{field} must not exceed 50 characters")

    @staticmethod
    def validate_email(email):
        """Validate email format"""
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            raise ValueError("Invalid email format")

    def set_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def add_place(self, place):
        """Add a place to user's owned places"""
        self.places.append(place)

    def update(self, data):
        """Update user attributes with validation"""
        if 'first_name' in data:
            self.validate_name(data['first_name'], "first_name")
        if 'last_name' in data:
            self.validate_name(data['last_name'], "last_name")
        if 'email' in data:
            self.validate_email(data['email'])
        
        # Ensure password update only when necessary and is hashed properly
        if 'password' in data:
            self.set_password(data['password'])
        
        super().update(data)

    def __repr__(self):
        """String representation of the User model, excluding the password."""
        return f"<User {self.first_name} {self.last_name} ({self.email})>"
