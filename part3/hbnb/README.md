# HBnB API Project

This is the HBnB API project, a RESTful API service for managing property rentals with authentication and database persistence.

## Project Structure

```
hbnb/
├── app/
│   ├── __init__.py          # Flask application instance
│   ├── extensions.py        # Flask extensions (SQLAlchemy, JWT, Bcrypt)
│   ├── db_init.py           # Database initialization functions
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── v1/             # API version 1
│   │       ├── __init__.py
│   │       ├── auth.py     # Authentication endpoints
│   │       ├── users.py    # User endpoints
│   │       ├── places.py   # Place endpoints
│   │       ├── reviews.py  # Review endpoints
│   │       ├── amenities.py # Amenity endpoints
│   ├── models/             # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/           # Service layer with Facade pattern
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/        # Data persistence layer
│       ├── __init__.py
│       ├── repository.py
│       ├── user_repository.py
│       ├── place_repository.py
│       ├── review_repository.py
│       ├── amenity_repository.py
├── config.py              # Configuration settings
├── run.py                 # Application entry point
├── init_admin.py          # Admin user initialization script
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
└── tests/                 # Test files
    ├── test_models.py
    ├── test_relationships.py
    ├── test_user_db.py
    ├── test_api.py
    └── ...
```

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   cd sql
   ./setup_database.sh
   cd ..
   ```

4. Create an admin user (optional):
   ```bash
   python init_admin.py
   ```

5. Run the application:
   ```bash
   python run.py
   ```

The application will start at http://localhost:5000 with the interactive API documentation available at http://localhost:5000/api/v1.

## Environment Variables

You can configure the application using these environment variables:

- `FLASK_ENV`: Set to "development" (default), "testing", or "production"
- `DATABASE_URL`: Database connection string (defaults to SQLite for development)
- `JWT_SECRET_KEY`: Secret key for JWT token generation (set a strong key in production)

## Project Components

- **API Layer**: RESTful endpoints with JWT authentication
- **Business Logic**: Core domain models with SQLAlchemy
- **Service Layer**: Facade pattern for coordinating between layers
- **Persistence**: Repository pattern with SQLite/MySQL database
- **Authentication**: JWT-based authentication and role-based authorization

## Testing

Run the tests with pytest:

```bash
pytest
```

Or run individual test files:

```bash
python test_user_db.py
python test_relationships.py
```
