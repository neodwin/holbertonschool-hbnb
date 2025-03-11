from app.persistence.repository import SQLAlchemyRepository
from app.models.place import Place
from app.extensions import db

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)
    
    def get_by_owner(self, owner_id):
        """Get all places owned by a specific user"""
        return Place.query.filter_by(owner_id=owner_id).all()
    
    def create_place(self, place_data):
        """Create a new place with validation"""
        # Create and add the place
        place = Place(**place_data)
        self.add(place)
        return place
    
    def update_place(self, place_id, place_data):
        """Update a place with validation"""
        place = self.get(place_id)
        if not place:
            return None
        
        # Handle amenities update if provided
        if 'amenities' in place_data:
            amenities = place_data.pop('amenities')
            # Clear current amenities and add new ones
            place.amenities = amenities
        
        # Update the place
        place.update(place_data)
        return place
    
    def add_amenity_to_place(self, place_id, amenity):
        """Add an amenity to a place"""
        place = self.get(place_id)
        if not place:
            return None
        
        place.add_amenity(amenity)
        db.session.commit()
        return place
    
    def remove_amenity_from_place(self, place_id, amenity):
        """Remove an amenity from a place"""
        place = self.get(place_id)
        if not place:
            return None
        
        place.remove_amenity(amenity)
        db.session.commit()
        return place 