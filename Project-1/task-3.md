# HBnB Technical Documentation

## Introduction

This technical document serves as a comprehensive blueprint for the HBnB (Holberton BnB) project, a web application designed to facilitate property rentals and bookings. This document outlines the system's architecture, component interactions, and implementation guidelines through detailed diagrams and explanations.

### Purpose and Scope
- Provide a clear architectural overview of the HBnB system
- Document the system's components and their interactions
- Guide the implementation process
- Serve as a reference for developers and stakeholders

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

    %% Relationships to influence layout
    BusinessFacade --> BusinessLogicLayer
    BusinessLogicLayer --> PersistenceLayer

    %% Layer composition
    PresentationLayer *-- API
    PresentationLayer *-- WebServices
    BusinessLogicLayer *-- Models
    BusinessLogicLayer *-- DomainLogic
    PersistenceLayer *-- Repository
    PersistenceLayer *-- Database

    %% Facade relationships
    API --> BusinessFacade
    WebServices --> BusinessFacade
    BusinessFacade --> Models
    BusinessFacade --> DomainLogic
    DomainLogic --> Repository
    Repository --> Database

    %% Additional relationships
    Models --> DomainLogic
```

### Architecture Overview
The system follows a three-layer architecture pattern with a Facade interface:

1. **Presentation Layer**
   - Handles user interactions and API endpoints
   - Manages request/response formatting
   - Contains RESTful API and web services

2. **Business Logic Layer**
   - Implements core business logic through the Facade pattern
   - Manages domain models and business rules
   - Handles data validation and processing

3. **Persistence Layer**
   - Manages data storage and retrieval
   - Handles database operations and transactions
   - Provides data mapping services

## 2. Business Logic Layer Details

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
        -salt: Bytes
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
        +is_available: Boolean
        -reviews: List~Review~
        +average_rating: Float
        +update_listing(data: dict) void
        +get_reviews() List~Review~
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

    User "1" --> "0..*" Place : owns
    User "1" --> "0..*" Review : writes
    Place "1" --> "0..*" Review : has
    Place "1" *--> "0..*" Amenity : includes

    class UserRole {
        <<enumeration>>
        GUEST
        HOST
        ADMIN
    }
```

### Key Components
1. **BaseModel**
   - Abstract base class providing common functionality
   - Handles creation and update timestamps
   - Implements basic CRUD operations

2. **Domain Models**
   - User: Manages user accounts and authentication
   - Place: Handles property listings and amenities
   - Review: Manages property reviews and ratings
   - Amenity: Represents property features and services

## 3. API Interaction Flows

### Sequence Diagrams
```mermaid
sequenceDiagram
    %% User Registration Flow
    participant Client
    participant API
    participant UserService
    participant UserModel
    participant Database

    Note over Client,Database: User Registration Flow
    Client->>API: POST /api/users/register
    API->>UserService: validateUserData(userData)
    UserService->>UserModel: createUser(validatedData)
    UserModel->>Database: save()
    Database-->>UserModel: confirmSave
    UserModel-->>UserService: newUser
    UserService-->>API: userCreated
    API-->>Client: 201 Created

    %% Place Creation Flow
    Note over Client,Database: Place Creation Flow
    Client->>API: POST /api/places
    API->>UserService: validateUserAuth()
    UserService-->>API: userAuthorized
    API->>PlaceService: validatePlaceData(placeData)
    PlaceService->>PlaceModel: createPlace(validatedData)
    PlaceModel->>Database: save()
    Database-->>PlaceModel: confirmSave
    PlaceModel-->>PlaceService: newPlace
    PlaceService-->>API: placeCreated
    API-->>Client: 201 Created

    %% Review Submission Flow
    Note over Client,Database: Review Submission Flow
    Client->>API: POST /api/places/{id}/reviews
    API->>UserService: validateUserAuth()
    UserService-->>API: userAuthorized
    API->>ReviewService: validateReviewData(reviewData)
    ReviewService->>PlaceService: checkPlaceExists(placeId)
    PlaceService-->>ReviewService: placeExists
    ReviewService->>ReviewModel: createReview(validatedData)
    ReviewModel->>Database: save()
    Database-->>ReviewModel: confirmSave
    ReviewModel-->>ReviewService: newReview
    ReviewService-->>API: reviewCreated
    API-->>Client: 201 Created

    %% Fetching Places Flow
    Note over Client,Database: Fetching Places Flow
    Client->>API: GET /api/places?filters
    API->>PlaceService: validateFilters(filters)
    PlaceService->>PlaceModel: findPlaces(validFilters)
    PlaceModel->>Database: query(filters)
    Database-->>PlaceModel: placesList
    PlaceModel-->>PlaceService: processedPlaces
    PlaceService-->>API: formattedPlaces
    API-->>Client: 200 OK with Places
```

### API Flow Descriptions

1. **User Registration**
   - Validates user input data
   - Creates new user record
   - Returns confirmation with user details
   - Implements proper error handling

2. **Place Creation**
   - Authenticates user
   - Validates place data
   - Creates new place listing
   - Associates place with owner

3. **Review Submission**
   - Verifies user authentication
   - Validates review data
   - Checks place existence
   - Creates and associates review

4. **Fetching Places**
   - Processes filter parameters
   - Queries database with filters
   - Returns formatted place listings
   - Implements pagination

## Implementation Guidelines

1. **Security Considerations**
   - Implement proper authentication and authorization
   - Use secure password hashing
   - Validate all user inputs
   - Implement rate limiting

2. **Performance Optimization**
   - Use database indexing
   - Implement caching where appropriate
   - Optimize database queries
   - Use pagination for large datasets

3. **Error Handling**
   - Implement comprehensive error handling
   - Use appropriate HTTP status codes
   - Provide meaningful error messages
   - Log errors for debugging

4. **Code Organization**
   - Follow clean code principles
   - Implement proper separation of concerns
   - Use meaningful naming conventions
   - Write comprehensive documentation

## Conclusion

This technical documentation provides a comprehensive overview of the HBnB system architecture and implementation guidelines. It serves as a reference for developers and stakeholders throughout the development process. Regular updates and maintenance of this documentation will ensure its continued relevance and usefulness.

