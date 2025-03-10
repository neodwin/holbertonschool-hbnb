-- crud_test.sql
-- Script to test CRUD operations on the HBnB database

-- =====================
-- CREATE operations
-- =====================

-- Create a new user
INSERT INTO users (id, first_name, last_name, email, _password_hash, is_admin, created_at, updated_at)
VALUES (
    'test-user-uuid-create-test-0000',
    'Test',
    'User',
    'test.create@example.com',
    '$2b$12$tVN1BzXLlRbUH1EjzWlQYOUJm6TLPDLEMnM6G9BKwAWHxQ5oJbZ4W',
    FALSE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Create a new amenity
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    'test-amenity-uuid-create-0000',
    'Test Amenity',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Create a new place
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'test-place-uuid-create-test-00',
    'Test Place',
    'A place created for testing purposes',
    100.00,
    40.7128,
    -74.0060,
    'test-user-uuid-create-test-0000',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Create a new review
INSERT INTO reviews (id, text, rating, place_id, user_id, created_at, updated_at)
VALUES (
    'test-review-uuid-create-test-0',
    'This is a test review',
    5,
    'test-place-uuid-create-test-00',
    'test-user-uuid-create-test-0000',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Create a place-amenity association
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    'test-place-uuid-create-test-00',
    'test-amenity-uuid-create-0000'
);

-- =====================
-- READ operations
-- =====================

-- Read all users
SELECT * FROM users;

-- Read a specific user
SELECT * FROM users WHERE id = 'test-user-uuid-create-test-0000';

-- Read all places owned by a specific user
SELECT * FROM places WHERE owner_id = 'test-user-uuid-create-test-0000';

-- Read all reviews for a specific place
SELECT * FROM reviews WHERE place_id = 'test-place-uuid-create-test-00';

-- Read all amenities for a specific place
SELECT a.* 
FROM amenities a
JOIN place_amenity pa ON a.id = pa.amenity_id
WHERE pa.place_id = 'test-place-uuid-create-test-00';

-- Read all places with a specific amenity
SELECT p.* 
FROM places p
JOIN place_amenity pa ON p.id = pa.place_id
WHERE pa.amenity_id = 'test-amenity-uuid-create-0000';

-- =====================
-- UPDATE operations
-- =====================

-- Update a user
UPDATE users
SET first_name = 'Updated', last_name = 'User', updated_at = CURRENT_TIMESTAMP
WHERE id = 'test-user-uuid-create-test-0000';

-- Verify the update
SELECT * FROM users WHERE id = 'test-user-uuid-create-test-0000';

-- Update a place
UPDATE places
SET title = 'Updated Test Place', price = 120.00, updated_at = CURRENT_TIMESTAMP
WHERE id = 'test-place-uuid-create-test-00';

-- Verify the update
SELECT * FROM places WHERE id = 'test-place-uuid-create-test-00';

-- Update a review
UPDATE reviews
SET text = 'This is an updated test review', rating = 4, updated_at = CURRENT_TIMESTAMP
WHERE id = 'test-review-uuid-create-test-0';

-- Verify the update
SELECT * FROM reviews WHERE id = 'test-review-uuid-create-test-0';

-- =====================
-- DELETE operations
-- =====================

-- Delete a place-amenity association
DELETE FROM place_amenity
WHERE place_id = 'test-place-uuid-create-test-00' AND amenity_id = 'test-amenity-uuid-create-0000';

-- Verify the deletion
SELECT * FROM place_amenity WHERE place_id = 'test-place-uuid-create-test-00';

-- Delete a review
DELETE FROM reviews
WHERE id = 'test-review-uuid-create-test-0';

-- Verify the deletion
SELECT * FROM reviews WHERE id = 'test-review-uuid-create-test-0';

-- Delete a place
DELETE FROM places
WHERE id = 'test-place-uuid-create-test-00';

-- Verify the deletion
SELECT * FROM places WHERE id = 'test-place-uuid-create-test-00';

-- Delete an amenity
DELETE FROM amenities
WHERE id = 'test-amenity-uuid-create-0000';

-- Verify the deletion
SELECT * FROM amenities WHERE id = 'test-amenity-uuid-create-0000';

-- Delete a user
DELETE FROM users
WHERE id = 'test-user-uuid-create-test-0000';

-- Verify the deletion
SELECT * FROM users WHERE id = 'test-user-uuid-create-test-0000'; 