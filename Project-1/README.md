# HBnB (Holberton BnB)

## Description
HBnB is a comprehensive property rental platform inspired by AirBnB. This web application facilitates property listings, bookings, and reviews, providing a seamless experience for both hosts and guests.

## Architecture
The application follows a three-layer architecture:
- **Presentation Layer**: Handles user interface and API endpoints
- **Business Logic Layer**: Manages core business rules and data processing
- **Persistence Layer**: Handles data storage and retrieval

### Key Features
- User authentication and authorization
- Property listing management
- Booking system
- Review and rating system
- Search and filtering capabilities
- Amenity management

## Technical Stack

### Backend
- Python 3.8+
- Flask/Django (Web Framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)

### Frontend
- HTML5/CSS3
- JavaScript (ES6+)
- React.js
- Bootstrap 5

### DevOps & Tools
- Git (Version Control)
- Docker (Containerization)
- Nginx (Web Server)
- Gunicorn (WSGI Server)

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- PostgreSQL
- Node.js and npm
- Docker (optional)

### Local Setup
1. Clone the repository
```bash
git clone https://github.com/yourusername/hbnb.git
cd hbnb
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
npm install  # For frontend dependencies
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

6. Run the development server
```bash
python manage.py runserver
```

### Docker Setup
```bash
docker-compose up --build
```

## API Documentation

### Authentication
- POST `/api/users/register`: Register new user
- POST `/api/users/login`: User login
- POST `/api/users/logout`: User logout

### Places
- GET `/api/places`: List all places
- POST `/api/places`: Create new place
- GET `/api/places/{id}`: Get place details
- PUT `/api/places/{id}`: Update place
- DELETE `/api/places/{id}`: Delete place

### Reviews
- GET `/api/places/{id}/reviews`: Get place reviews
- POST `/api/places/{id}/reviews`: Create review
- PUT `/api/reviews/{id}`: Update review
- DELETE `/api/reviews/{id}`: Delete review

### Amenities
- GET `/api/amenities`: List all amenities
- POST `/api/amenities`: Create amenity
- PUT `/api/amenities/{id}`: Update amenity
- DELETE `/api/amenities/{id}`: Delete amenity

## Testing
```bash
# Run unit tests
python -m pytest tests/unit

# Run integration tests
python -m pytest tests/integration

# Run with coverage
coverage run -m pytest
coverage report
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Code Style
- Follow PEP 8 for Python code
- Use ESLint for JavaScript code
- Write descriptive commit messages
- Include docstrings and comments

## Project Structure
```
hbnb/
├── api/                 # API endpoints
├── models/             # Data models
├── services/           # Business logic
├── static/             # Static files
├── templates/          # HTML templates
├── tests/              # Test files
├── config.py           # Configuration
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors
- Your Name - Initial work - [YourGithub](https://github.com/yourusername)

## Acknowledgments
- Holberton School for the project requirements and guidance
- AirBnB for inspiration
- All contributors who have helped shape this project