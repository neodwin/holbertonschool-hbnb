from app.persistence.repository import SQLAlchemyRepository
from app.models.amenity import Amenity

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)
    
    def get_by_name(self, name):
        """Get an amenity by name"""
        return Amenity.query.filter_by(name=name).first()
    
    def create_amenity(self, amenity_data):
        """Create a new amenity with validation"""
        # Check if amenity with same name already exists
        if 'name' in amenity_data and self.get_by_name(amenity_data['name']):
            raise ValueError('Amenity with this name already exists')
            
        # Create and add the amenity
        amenity = Amenity(**amenity_data)
        self.add(amenity)
        return amenity
    
    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity with validation"""
        amenity = self.get(amenity_id)
        if not amenity:
            return None
            
        # Check name uniqueness if name is being updated
        if 'name' in amenity_data and amenity_data['name'] != amenity.name:
            existing_amenity = self.get_by_name(amenity_data['name'])
            if existing_amenity:
                raise ValueError('Amenity with this name already exists')
                
        # Update the amenity
        amenity.update(amenity_data)
        return amenity 