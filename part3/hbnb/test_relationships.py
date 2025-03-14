from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
import json

def test_relationships():
    """Test relationships between entities"""
    app = create_app('testing')
    
    with app.app_context():
        # Initialize the database
        db.create_all()
        
        print("\n--- Creating test data ---")
        
        # Create users
        owner = User(
            first_name='Owner',
            last_name='User',
            email='owner@example.com',
            password='ownerpassword'
        )
        
        reviewer1 = User(
            first_name='Reviewer1',
            last_name='User',
            email='reviewer1@example.com',
            password='reviewer1password'
        )
        
        reviewer2 = User(
            first_name='Reviewer2',
            last_name='User',
            email='reviewer2@example.com',
            password='reviewer2password'
        )
        
        db.session.add_all([owner, reviewer1, reviewer2])
        db.session.commit()
        
        # Create amenities
        wifi = Amenity(name='WiFi')
        pool = Amenity(name='Pool')
        parking = Amenity(name='Parking')
        
        db.session.add_all([wifi, pool, parking])
        db.session.commit()
        
        # Create places
        place1 = Place(
            title='Beach House',
            description='Beautiful house near the beach',
            price=150.0,
            latitude=34.0522,
            longitude=-118.2437,
            owner=owner
        )
        
        place2 = Place(
            title='Mountain Cabin',
            description='Cozy cabin in the mountains',
            price=120.0,
            latitude=39.5501,
            longitude=-105.7821,
            owner=owner
        )
        
        db.session.add_all([place1, place2])
        db.session.commit()
        
        # Add amenities to places
        place1.add_amenity(wifi)
        place1.add_amenity(pool)
        place2.add_amenity(wifi)
        place2.add_amenity(parking)
        db.session.commit()
        
        # Create reviews
        review1 = Review(
            text='Great place with amazing views!',
            rating=5,
            place=place1,
            user=reviewer1
        )
        
        review2 = Review(
            text='Nice place but a bit expensive',
            rating=4,
            place=place1,
            user=reviewer2
        )
        
        review3 = Review(
            text='Cozy and comfortable',
            rating=5,
            place=place2,
            user=reviewer1
        )
        
        db.session.add_all([review1, review2, review3])
        db.session.commit()
        
        print("Test data created successfully!")
        
        # Test User-Place relationship (one-to-many)
        print("\n--- Testing User-Place relationship ---")
        user_places = owner.places.all()
        print(f"Owner has {len(user_places)} places:")
        for place in user_places:
            print(f"- {place.title}")
        
        # Test Place-Review relationship (one-to-many)
        print("\n--- Testing Place-Review relationship ---")
        place1_reviews = place1.reviews.all()
        print(f"Place '{place1.title}' has {len(place1_reviews)} reviews:")
        for review in place1_reviews:
            print(f"- {review.rating}/5 stars: {review.text}")
        
        # Test User-Review relationship (one-to-many)
        print("\n--- Testing User-Review relationship ---")
        user_reviews = reviewer1.reviews.all()
        print(f"User '{reviewer1.first_name}' has written {len(user_reviews)} reviews:")
        for review in user_reviews:
            print(f"- {review.rating}/5 stars for '{review.place_rel.title}': {review.text}")
        
        # Test Place-Amenity relationship (many-to-many)
        print("\n--- Testing Place-Amenity relationship ---")
        place1_amenities = place1.amenities.all()
        print(f"Place '{place1.title}' has {len(place1_amenities)} amenities:")
        for amenity in place1_amenities:
            print(f"- {amenity.name}")
        
        # Test Amenity-Place relationship (many-to-many)
        print("\n--- Testing Amenity-Place relationship ---")
        wifi_places = wifi.places.all()
        print(f"Amenity '{wifi.name}' is available in {len(wifi_places)} places:")
        for place in wifi_places:
            print(f"- {place.title}")
        
        # Test cascading delete (when a place is deleted, its reviews should be deleted too)
        print("\n--- Testing cascading delete ---")
        print(f"Before deletion: {len(Review.query.all())} reviews in total")
        db.session.delete(place1)
        db.session.commit()
        print(f"After deletion of '{place1.title}': {len(Review.query.all())} reviews in total")
        
        # Clean up
        db.drop_all()
        print("\nAll relationship tests completed successfully!")

if __name__ == '__main__':
    test_relationships() 