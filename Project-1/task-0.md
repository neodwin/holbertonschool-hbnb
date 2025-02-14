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
    PresentationLayer -- API
    PresentationLayer -- WebServices
    BusinessLogicLayer -- Models
    BusinessLogicLayer -- DomainLogic
    PersistenceLayer -- Repository
    PersistenceLayer -- Database

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

### Layer Descriptions

1. **Presentation Layer** (Top)
   - Handles all user interactions and API endpoints
   - Manages request/response formatting
   - Provides web services and user interface

2. **Business Logic Layer** (Middle)
   - Contains the core business logic and domain models
   - Implements the Facade pattern through BusinessFacade
   - Manages entities like User, Place, Review, and Amenity

3. **Persistence Layer** (Bottom)
   - Responsible for data storage and retrieval
   - Handles database operations and transactions
   - Manages data mapping and query execution

### Communication via Facade Pattern

The BusinessFacade serves as a unified interface that:
- Simplifies the interaction between layers
- Provides a clean API for the presentation layer
- Encapsulates the complexity of business operations
- Manages the communication with the persistence layer