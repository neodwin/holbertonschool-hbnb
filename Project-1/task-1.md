```mermaid

classDiagram
    class User {
        -String Name
        -int PosX
        -int PosY
        +Despawn() void
    }
    class Place {
        +int MaxHealth
        -int Health
        +IsDead() bool
        +TakeDamage(int damage) void
        +OnKilled()* void
    }
    class Review {
        +int MaxHealth
        -int Health
        +IsDead() bool
        +TakeDamage(int damage) void
        +OnKilled()* void
    }
    class Amenity {
        +int MaxHealth
        -int Health
        +IsDead() bool
        +TakeDamage(int damage) void
        +OnKilled()* void
    }

    GameObject <|-- DamageableObject