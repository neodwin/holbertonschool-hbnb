```mermaid

sequenceDiagram
    User->>System: login
    System-->>User: LoginIsOk
    User->>Ad: Create
    User->>Ad: Check
    User->>Ad: AddToCart
    User->>Ad: Confirm
    System->>Availability: Check
    System->>CallReservation: Create
    System->>ConfirmReservation: Confirmation