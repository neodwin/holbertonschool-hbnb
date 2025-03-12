from app.models.base import BaseModel
from app.extensions import db

# Association table for the many-to-many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    reviews = db.relationship('Review', backref='place_rel', lazy='dynamic', cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='dynamic',
                               backref=db.backref('places', lazy='dynamic'))
    
    def __init__(self, title, description, price, latitude, longitude, owner, **kwargs):
        self.validate_title(title)
        self.validate_price(price)
        self.validate_coordinates(latitude, longitude)
        
        super().__init__(
            title=title,
            description=description or "",
            price=float(price),
            latitude=float(latitude),
            longitude=float(longitude),
            owner_id=owner.id,
            **kwargs
        )
        
        # These will be handled by relationships in a later task
        self._owner = owner  # Temporary reference, not stored in DB
        self._reviews = []   # Temporary list, not stored in DB
        self._amenities = [] # Temporary list, not stored in DB
        
        # Add this place to the owner's places (will be handled by relationships later)
        if hasattr(owner, 'add_place'):
            owner.add_place(self)

    @staticmethod
    def validate_title(title):
        """Validate title field"""
        if not title or not isinstance(title, str):
            raise ValueError("Title is required and must be a string")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")

    @staticmethod
    def validate_price(price):
        """Validate price field"""
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError("Price must be a positive number")

    @staticmethod
    def validate_coordinates(latitude, longitude):
        """Validate geographic coordinates"""
        try:
            lat = float(latitude)
            lon = float(longitude)
            if not (-90.0 <= lat <= 90.0) or not (-180.0 <= lon <= 180.0):
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError("Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180")

    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Remove an amenity from the place"""
        if amenity in self.amenities:
            self.amenities.remove(amenity)

    def update(self, data):
        """Update place attributes with validation"""
        if 'title' in data:
            self.validate_title(data['title'])
        if 'price' in data:
            self.validate_price(data['price'])
        if 'latitude' in data or 'longitude' in data:
            lat = data.get('latitude', self.latitude)
            lon = data.get('longitude', self.longitude)
            self.validate_coordinates(lat, lon)
        
        super().update(data)

    def to_dict(self):
        """Convert the object to a dictionary representation"""
        result = super().to_dict()
        # Add related data
        result['owner'] = self.owner_rel.to_dict() if hasattr(self, 'owner_rel') else None
        result['reviews'] = [review.to_dict() for review in self.reviews.all()] if hasattr(self, 'reviews') else []
        result['amenities'] = [amenity.to_dict() for amenity in self.amenities.all()] if hasattr(self, 'amenities') else []
        return result
