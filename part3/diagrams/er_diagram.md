# Entity-Relationship Diagram for HBnB Database

This diagram represents the database structure of the HBnB project, showing the relationships between the different entities.

## Complete ER Diagram

```mermaid
erDiagram
    USERS {
        string id PK
        string first_name
        string last_name
        string email UK
        string _password_hash
        boolean is_admin
        datetime created_at
        datetime updated_at
    }
    
    PLACES {
        string id PK
        string title
        text description
        float price
        float latitude
        float longitude
        string owner_id FK
        datetime created_at
        datetime updated_at
    }
    
    REVIEWS {
        string id PK
        text text
        int rating
        string place_id FK
        string user_id FK
        datetime created_at
        datetime updated_at
    }
    
    AMENITIES {
        string id PK
        string name UK
        datetime created_at
        datetime updated_at
    }
    
    PLACE_AMENITY {
        string place_id PK,FK
        string amenity_id PK,FK
    }
    
    USERS ||--o{ PLACES : "owns"
    USERS ||--o{ REVIEWS : "writes"
    PLACES ||--o{ REVIEWS : "has"
    PLACES }|--|{ AMENITIES : "has"
    PLACE_AMENITY }|--|| PLACES : "belongs to"
    PLACE_AMENITY }|--|| AMENITIES : "belongs to"
```

## Explanation of Relationships

1. **Users - Places** (One-to-Many):
   - A user can own multiple places
   - Each place belongs to a single user

2. **Users - Reviews** (One-to-Many):
   - A user can write multiple reviews
   - Each review is written by a single user

3. **Places - Reviews** (One-to-Many):
   - A place can have multiple reviews
   - Each review concerns a single place

4. **Places - Amenities** (Many-to-Many):
   - A place can have multiple amenities
   - An amenity can be associated with multiple places
   - This relationship is implemented through the PLACE_AMENITY association table

## Legend

- PK: Primary Key
- FK: Foreign Key
- UK: Unique Key

## Detailed Diagrams by Entity

### User and its relationships

```mermaid
erDiagram
    USERS {
        string id PK
        string first_name
        string last_name
        string email UK
        string _password_hash
        boolean is_admin
        datetime created_at
        datetime updated_at
    }
    
    PLACES {
        string id PK
        string owner_id FK
    }
    
    REVIEWS {
        string id PK
        string user_id FK
    }
    
    USERS ||--o{ PLACES : "owns"
    USERS ||--o{ REVIEWS : "writes"
```

### Place and its relationships

```mermaid
erDiagram
    PLACES {
        string id PK
        string title
        text description
        float price
        float latitude
        float longitude
        string owner_id FK
        datetime created_at
        datetime updated_at
    }
    
    USERS {
        string id PK
    }
    
    REVIEWS {
        string id PK
        string place_id FK
    }
    
    PLACE_AMENITY {
        string place_id PK,FK
        string amenity_id PK,FK
    }
    
    AMENITIES {
        string id PK
    }
    
    USERS ||--o{ PLACES : "owns"
    PLACES ||--o{ REVIEWS : "has"
    PLACES }|--|{ AMENITIES : "has"
    PLACE_AMENITY }|--|| PLACES : "belongs to"
```

### Review and its relationships

```mermaid
erDiagram
    REVIEWS {
        string id PK
        text text
        int rating
        string place_id FK
        string user_id FK
        datetime created_at
        datetime updated_at
    }
    
    USERS {
        string id PK
    }
    
    PLACES {
        string id PK
    }
    
    USERS ||--o{ REVIEWS : "writes"
    PLACES ||--o{ REVIEWS : "has"
```

### Amenity and its relationships

```mermaid
erDiagram
    AMENITIES {
        string id PK
        string name UK
        datetime created_at
        datetime updated_at
    }
    
    PLACE_AMENITY {
        string place_id PK,FK
        string amenity_id PK,FK
    }
    
    PLACES {
        string id PK
    }
    
    PLACES }|--|{ AMENITIES : "has"
    PLACE_AMENITY }|--|| AMENITIES : "belongs to"
``` 