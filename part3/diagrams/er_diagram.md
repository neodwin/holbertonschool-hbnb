# Entity-Relationship Diagram for HBnB Database

Ce diagramme représente la structure de la base de données du projet HBnB, montrant les relations entre les différentes entités.

## Diagramme ER complet

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

## Explication des relations

1. **Users - Places** (One-to-Many):
   - Un utilisateur peut posséder plusieurs lieux
   - Chaque lieu appartient à un seul utilisateur

2. **Users - Reviews** (One-to-Many):
   - Un utilisateur peut écrire plusieurs avis
   - Chaque avis est écrit par un seul utilisateur

3. **Places - Reviews** (One-to-Many):
   - Un lieu peut avoir plusieurs avis
   - Chaque avis concerne un seul lieu

4. **Places - Amenities** (Many-to-Many):
   - Un lieu peut avoir plusieurs équipements
   - Un équipement peut être associé à plusieurs lieux
   - Cette relation est implémentée via la table d'association PLACE_AMENITY

## Légende

- PK: Primary Key (Clé primaire)
- FK: Foreign Key (Clé étrangère)
- UK: Unique Key (Clé unique)

## Diagrammes détaillés par entité

### User et ses relations

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

### Place et ses relations

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

### Review et ses relations

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

### Amenity et ses relations

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