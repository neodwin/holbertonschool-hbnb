# High-Level Package Diagram

## Overview

This document presents the high-level architecture of the HBnB Evolution application, showing the three main layers and how they communicate through the Facade pattern.

## Architecture Diagram

```mermaid
classDiagram
    %% Main Layers
    class PresentationLayer["Presentation Layer"] {
        <<Package>>
        Web Services
        API Endpoints
    }
    class BusinessLogicLayer["Business Logic Layer"] {
        <<Package>>
        Domain Models
        Business Rules
    }
    class PersistenceLayer["Persistence Layer"] {
        <<Package>>
        Data Storage
        Data Access
    }

    %% Facade
    class BusinessFacade {
        <<Interface>>
        CRUD Operations
        Business Operations
    }

    %% Relationships
    PresentationLayer --> BusinessFacade : uses
    BusinessFacade --> BusinessLogicLayer : manages
    BusinessLogicLayer --> PersistenceLayer : accesses
```

## Layer Descriptions

1. **Presentation Layer**
   - Handles user interactions and API endpoints
   - Manages request/response formatting

2. **Business Logic Layer**
   - Contains core business logic and models
   - Implements business rules and validations

3. **Persistence Layer**
   - Manages data storage and retrieval
   - Handles database operations

## Communication Flow

The BusinessFacade pattern simplifies the interaction between layers by providing a unified interface for the presentation layer to access business operations.