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