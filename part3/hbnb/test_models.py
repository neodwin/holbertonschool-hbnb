from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.db_init import init_db
import json

def test_models():
    """Test CRUD operations for all models"""
    app = create_app('testing')
    
    with app.app_context():
        # Initialize the database
        db.create_all()
        
        # Create a test user
        test_user = User(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='testpassword'
        )
        db.session.add(test_user)
        db.session.commit()
        
        # Create a test amenity
        test_amenity = Amenity(name='Test Amenity')
        db.session.add(test_amenity)
        db.session.commit()
        
        # Create a test place
        test_place = Place(
            title='Test Place',
            description='A test place description',
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=test_user
        )
        db.session.add(test_place)
        db.session.commit()
        
        # Create a second user for reviews
        reviewer = User(
            first_name='Reviewer',
            last_name='User',
            email='reviewer@example.com',
            password='reviewerpassword'
        )
        db.session.add(reviewer)
        db.session.commit()
        
        # Create a test review
        test_review = Review(
            text='This is a test review',
            rating=5,
            place=test_place,
            user=reviewer
        )
        db.session.add(test_review)
        db.session.commit()
        
        # Test retrieving data
        print("\n--- Testing Place Retrieval ---")
        place = Place.query.filter_by(title='Test Place').first()
        assert place is not None
        print(f"Place: {place.title}, Price: {place.price}, Owner ID: {place.owner_id}")
        
        print("\n--- Testing Amenity Retrieval ---")
        amenity = Amenity.query.filter_by(name='Test Amenity').first()
        assert amenity is not None
        print(f"Amenity: {amenity.name}")
        
        print("\n--- Testing Review Retrieval ---")
        review = Review.query.filter_by(place_id=place.id).first()
        assert review is not None
        print(f"Review: {review.text}, Rating: {review.rating}, User ID: {review.user_id}")
        
        # Test updating data
        print("\n--- Testing Updates ---")
        place.price = 150.0
        amenity.name = 'Updated Amenity'
        review.rating = 4
        db.session.commit()
        
        # Verify updates
        updated_place = Place.query.get(place.id)
        assert updated_place.price == 150.0
        print(f"Updated Place Price: {updated_place.price}")
        
        updated_amenity = Amenity.query.get(amenity.id)
        assert updated_amenity.name == 'Updated Amenity'
        print(f"Updated Amenity Name: {updated_amenity.name}")
        
        updated_review = Review.query.get(review.id)
        assert updated_review.rating == 4
        print(f"Updated Review Rating: {updated_review.rating}")
        
        # Test deleting data
        print("\n--- Testing Deletion ---")
        db.session.delete(review)
        db.session.delete(place)
        db.session.delete(amenity)
        db.session.delete(reviewer)
        db.session.delete(test_user)
        db.session.commit()
        
        # Verify deletion
        assert Place.query.get(place.id) is None
        assert Amenity.query.get(amenity.id) is None
        assert Review.query.get(review.id) is None
        
        print("All model tests passed!")
        
        # Clean up
        db.drop_all()

if __name__ == '__main__':
    test_models() 