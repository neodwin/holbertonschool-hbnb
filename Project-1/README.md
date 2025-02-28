# HBnB Technical Documentation

## Overview
This directory contains the complete technical documentation for the HBnB (Holberton BnB) project, including architectural diagrams, design patterns, and implementation guidelines.

## Document Structure

### 1. Package Diagram (`task-0.md`)
- High-level architecture visualization
- Three-tier architecture implementation
- Facade pattern design
- Component relationships and responsibilities
- Layer descriptions:
  - Presentation Layer (API & Web UI)
  - Business Logic Layer (Models & Services)
  - Persistence Layer (Database & Repository)

### 2. Class Diagram (`task-1.md`)
- Detailed business logic layer design
- Core domain models:
  - BaseModel (Abstract base class)
  - User (Account management)
  - Place (Property listings)
  - Review (User feedback)
  - Amenity (Property features)
- Entity relationships and inheritance patterns
- Data model attributes and methods

### 3. Sequence Diagrams (`task-2.md`)
Key API interaction flows with error handling:
1. User Registration
   - Success path and validation
   - Error scenarios (400, 409, 500)

2. Place Creation
   - Authentication flow
   - Error handling (401, 400, 500)

3. Review Submission
   - Authorization checks
   - Error scenarios (404, 401, 400)

4. Place Listing Retrieval
   - Filter processing
   - Error handling (400, 204, 500)

### 4. Complete Documentation (`task-3.md`)
Comprehensive technical blueprint including:
- Architectural overview
- Design patterns implementation
- Error handling strategy
- Security considerations
- Performance optimization
- Code organization
- Implementation guidelines

## Key Technical Decisions

### Architecture
- Three-tier architecture for separation of concerns
- Facade pattern for simplified interface
- RESTful API design
- Modular component structure

### Data Management
- UUID-based identification
- Timestamp tracking
- Automated validation
- Relationship management

### Security
- JWT authentication
- Role-based access control
- Input validation at multiple levels
- Secure password handling

### Error Handling
- Standardized HTTP status codes
- Consistent error response format
- Comprehensive error logging
- Multiple validation layers

## Implementation Stack
- Backend: Python with Flask/Django
- Database: PostgreSQL
- ORM: SQLAlchemy
- Frontend: React.js with Bootstrap
- Authentication: JWT
- Caching: Redis

## Getting Started
1. Review the architecture overview in `task-0.md`
2. Study the domain model in `task-1.md`
3. Understand API flows in `task-2.md`
4. Consult implementation details in `task-3.md`

## Authors
- Ewan
- Edwin
- Frederic

## License
This project is licensed under the MIT License