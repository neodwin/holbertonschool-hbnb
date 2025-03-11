from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app import create_app
import os

def init_db(app=None):
    """Initialize the database"""
    if app is None:
        app = create_app('development')
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@hbnb.com').first()
        if not admin:
            # Create admin user
            admin = User(
                first_name='Admin',
                last_name='User',
                email='admin@hbnb.com',
                password='adminpassword',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully.")
        
        # Create some amenities if they don't exist
        amenities = [
            'WiFi', 'Kitchen', 'Washer', 'Dryer', 'Air Conditioning',
            'Heating', 'Dedicated Workspace', 'TV', 'Hair Dryer',
            'Iron', 'Pool', 'Hot Tub', 'Free Parking', 'EV Charger',
            'Crib', 'Gym', 'BBQ Grill', 'Breakfast', 'Indoor Fireplace',
            'Smoking Allowed', 'Beachfront', 'Waterfront', 'Ski-in/Ski-out'
        ]
        
        for amenity_name in amenities:
            if not Amenity.query.filter_by(name=amenity_name).first():
                amenity = Amenity(name=amenity_name)
                db.session.add(amenity)
        
        db.session.commit()
        print("Database initialized successfully.")

if __name__ == '__main__':
    init_db() 