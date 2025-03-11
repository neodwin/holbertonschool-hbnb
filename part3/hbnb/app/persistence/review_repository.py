from app.persistence.repository import SQLAlchemyRepository
from app.models.review import Review

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)
    
    def get_by_place(self, place_id):
        """Get all reviews for a specific place"""
        return Review.query.filter_by(place_id=place_id).all()
    
    def get_by_user(self, user_id):
        """Get all reviews by a specific user"""
        return Review.query.filter_by(user_id=user_id).all()
    
    def get_by_place_and_user(self, place_id, user_id):
        """Get a review by place and user (to check if user already reviewed a place)"""
        return Review.query.filter_by(place_id=place_id, user_id=user_id).first()
    
    def create_review(self, review_data):
        """Create a new review with validation"""
        # Create and add the review
        review = Review(**review_data)
        self.add(review)
        return review
    
    def update_review(self, review_id, review_data):
        """Update a review with validation"""
        review = self.get(review_id)
        if not review:
            return None
                
        # Update the review
        review.update(review_data)
        return review 