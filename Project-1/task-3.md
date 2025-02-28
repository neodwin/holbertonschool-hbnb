# HBnB Technical Documentation

## Introduction

### Purpose
This technical document serves as a comprehensive blueprint for the HBnB (Holberton BnB) project. It consolidates all architectural diagrams, design decisions, and implementation guidelines into a single, cohesive reference document that will guide the development process.

### Project Overview
HBnB is a web application inspired by AirBnB, designed to facilitate property rentals and bookings. The system implements a robust three-tier architecture, utilizing modern design patterns and best practices to ensure scalability, maintainability, and security.

## 1. High-Level Architecture

### Package Diagram
```mermaid
classDiagram
    %% Facade Pattern (declared first to influence layout)
    class BusinessFacade {
        <<Interface>>
        createEntity()
        readEntity()
        updateEntity()
        deleteEntity()
    }

    %% Layers as containers
    class PresentationLayer["Presentation Layer"] {
        <<Layer>>
    }
    class BusinessLogicLayer["Business Logic Layer"] {
        <<Layer>>
    }
    class PersistenceLayer["Persistence Layer"] {
        <<Layer>>
    }

    %% Components in Presentation Layer
    class API {
        RESTful Endpoints
        Request Handling
        Response Formatting
    }
    class WebServices {
        User Interface
        Client Communication
    }

    %% Components in Business Logic Layer
    class Models {
        User
        Place
        Review
        Amenity
        State
        City
    }
    class DomainLogic {
        Business Rules
        Validation
        Processing
    }

    %% Components in Persistence Layer
    class Repository {
        DatabaseOperations
        DataMapping
        QueryExecution
    }
    class Database {
        Storage
        Retrieval
        Transactions
    }

    %% Relationships
    BusinessFacade --> BusinessLogicLayer
    BusinessLogicLayer --> PersistenceLayer
    PresentationLayer -- API
    PresentationLayer -- WebServices
    BusinessLogicLayer -- Models
    BusinessLogicLayer -- DomainLogic
    PersistenceLayer -- Repository
    PersistenceLayer -- Database
    API --> BusinessFacade
    WebServices --> BusinessFacade
    BusinessFacade --> Models
    BusinessFacade --> DomainLogic
    DomainLogic --> Repository
    Repository --> Database
    Models --> DomainLogic
```

### Architectural Design Decisions

1. **Three-Tier Architecture**
   - **Presentation Layer**: Handles user interface and API endpoints
   - **Business Logic Layer**: Contains core business rules and data processing
   - **Persistence Layer**: Manages data storage and retrieval

2. **Facade Pattern Implementation**
   - Simplifies complex subsystem interactions
   - Provides a unified interface for the presentation layer
   - Reduces coupling between layers
   - Facilitates maintenance and future modifications

## 2. Business Logic Layer

### Class Diagram
```mermaid
classDiagram
    class BaseModel {
        <<abstract>>
        +id: UUID
        +created_at: DateTime
        +updated_at: DateTime
        +save() void
        +to_dict() dict
        +__str__() String
        +delete() void
        #validate() bool
    }

    class User {
        +email: String
        -password_hash: Bytes
        +first_name: String
        +last_name: String
        +address: String
        +phone: String
        +birth_date: Date
        +age: Integer
        +role: UserRole
        -owned_places: List~Place~
        -reviews: List~Review~
        +create_listing(place: Place) Place
        +add_review(place: Place, comment: String, rating: Integer) Review
        +update_profile(data: dict) void
        +get_listings() List~Place~
        +change_password(old_pwd: String, new_pwd: String) bool
        +verify_email() bool
        -hash_password(password: String, salt: Bytes) Bytes
        -verify_password(password: String) bool
    }

    class Place {
        +name: String
        +description: String
        +area: Float
        +address: String
        +latitude: Float
        +longitude: Float
        +max_guests: Integer
        +number_rooms: Integer
        +number_bathrooms: Integer
        +price_per_night: Float
        +owner: User
        +amenities: List~Amenity~
        -reviews: List~Review~
        +average_rating: Float
        +update_listing(data: dict) void
        +get_reviews() List~Review~
        +is_available() Boolean
        +calculate_rating() Float
        +add_amenity(amenity: Amenity) void
        +remove_amenity(amenity: Amenity) void
        -validate_coordinates() bool
    }

    class Review {
        +reviewer: User
        +place: Place
        +rating: Integer
        +comment: String
        +language: String
        +review_date: DateTime
        -is_verified: Boolean
        +update_review(comment: String, rating: Integer) void
        +delete_review() void
        +translate(target_language: String) String
        +get_reviewer_info() dict
        +mark_as_helpful() void
        +report_inappropriate() void
        -validate_rating() bool
    }

    class Amenity {
        +name: String
        +description: String
        +is_available: Boolean
        +category: String
        -additional_cost: Float
        -associated_places: List~Place~
        +update_availability(status: Boolean) void
        +get_places() List~Place~
        +set_additional_cost(cost: Float) void
        +get_total_cost(days: Integer) Float
    }

    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity
    User --> Place : owns
    User --> Review : writes
    Place --> Review : has
    Place --> Amenity : includes
```

