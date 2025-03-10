#!/bin/bash

# Change to the directory containing this script
cd "$(dirname "$0")"

# Define database file
DB_FILE="hbnb.db"

# Remove existing database file if it exists
if [ -f "$DB_FILE" ]; then
    echo "Removing existing database file..."
    rm "$DB_FILE"
fi

# Create a new SQLite database and execute the schema script
echo "Creating database schema..."
sqlite3 "$DB_FILE" < schema.sql

# Insert initial data
echo "Inserting initial data..."
sqlite3 "$DB_FILE" < initial_data.sql

# Run CRUD tests
echo "Running CRUD tests..."
sqlite3 "$DB_FILE" < crud_test.sql

# Run constraint tests (these will produce errors, which is expected)
echo "Running constraint tests (expect some errors)..."
sqlite3 "$DB_FILE" < constraint_test.sql

echo "Database setup complete!"
echo "You can explore the database using: sqlite3 $DB_FILE" 