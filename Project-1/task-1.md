```mermaid

classDiagram
    class User {
        +userID
        +surname
        +name
        +adress
        +phone
        +age
        +email
        +birthdate
        +Role
        #password
        +rent()
        +pay()
        +register()
        +addreview()
        +IsOwner()
        +MakeListing()
    }
    class Place {
        +area
        +location
        +GPS
        +numberofrooms
        +price
        +check-in
        +Isfree()
    }
    class Review {
        +UserName
        +UserMail
        +Notations
        +Language
        +evaluate()
    }
    class Amenity {
        +cleaning
        +handicaps
        +animals
        +children
        +Iswithfurnitures()
    }

    User --> Place
    User --> Review
    Review --> Place
    Place <-- Amenity