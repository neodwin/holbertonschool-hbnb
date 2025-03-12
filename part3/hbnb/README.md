# HBnB API Project

This is the HBnB API project, a RESTful API service for managing property rentals.

## Project Structure

```
hbnb/
├── app/
│   ├── __init__.py          # Flask application instance
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── v1/             # API version 1
│   │       ├── __init__.py
│   │       ├── users.py    # User endpoints
│   │       ├── places.py   # Place endpoints
│   │       ├── reviews.py  # Review endpoints
│   │       ├── amenities.py # Amenity endpoints
│   ├── models/             # Business logic classes
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
├── run.py                  # Application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Project dependencies
├── README.md             # Project documentation
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

3. Run the application:
   ```bash
   python run.py
   ```

The application will start in development mode with debug enabled.

## Project Components

- **API Layer**: RESTful endpoints for users, places, reviews, and amenities
- **Business Logic**: Core domain models and business rules
- **Service Layer**: Facade pattern for coordinating between layers
- **Persistence**: In-memory repository (to be replaced with database in Part 3)
