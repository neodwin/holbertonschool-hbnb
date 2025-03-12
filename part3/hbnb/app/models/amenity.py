from app.models.base import BaseModel
from app.extensions import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    # Relationships will be added in a later task
    
    def __init__(self, name, **kwargs):
        self.validate_name(name)
        super().__init__(name=name, **kwargs)

    @staticmethod
    def validate_name(name):
        """Validate amenity name"""
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required and must be a string")
        if len(name) > 50:
            raise ValueError("Amenity name must not exceed 50 characters")

    def update(self, data):
        """Update amenity attributes with validation"""
        if 'name' in data:
            self.validate_name(data['name'])
        
        super().update(data)
        
    def to_dict(self):
        """Convert the object to a dictionary representation"""
        result = super().to_dict()
        # We don't include places to avoid circular references
        return result
