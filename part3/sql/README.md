# SQL Scripts for HBnB Database

This directory contains SQL scripts to create and manage the HBnB database schema.

## Files

- `schema.sql`: Creates the database schema (tables, constraints, indexes)
- `initial_data.sql`: Inserts initial data (admin user, amenities, sample place)
- `crud_test.sql`: Tests CRUD operations (Create, Read, Update, Delete)
- `constraint_test.sql`: Tests database constraints and referential integrity
- `setup_database.sh`: Shell script to set up the database and run all scripts

## Database Schema

The database schema consists of the following tables:

1. `users`: Stores user information
   - Primary key: `id`
   - Unique constraint: `email`

2. `amenities`: Stores amenity information
   - Primary key: `id`
   - Unique constraint: `name`

3. `places`: Stores place information
   - Primary key: `id`
   - Foreign key: `owner_id` references `users(id)`

4. `reviews`: Stores review information
   - Primary key: `id`
   - Foreign key: `place_id` references `places(id)`
   - Foreign key: `user_id` references `users(id)`
   - Unique constraint: `(place_id, user_id)` (a user can only review a place once)

5. `place_amenity`: Association table for the many-to-many relationship between places and amenities
   - Primary key: `(place_id, amenity_id)`
   - Foreign key: `place_id` references `places(id)`
   - Foreign key: `amenity_id` references `amenities(id)`

## Usage

### Setting up the database

To set up the database and run all scripts, use the `setup_database.sh` script:

```bash
cd part3/sql
./setup_database.sh
```

This will:
1. Create a new SQLite database file (`hbnb.db`)
2. Create the database schema
3. Insert initial data
4. Run CRUD tests
5. Run constraint tests (some errors are expected)

### Exploring the database

To explore the database manually, use the SQLite command-line tool:

```bash
cd part3/sql
sqlite3 hbnb.db
```

Some useful SQLite commands:
- `.tables`: List all tables
- `.schema [table]`: Show the schema for a table
- `.headers on`: Show column headers in query results
- `.mode column`: Format query results as columns
- `.exit`: Exit SQLite

### Running individual scripts

You can also run individual scripts using the SQLite command-line tool:

```bash
cd part3/sql
sqlite3 hbnb.db < schema.sql
sqlite3 hbnb.db < initial_data.sql
sqlite3 hbnb.db < crud_test.sql
sqlite3 hbnb.db < constraint_test.sql
```

## Notes

- The `constraint_test.sql` script intentionally includes operations that should fail due to constraint violations. These errors are expected and demonstrate that the database constraints are working correctly.
- The `setup_database.sh` script will delete any existing `hbnb.db` file before creating a new one. 