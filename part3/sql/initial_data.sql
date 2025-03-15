-- initial_data.sql
-- Script pour insérer les données initiales dans la base de données HolbertonBnB.
-- Ce fichier ajoute un utilisateur administrateur, un utilisateur régulier,
-- des équipements communs et un exemple de logement pour tester l'application.

-- Insertion de l'utilisateur administrateur
-- Note: Dans une application réelle, il faudrait générer les hachages de mots de passe
-- avec une fonction sécurisée et ne pas les stocker en clair dans les scripts
-- Le hachage ci-dessous correspond au mot de passe 'adminpassword' en utilisant bcrypt
INSERT INTO users (id, first_name, last_name, email, _password_hash, is_admin, created_at, updated_at)
VALUES (
    'admin-uuid-1234-5678-90ab-cdef', -- UUID pour l'utilisateur admin
    'Admin',
    'User',
    'admin@hbnb.com',
    '$2b$12$tVN1BzXLlRbUH1EjzWlQYOUJm6TLPDLEMnM6G9BKwAWHxQ5oJbZ4W', -- Hachage de 'adminpassword'
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insertion d'un utilisateur standard pour les tests
INSERT INTO users (id, first_name, last_name, email, _password_hash, is_admin, created_at, updated_at)
VALUES (
    'user-uuid-1234-5678-90ab-cdef', -- UUID pour l'utilisateur standard
    'Regular',
    'User',
    'user@hbnb.com',
    '$2b$12$tVN1BzXLlRbUH1EjzWlQYOUJm6TLPDLEMnM6G9BKwAWHxQ5oJbZ4W', -- Hachage de 'userpassword'
    FALSE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insertion des équipements communs
-- Cette liste représente les commodités courantes que les utilisateurs
-- peuvent sélectionner pour leurs logements
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

-- Insertion d'un exemple de logement appartenant à l'utilisateur standard
-- Cet exemple permet de tester la fonctionnalité de recherche et d'affichage des logements
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

-- Ajout d'équipements au logement exemple
-- Association des commodités au logement via la table d'association
INSERT INTO place_amenity (place_id, amenity_id) VALUES
('place-uuid-1234-5678-90ab-cdef', 'amenity-uuid-wifi-0000-0000-0000'),
('place-uuid-1234-5678-90ab-cdef', 'amenity-uuid-pool-0000-0000-0000'),
('place-uuid-1234-5678-90ab-cdef', 'amenity-uuid-kitchen-00-0000-0000'),
('place-uuid-1234-5678-90ab-cdef', 'amenity-uuid-ac-0000-0000-0000-00'),
('place-uuid-1234-5678-90ab-cdef', 'amenity-uuid-beachfront-000-0000'); 