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

    %% Inheritance relationships
    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity

    %% Associations with multiplicity
    User --> Place : owns
    User --> Review : writes
    Place --> Review : has
    Place --> Amenity : includes
