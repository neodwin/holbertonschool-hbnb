-- initial_data.sql
-- Script to insert initial data into the HBnB database

-- Insert admin user
-- Note: In a real application, you would use a secure hashing function for passwords
-- The password hash below is for 'adminpassword' using bcrypt
INSERT INTO users (id, first_name, last_name, email, _password_hash, is_admin, created_at, updated_at)
VALUES (
    'admin-uuid-1234-5678-90ab-cdef', -- UUID for admin user
    'Admin',
    'User',
    'admin@hbnb.com',
    '$2b$12$tVN1BzXLlRbUH1EjzWlQYOUJm6TLPDLEMnM6G9BKwAWHxQ5oJbZ4W', -- Hashed 'adminpassword'
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert regular user for testing
INSERT INTO users (id, first_name, last_name, email, _password_hash, is_admin, created_at, updated_at)
VALUES (
    'user-uuid-1234-5678-90ab-cdef', -- UUID for regular user
    'Regular',
    'User',
    'user@hbnb.com',
    '$2b$12$tVN1BzXLlRbUH1EjzWlQYOUJm6TLPDLEMnM6G9BKwAWHxQ5oJbZ4W', -- Hashed 'userpassword'
    FALSE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert common amenities
INSERT INTO amenities (id, name, created_at, updated_at) VALUES
('amenity-uuid-wifi-0000-0000-0000', 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-pool-0000-0000-0000', 'Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-kitchen-00-0000-0000', 'Kitchen', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-washer-00-0000-0000', 'Washer', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-dryer-00-0000-0000', 'Dryer', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-ac-0000-0000-0000-00', 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-heating-0-0000-0000', 'Heating', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-workspace-0000-0000', 'Dedicated Workspace', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-tv-0000-0000-0000-00', 'TV', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-hairdryer-0000-0000', 'Hair Dryer', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-iron-00-0000-0000-00', 'Iron', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-parking-0-0000-0000', 'Free Parking', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-ev-0000-0000-0000-00', 'EV Charger', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-crib-00-0000-0000-00', 'Crib', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-gym-000-0000-0000-00', 'Gym', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-bbq-000-0000-0000-00', 'BBQ Grill', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-breakfast-0000-0000', 'Breakfast', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-fireplace-0000-0000', 'Indoor Fireplace', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-smoking-0-0000-0000', 'Smoking Allowed', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-beachfront-000-0000', 'Beachfront', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-waterfront-000-0000', 'Waterfront', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('amenity-uuid-ski-000-0000-0000-00', 'Ski-in/Ski-out', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert a sample place owned by the regular user
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'place-uuid-1234-5678-90ab-cdef',
    'Beautiful Beach House',
    'A stunning beach house with ocean views and modern amenities.',
    150.00,
    34.0522,
    -118.2437,
    'user-uuid-1234-5678-90ab-cdef',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Add amenities to the sample place
INSERT INTO place_amenity (place_id, amenity_id) VALUES
('place-uuid-1234-5678-90ab-cdef', 'amenity-uuid-wifi-0000-0000-0000'),
('place-uuid-1234-5678-90ab-cdef', 'amenity-uuid-pool-0000-0000-0000'),
('place-uuid-1234-5678-90ab-cdef', 'amenity-uuid-kitchen-00-0000-0000'),
('place-uuid-1234-5678-90ab-cdef', 'amenity-uuid-ac-0000-0000-0000-00'),
('place-uuid-1234-5678-90ab-cdef', 'amenity-uuid-beachfront-000-0000'); 