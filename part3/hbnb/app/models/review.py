from app.models.base import BaseModel
from app.extensions import db

class Review(BaseModel):
    __tablename__ = 'reviews'
    
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships will be added in a later task
    
    def __init__(self, text, rating, place, user, **kwargs):
        self.validate_text(text)
        self.validate_rating(rating)
        
        super().__init__(
            text=text,
            rating=int(rating),
            place_id=place.id,
            user_id=user.id,
            **kwargs
        )
        
        # These will be handled by relationships in a later task
        self._place = place  # Temporary reference, not stored in DB
        self._user = user    # Temporary reference, not stored in DB
        
        # Add this review to the place's reviews (will be handled by relationships later)
        if hasattr(place, 'add_review'):
            place.add_review(self)

    @staticmethod
    def validate_text(text):
        """Validate review text"""
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string")

    @staticmethod
    def validate_rating(rating):
        """Validate rating value"""
        try:
            rating = int(rating)
            if not (1 <= rating <= 5):
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError("Rating must be an integer between 1 and 5")

    def update(self, data):
        """Update review attributes with validation"""
        if 'text' in data:
            self.validate_text(data['text'])
        if 'rating' in data:
            self.validate_rating(data['rating'])
        
        super().update(data)

    def to_dict(self):
        """Convert the object to a dictionary representation"""
        result = super().to_dict()
        # Add related data (minimal to avoid circular references)
        result['user'] = {
            'id': self.user_rel.id,
            'first_name': self.user_rel.first_name,
            'last_name': self.user_rel.last_name
        } if hasattr(self, 'user_rel') else None
        
        result['place'] = {
            'id': self.place_rel.id,
            'title': self.place_rel.title
        } if hasattr(self, 'place_rel') else None
        
        return result
