-- constraint_test.sql
-- Script to test database constraints and referential integrity

-- =====================
-- Test foreign key constraints
-- =====================

-- Test 1: Try to create a place with a non-existent owner_id
-- This should fail due to the foreign key constraint
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'constraint-test-place-1',
    'Invalid Place',
    'This place has an invalid owner_id',
    100.00,
    40.7128,
    -74.0060,
    'non-existent-user-id',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Test 2: Try to create a review with a non-existent place_id
-- This should fail due to the foreign key constraint
INSERT INTO reviews (id, text, rating, place_id, user_id, created_at, updated_at)
VALUES (
    'constraint-test-review-1',
    'This is a test review',
    5,
    'non-existent-place-id',
    'user-uuid-1234-5678-90ab-cdef',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Test 3: Try to create a review with a non-existent user_id
-- This should fail due to the foreign key constraint
INSERT INTO reviews (id, text, rating, place_id, user_id, created_at, updated_at)
VALUES (
    'constraint-test-review-2',
    'This is a test review',
    5,
    'place-uuid-1234-5678-90ab-cdef',
    'non-existent-user-id',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Test 4: Try to create a place_amenity association with a non-existent place_id
-- This should fail due to the foreign key constraint
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    'non-existent-place-id',
    'amenity-uuid-wifi-0000-0000-0000'
);

-- Test 5: Try to create a place_amenity association with a non-existent amenity_id
-- This should fail due to the foreign key constraint
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    'place-uuid-1234-5678-90ab-cdef',
    'non-existent-amenity-id'
);

-- =====================
-- Test unique constraints
-- =====================

-- Test 6: Try to create a user with an existing email
-- This should fail due to the unique constraint on email
INSERT INTO users (id, first_name, last_name, email, _password_hash, is_admin, created_at, updated_at)
VALUES (
    'constraint-test-user-1',
    'Duplicate',
    'Email',
    'admin@hbnb.com', -- This email already exists
    '$2b$12$tVN1BzXLlRbUH1EjzWlQYOUJm6TLPDLEMnM6G9BKwAWHxQ5oJbZ4W',
    FALSE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Test 7: Try to create an amenity with an existing name
-- This should fail due to the unique constraint on name
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    'constraint-test-amenity-1',
    'WiFi', -- This name already exists
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Test 8: Try to create a duplicate review for the same place and user
-- This should fail due to the unique constraint on (place_id, user_id)
-- First, create a valid review
INSERT INTO reviews (id, text, rating, place_id, user_id, created_at, updated_at)
VALUES (
    'constraint-test-review-3',
    'This is a valid review',
    5,
    'place-uuid-1234-5678-90ab-cdef',
    'admin-uuid-1234-5678-90ab-cdef',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Now try to create another review for the same place and user
-- This should fail
INSERT INTO reviews (id, text, rating, place_id, user_id, created_at, updated_at)
VALUES (
    'constraint-test-review-4',
    'This is a duplicate review',
    4,
    'place-uuid-1234-5678-90ab-cdef',
    'admin-uuid-1234-5678-90ab-cdef',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- =====================
-- Test cascading deletes
-- =====================

-- Test 9: Create a test user, place, and review to test cascading deletes
INSERT INTO users (id, first_name, last_name, email, _password_hash, is_admin, created_at, updated_at)
VALUES (
    'cascade-test-user-1',
    'Cascade',
    'Test',
    'cascade.test@example.com',
    '$2b$12$tVN1BzXLlRbUH1EjzWlQYOUJm6TLPDLEMnM6G9BKwAWHxQ5oJbZ4W',
    FALSE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'cascade-test-place-1',
    'Cascade Test Place',
    'A place created for testing cascading deletes',
    100.00,
    40.7128,
    -74.0060,
    'cascade-test-user-1',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO reviews (id, text, rating, place_id, user_id, created_at, updated_at)
VALUES (
    'cascade-test-review-1',
    'This is a review for testing cascading deletes',
    5,
    'cascade-test-place-1',
    'admin-uuid-1234-5678-90ab-cdef',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    'cascade-test-place-1',
    'amenity-uuid-wifi-0000-0000-0000'
);

-- Verify that the data was created
SELECT * FROM users WHERE id = 'cascade-test-user-1';
SELECT * FROM places WHERE id = 'cascade-test-place-1';
SELECT * FROM reviews WHERE id = 'cascade-test-review-1';
SELECT * FROM place_amenity WHERE place_id = 'cascade-test-place-1';

-- Now delete the user and verify that the place and its associated data are also deleted
DELETE FROM users WHERE id = 'cascade-test-user-1';

-- Verify that the place was deleted (should return no rows)
SELECT * FROM places WHERE id = 'cascade-test-place-1';

-- Verify that the review was deleted (should return no rows)
SELECT * FROM reviews WHERE id = 'cascade-test-review-1';

-- Verify that the place_amenity association was deleted (should return no rows)
SELECT * FROM place_amenity WHERE place_id = 'cascade-test-place-1';

-- Clean up the test review created earlier
DELETE FROM reviews WHERE id = 'constraint-test-review-3'; 