### Domain Model Design Decisions

1. **BaseModel Abstraction**
   - Provides common functionality for all entities
   - Implements UUID-based identification
   - Manages creation and update timestamps
   - Ensures consistent data validation

2. **Entity Relationships**
   - User-Place: One-to-many ownership relationship
   - User-Review: One-to-many authorship relationship
   - Place-Review: One-to-many composition
   - Place-Amenity: Many-to-many association

## 3. API Interaction Flows

### Error Handling Strategy
The system implements a comprehensive error handling strategy with standardized HTTP status codes:

- **400 Bad Request**: Invalid input data or parameters
- **401 Unauthorized**: Authentication required
- **404 Not Found**: Resource not found
- **409 Conflict**: Resource conflict (e.g., duplicate email)
- **500 Server Error**: Internal server errors

### Sequence Diagrams

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Service
    participant Database

    Note over API: Error Codes:<br/>400: Bad Request<br/>401: Unauthorized<br/>404: Not Found<br/>409: Conflict<br/>500: Server Error

    %% User Registration Flow
    Note over Client,Database: User Registration
    Client->>API: POST /api/users/register
    API->>Service: validateAndCreateUser(userData)
    Service->>Database: save()
    
    %% Success Path
    Database-->>Service: confirm
    Service-->>API: userCreated
    API-->>Client: 201 Created
    
    %% Error Paths
    Note right of API: Possible Errors:<br/>- Invalid Data (400)<br/>- Email Exists (409)<br/>- Database Error (500)

    %% Place Creation Flow
    Note over Client,Database: Place Creation
    Client->>API: POST /api/places
    API->>Service: checkAuthAndCreatePlace(placeData)
    Service->>Database: save()
    
    %% Success Path
    Database-->>Service: confirm
    Service-->>API: placeCreated
    API-->>Client: 201 Created
    
    %% Error Paths
    Note right of API: Possible Errors:<br/>- Unauthorized (401)<br/>- Invalid Data (400)<br/>- Database Error (500)

    %% Review Submission Flow
    Note over Client,Database: Review Submission
    Client->>API: POST /api/places/{id}/reviews
    API->>Service: validateAndCreateReview(reviewData)
    Service->>Database: save()
    
    %% Success Path
    Database-->>Service: confirm
    Service-->>API: reviewCreated
    API-->>Client: 201 Created
    
    %% Error Paths
    Note right of API: Possible Errors:<br/>- Place Not Found (404)<br/>- Unauthorized (401)<br/>- Invalid Data (400)

    %% Fetching Places Flow
    Note over Client,Database: Fetching Places
    Client->>API: GET /api/places?filters
    API->>Service: findPlaces(filters)
    Service->>Database: query()
    
    %% Success Path
    Database-->>Service: placesList
    Service-->>API: formattedPlaces
    API-->>Client: 200 OK
    
    %% Error Paths
    Note right of API: Possible Errors:<br/>- Invalid Filters (400)<br/>- No Results (204)<br/>- Database Error (500)
```

#### Flow Descriptions

## Implementation Guidelines

### Error Handling Implementation
1. **Validation Layer**
   - Input validation at API level
   - Business rule validation in service layer
   - Data integrity checks in model layer

2. **Error Response Format**
   ```json
   {
     "status": "error",
     "code": 400,
     "message": "Invalid input",
     "details": {
       "field": "email",
       "error": "Invalid email format"
     }
   }
   ```

3. **Error Logging**
   - Log all errors with appropriate severity levels
   - Include stack traces for 500 errors
   - Monitor error patterns for system health

### Security Considerations
1. **Authentication**
   - Implement JWT-based authentication
   - Secure password hashing using bcrypt
   - Session management and token expiration

2. **Data Protection**
   - Input sanitization
   - CORS configuration
   - Rate limiting for API endpoints

### Performance Optimization
1. **Database**
   - Implement indexing for frequent queries
   - Use connection pooling
   - Optimize query patterns

2. **Caching**
   - Implement Redis for session storage
   - Cache frequently accessed data
   - Use ETags for API responses

### Code Organization
1. **Project Structure**
   ```
   hbnb/
   ├── api/                 # API endpoints
   ├── models/             # Data models
   ├── services/           # Business logic
   ├── static/             # Static files
   ├── templates/          # HTML templates
   ├── tests/              # Test files
   ├── config.py           # Configuration
   └── requirements.txt    # Dependencies
   ```

2. **Coding Standards**
   - Follow PEP 8 for Python code
   - Use ESLint for JavaScript
   - Write comprehensive documentation
   - Implement unit tests

## Conclusion
This technical documentation provides a comprehensive blueprint for implementing the HBnB project. The updated error handling strategy ensures robust and consistent error management across all system components, while maintaining the original architectural patterns and design decisions.