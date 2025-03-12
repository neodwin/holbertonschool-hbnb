from app.persistence.repository import InMemoryRepository
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from flask_jwt_extended import create_access_token
from datetime import datetime
from app.extensions import db

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    def authenticate_user(self, email, password):
        """Authenticate a user and return a JWT token"""
        user = self.get_user_by_email(email)
        if not user or not user.check_password(password):
            return None
        
        # Create access token with claims
        additional_claims = {
            'is_admin': user.is_admin
        }
        access_token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims
        )
        return access_token

    # User-related methods
    def create_user(self, user_data):
        """Create a new user"""
        try:
            return self.user_repo.create_user(user_data)
        except ValueError as e:
            raise e

    def get_user(self, user_id):
        """Get a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get a user by email"""
        return self.user_repo.get_by_email(email)

    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information"""
        try:
            return self.user_repo.update_user(user_id, user_data)
        except ValueError as e:
            raise e

    # Place-related methods
    def create_place(self, place_data):
        """Create a new place"""
        try:
            # Get the owner
            owner_id = place_data.get('owner_id')
            owner = self.get_user(owner_id)
            if not owner:
                raise ValueError('Owner not found')
            
            # Handle amenities if provided
            amenities = []
            if 'amenity_ids' in place_data:
                amenity_ids = place_data.pop('amenity_ids')
                for amenity_id in amenity_ids:
                    amenity = self.get_amenity(amenity_id)
                    if not amenity:
                        raise ValueError(f'Amenity with ID {amenity_id} not found')
                    amenities.append(amenity)
            
            # Create the place
            place_data['owner'] = owner
            place = self.place_repo.create_place(place_data)
            
            # Add amenities to the place
            for amenity in amenities:
                place.add_amenity(amenity)
            
            db.session.commit()
            return place
        except ValueError as e:
            raise e

    def get_place(self, place_id):
        """Get a place by ID"""
        return self.place_repo.get(place_id)

    def get_places_by_owner(self, owner_id):
        """Get all places owned by a specific user"""
        return self.place_repo.get_by_owner(owner_id)

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place's information"""
        try:
            # Handle amenities if provided
            if 'amenity_ids' in place_data:
                amenity_ids = place_data.pop('amenity_ids')
                amenities = []
                for amenity_id in amenity_ids:
                    amenity = self.get_amenity(amenity_id)
                    if not amenity:
                        raise ValueError(f'Amenity with ID {amenity_id} not found')
                    amenities.append(amenity)
                place_data['amenities'] = amenities
            
            return self.place_repo.update_place(place_id, place_data)
        except ValueError as e:
            raise e
    
    def add_amenity_to_place(self, place_id, amenity_id):
        """Add an amenity to a place"""
        place = self.get_place(place_id)
        if not place:
            raise ValueError('Place not found')
            
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError('Amenity not found')
            
        return self.place_repo.add_amenity_to_place(place_id, amenity)
    
    def remove_amenity_from_place(self, place_id, amenity_id):
        """Remove an amenity from a place"""
        place = self.get_place(place_id)
        if not place:
            raise ValueError('Place not found')
            
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError('Amenity not found')
            
        return self.place_repo.remove_amenity_from_place(place_id, amenity)

    # Review-related methods
    def create_review(self, review_data):
        """Create a new review"""
        try:
            # Get the place
            place_id = review_data.get('place_id')
            place = self.get_place(place_id)
            if not place:
                raise ValueError('Place not found')
                
            # Get the user
            user_id = review_data.get('user_id')
            user = self.get_user(user_id)
            if not user:
                raise ValueError('User not found')
                
            # Check if user is the owner of the place
            if place.owner_id == user_id:
                raise ValueError('Owner cannot review their own place')
                
            # Check if user already reviewed this place
            existing_review = self.review_repo.get_by_place_and_user(place_id, user_id)
            if existing_review:
                raise ValueError('User already reviewed this place')
                
            review_data['place'] = place
            review_data['user'] = user
            
            return self.review_repo.create_review(review_data)
        except ValueError as e:
            raise e

    def get_review(self, review_id):
        """Get a review by ID"""
        return self.review_repo.get(review_id)

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        return self.review_repo.get_by_place(place_id)

    def get_reviews_by_user(self, user_id):
        """Get all reviews by a specific user"""
        return self.review_repo.get_by_user(user_id)

    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        """Update a review's information"""
        try:
            return self.review_repo.update_review(review_id, review_data)
        except ValueError as e:
            raise e

    # Amenity-related methods
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        try:
            return self.amenity_repo.create_amenity(amenity_data)
        except ValueError as e:
            raise e

    def get_amenity(self, amenity_id):
        """Get an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, name):
        """Get an amenity by name"""
        return self.amenity_repo.get_by_name(name)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity's information"""
        try:
            return self.amenity_repo.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            raise e
    
    def get_places_by_amenity(self, amenity_id):
        """Get all places that have a specific amenity"""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError('Amenity not found')
        
        return amenity.places.all() 