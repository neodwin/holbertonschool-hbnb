# Diagrams for HBnB

This directory contains diagrams for the HBnB project, created with Mermaid.js.

## Contents

- `er_diagram.md`: Entity-Relationship (ER) diagram for the database
- `class_diagram.md`: Class diagram for SQLAlchemy models
- `architecture_diagram.md`: Architecture diagram for the application

## About Mermaid.js

[Mermaid.js](https://mermaid.js.org/) is a JavaScript-based diagram generation tool that allows you to create diagrams from Markdown-like syntax. It's particularly useful for creating ER diagrams, class diagrams, sequence diagrams, flowcharts, etc.

## How to View the Diagrams

### Option 1: GitHub

If you're viewing these files on GitHub, Mermaid diagrams are automatically rendered in the web interface.

### Option 2: Mermaid Live Editor

You can copy and paste the Mermaid code into the [Mermaid Live Editor](https://mermaid.live/) to view and modify the diagrams.

### Option 3: VS Code Extensions

If you're using VS Code, you can install the [Mermaid Preview](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) extension to view diagrams directly in the editor.

## Types of Diagrams

### ER Diagram (Entity-Relationship)

The ER diagram represents the database structure, showing tables, their attributes, and relationships between them. It's useful for understanding how data is organized and linked in the database.

### Class Diagram

The class diagram represents the structure of Python classes used in the project, showing attributes, methods, and relationships between classes. It's useful for understanding the object-oriented architecture of the project.

### Architecture Diagram

The architecture diagram represents the overall structure of the application, showing the different layers and their interactions. It's useful for understanding how the different parts of the application work together.

## HBnB Project Structure

The HBnB project is structured in several layers:

1. **Presentation Layer**: REST API with JWT authentication
2. **Business Layer**: Facade (HBnBFacade) that centralizes business logic
3. **Persistence Layer**: Repositories that manage data access
4. **Data Layer**: SQLite/MySQL database

The main entities of the project are:

1. **User**: Application users
2. **Place**: Properties/locations for rent
3. **Review**: User reviews of places
4. **Amenity**: Facilities/amenities available in places 