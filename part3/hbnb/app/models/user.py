import re
from app.models.base import BaseModel
from app.extensions import bcrypt, db

class User(BaseModel):
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    places = db.relationship('Place', backref='owner_rel', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user_rel', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, first_name, last_name, email, password=None, is_admin=False, **kwargs):
        self.validate_name(first_name, "first_name")
        self.validate_name(last_name, "last_name")
        self.validate_email(email)
        
        super().__init__(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_admin=is_admin,
            **kwargs
        )
        
        # Hash password if provided
        if password:
            self.set_password(password)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    def set_password(self, password):
        """Hash and set the password"""
        if not password or not isinstance(password, str):
            raise ValueError("Password is required and must be a string")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def check_password(self, password):
        """Check if the provided password matches the stored hash"""
        if not self._password_hash:
            return False
        return bcrypt.check_password_hash(self._password_hash, password)

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
        if 'password' in data:
            self.set_password(data['password'])
            # Remove password from data to prevent it from being stored in plaintext
            data = {k: v for k, v in data.items() if k != 'password'}
        
        super().update(data)
        
    def to_dict(self):
        """Convert user to dictionary without password"""
        user_dict = super().to_dict()
        # Ensure password is not included
        if '_password_hash' in user_dict:
            del user_dict['_password_hash']
        return user_dict
