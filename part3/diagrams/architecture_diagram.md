# Diagramme d'Architecture pour HBnB

Ce diagramme représente l'architecture globale de l'application HBnB, montrant les différentes couches et leurs interactions.

## Architecture en couches

```mermaid
flowchart TD
    subgraph "Couche Présentation"
        API[API REST]
        JWT[JWT Authentication]
    end
    
    subgraph "Couche Métier"
        Facade[HBnBFacade]
        Validation[Validation des données]
    end
    
    subgraph "Couche Persistance"
        Repositories[Repositories]
        ORM[SQLAlchemy ORM]
    end
    
    subgraph "Couche Données"
        DB[(Base de données)]
    end
    
    API --> JWT
    JWT --> Facade
    Facade --> Validation
    Facade --> Repositories
    Repositories --> ORM
    ORM --> DB
```

## Architecture détaillée

```mermaid
flowchart TD
    subgraph "Couche Présentation"
        UsersAPI[Users API]
        PlacesAPI[Places API]
        ReviewsAPI[Reviews API]
        AmenitiesAPI[Amenities API]
        AuthAPI[Auth API]
        JWT[JWT Authentication]
    end
    
    subgraph "Couche Métier"
        Facade[HBnBFacade]
    end
    
    subgraph "Couche Persistance"
        UserRepo[UserRepository]
        PlaceRepo[PlaceRepository]
        ReviewRepo[ReviewRepository]
        AmenityRepo[AmenityRepository]
    end
    
    subgraph "Couche Données"
        DB[(SQLite/MySQL)]
    end
    
    UsersAPI --> JWT
    PlacesAPI --> JWT
    ReviewsAPI --> JWT
    AmenitiesAPI --> JWT
    AuthAPI --> Facade
    
    JWT --> Facade
    
    Facade --> UserRepo
    Facade --> PlaceRepo
    Facade --> ReviewRepo
    Facade --> AmenityRepo
    
    UserRepo --> DB
    PlaceRepo --> DB
    ReviewRepo --> DB
    AmenityRepo --> DB
```

## Flux d'authentification

```mermaid
sequenceDiagram
    participant Client
    participant API as API REST
    participant Facade as HBnBFacade
    participant Repository as UserRepository
    participant DB as Base de données
    
    Client->>API: POST /api/v1/auth/login
    API->>Facade: authenticate_user(email, password)
    Facade->>Repository: get_user_by_email(email)
    Repository->>DB: SELECT * FROM users WHERE email = ?
    DB-->>Repository: User data
    Repository-->>Facade: User object
    Facade->>Facade: check_password(password)
    Facade-->>API: JWT token
    API-->>Client: JWT token
    
    Client->>API: GET /api/v1/users/ (with JWT)
    API->>API: verify_jwt()
    API->>Facade: get_all_users()
    Facade->>Repository: get_all()
    Repository->>DB: SELECT * FROM users
    DB-->>Repository: Users data
    Repository-->>Facade: User objects
    Facade-->>API: User objects
    API-->>Client: User data (JSON)
```

## Flux de création d'un lieu

```mermaid
sequenceDiagram
    participant Client
    participant API as API REST
    participant Facade as HBnBFacade
    participant PlaceRepo as PlaceRepository
    participant UserRepo as UserRepository
    participant DB as Base de données
    
    Client->>API: POST /api/v1/places/ (with JWT)
    API->>API: verify_jwt()
    API->>Facade: create_place(place_data)
    Facade->>UserRepo: get(owner_id)
    UserRepo->>DB: SELECT * FROM users WHERE id = ?
    DB-->>UserRepo: User data
    UserRepo-->>Facade: User object
    Facade->>PlaceRepo: create_place(place_data)
    PlaceRepo->>DB: INSERT INTO places VALUES (...)
    DB-->>PlaceRepo: Success
    PlaceRepo-->>Facade: Place object
    Facade-->>API: Place object
    API-->>Client: Place data (JSON)
``` 