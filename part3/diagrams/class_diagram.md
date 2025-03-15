# Class Diagram for SQLAlchemy Models

This diagram represents the Python classes used in the HBnB project, showing how SQLAlchemy models are structured and related.

## Complete Class Diagram

```mermaid
classDiagram
    class BaseModel {
        +id: String
        +created_at: DateTime
        +updated_at: DateTime
        +__init__()
        +save()
        +update(data)
        +to_dict()
    }
    
    class User {
        +first_name: String
        +last_name: String
        +email: String
        +_password_hash: String
        +is_admin: Boolean
        +places: Relationship
        +reviews: Relationship
        +__init__(first_name, last_name, email, password, is_admin)
        +password: Property
        +set_password(password)
        +check_password(password)
        +validate_name(name, field)
        +validate_email(email)
        +add_place(place)
        +update(data)
        +to_dict()
    }
    
    class Place {
        +title: String
        +description: String
        +price: Float
        +latitude: Float
        +longitude: Float
        +owner_id: String
        +reviews: Relationship
        +amenities: Relationship
        +__init__(title, description, price, latitude, longitude, owner)
        +validate_title(title)
        +validate_price(price)
        +validate_coordinates(latitude, longitude)
        +add_review(review)
        +add_amenity(amenity)
        +remove_amenity(amenity)
        +update(data)
        +to_dict()
    }
    
    class Review {
        +text: String
        +rating: Integer
        +place_id: String
        +user_id: String
        +__init__(text, rating, place, user)
        +validate_text(text)
        +validate_rating(rating)
        +update(data)
        +to_dict()
    }
    
    class Amenity {
        +name: String
        +places: Relationship
        +__init__(name)
        +validate_name(name)
        +update(data)
        +to_dict()
    }
    
    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity
    
    User "1" --> "*" Place : owns
    User "1" --> "*" Review : writes
    Place "1" --> "*" Review : has
    Place "*" --> "*" Amenity : has
```

## Explanation of Relationships

1. **Inheritance**:
   - All model classes (User, Place, Review, Amenity) inherit from BaseModel
   - BaseModel provides common attributes and methods like id, created_at, updated_at, save(), update(), to_dict()

2. **Class Relationships**:
   - User - Place: A user can own multiple places (one-to-many)
   - User - Review: A user can write multiple reviews (one-to-many)
   - Place - Review: A place can have multiple reviews (one-to-many)
   - Place - Amenity: A place can have multiple amenities and an amenity can be associated with multiple places (many-to-many)

## Repository Diagram

```mermaid
classDiagram
    class Repository {
        <<abstract>>
        +add(obj)
        +get(obj_id)
        +get_all()
        +update(obj_id, data)
        +delete(obj_id)
        +get_by_attribute(attr_name, attr_value)
    }
    
    class InMemoryRepository {
        -_storage: Dict
        +add(obj)
        +get(obj_id)
        +get_all()
        +update(obj_id, data)
        +delete(obj_id)
        +get_by_attribute(attr_name, attr_value)
    }
    
    class SQLAlchemyRepository {
        -model_class: Class
        +add(obj)
        +get(obj_id)
        +get_all()
        +update(obj_id, data)
        +delete(obj_id)
        +get_by_attribute(attr_name, attr_value)
    }
    
    class UserRepository {
        +get_by_email(email)
        +create_user(user_data)
        +update_user(user_id, user_data)
    }
    
    class PlaceRepository {
        +get_by_owner(owner_id)
        +create_place(place_data)
        +update_place(place_id, place_data)
        +add_amenity_to_place(place_id, amenity)
        +remove_amenity_from_place(place_id, amenity)
    }
    
    class ReviewRepository {
        +get_by_place(place_id)
        +get_by_user(user_id)
        +get_by_place_and_user(place_id, user_id)
        +create_review(review_data)
        +update_review(review_id, review_data)
    }
    
    class AmenityRepository {
        +get_by_name(name)
        +create_amenity(amenity_data)
        +update_amenity(amenity_id, amenity_data)
    }
    
    Repository <|-- InMemoryRepository
    Repository <|-- SQLAlchemyRepository
    SQLAlchemyRepository <|-- UserRepository
    SQLAlchemyRepository <|-- PlaceRepository
    SQLAlchemyRepository <|-- ReviewRepository
    SQLAlchemyRepository <|-- AmenityRepository
```

## Facade Diagram

```mermaid
classDiagram
    class HBnBFacade {
        -user_repo: UserRepository
        -place_repo: PlaceRepository
        -review_repo: ReviewRepository
        -amenity_repo: AmenityRepository
        +authenticate_user(email, password)
        +create_user(user_data)
        +get_user(user_id)
        +get_user_by_email(email)
        +get_all_users()
        +update_user(user_id, user_data)
        +create_place(place_data)
        +get_place(place_id)
        +get_places_by_owner(owner_id)
        +get_all_places()
        +update_place(place_id, place_data)
        +add_amenity_to_place(place_id, amenity_id)
        +remove_amenity_from_place(place_id, amenity_id)
        +create_review(review_data)
        +get_review(review_id)
        +get_reviews_by_place(place_id)
        +get_reviews_by_user(user_id)
        +get_all_reviews()
        +update_review(review_id, review_data)
        +create_amenity(amenity_data)
        +get_amenity(amenity_id)
        +get_amenity_by_name(name)
        +get_all_amenities()
        +update_amenity(amenity_id, amenity_data)
        +get_places_by_amenity(amenity_id)
    }
    
    HBnBFacade --> UserRepository : uses
    HBnBFacade --> PlaceRepository : uses
    HBnBFacade --> ReviewRepository : uses
    HBnBFacade --> AmenityRepository : uses
``` 