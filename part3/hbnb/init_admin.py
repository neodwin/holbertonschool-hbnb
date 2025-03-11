from app import create_app
from app.extensions import db
from app.models.user import User

def create_admin():
    """Create an admin user"""
    app = create_app('development')
    
    with app.app_context():
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@hbnb.com').first()
        if admin:
            print("Admin user already exists.")
            return
        
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
        print(f"Admin ID: {admin.id}")
        print(f"Admin email: {admin.email}")
        print(f"Admin password: adminpassword")

if __name__ == '__main__':
    create_admin() 