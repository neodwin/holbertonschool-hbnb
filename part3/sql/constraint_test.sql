-- constraint_test.sql
-- Script de test des contraintes et de l'intégrité référentielle de la base de données HolbertonBnB.
-- Ce fichier contient des requêtes SQL qui doivent échouer pour vérifier que les contraintes
-- d'intégrité sont correctement appliquées.

-- =====================
-- Test des contraintes de clé étrangère
-- =====================

-- Test 1: Tentative de création d'un logement avec un propriétaire inexistant
-- Cette requête doit échouer en raison de la contrainte de clé étrangère sur owner_id
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

-- Test 2: Tentative de création d'un avis avec un logement inexistant
-- Cette requête doit échouer en raison de la contrainte de clé étrangère sur place_id
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

-- Test 3: Tentative de création d'un avis avec un utilisateur inexistant
-- Cette requête doit échouer en raison de la contrainte de clé étrangère sur user_id
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

-- Test 4: Tentative de création d'une association avec un logement inexistant
-- Cette requête doit échouer en raison de la contrainte de clé étrangère dans la table d'association
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    'non-existent-place-id',
    'amenity-uuid-wifi-0000-0000-0000'
);

-- Test 5: Tentative de création d'une association avec un équipement inexistant
-- Cette requête doit échouer en raison de la contrainte de clé étrangère dans la table d'association
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    'place-uuid-1234-5678-90ab-cdef',
    'non-existent-amenity-id'
);

-- =====================
-- Test des contraintes d'unicité
-- =====================

-- Test 6: Tentative de création d'un utilisateur avec un email déjà utilisé
-- Cette requête doit échouer en raison de la contrainte d'unicité sur email
INSERT INTO users (id, first_name, last_name, email, _password_hash, is_admin, created_at, updated_at)
VALUES (
    'constraint-test-user-1',
    'Duplicate',
    'Email',
    'admin@hbnb.com',  -- Cet email existe déjà
    '$2b$12$tVN1BzXLlRbUH1EjzWlQYOUJm6TLPDLEMnM6G9BKwAWHxQ5oJbZ4W',
    FALSE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Test 7: Tentative de création d'un équipement avec un nom déjà utilisé
-- Cette requête doit échouer en raison de la contrainte d'unicité sur name
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    'constraint-test-amenity-1',
    'WiFi',  -- Ce nom existe déjà
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Test 8: Tentative de création d'un avis dupliqué (même utilisateur, même logement)
-- Cette requête doit échouer en raison de la contrainte d'unicité composite sur place_id et user_id
-- D'abord, créons un avis valide
INSERT INTO reviews (id, text, rating, place_id, user_id, created_at, updated_at)
VALUES (
    'constraint-test-review-3',
    'First review from this user',
    4,
    'place-uuid-1234-5678-90ab-cdef',
    'user-uuid-1234-5678-90ab-cdef',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Maintenant, essayons de créer un autre avis du même utilisateur pour le même logement
INSERT INTO reviews (id, text, rating, place_id, user_id, created_at, updated_at)
VALUES (
    'constraint-test-review-4',
    'Second review from the same user for the same place',
    5,
    'place-uuid-1234-5678-90ab-cdef',
    'user-uuid-1234-5678-90ab-cdef',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- =====================
-- Test des contraintes NOT NULL
-- =====================

-- Test 9: Tentative de création d'un utilisateur avec un prénom NULL
-- Cette requête doit échouer en raison de la contrainte NOT NULL sur first_name
INSERT INTO users (id, first_name, last_name, email, _password_hash, is_admin, created_at, updated_at)
VALUES (
    'constraint-test-user-2',
    NULL,  -- Prénom NULL
    'User',
    'null.firstname@example.com',
    '$2b$12$tVN1BzXLlRbUH1EjzWlQYOUJm6TLPDLEMnM6G9BKwAWHxQ5oJbZ4W',
    FALSE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Test 10: Tentative de création d'un logement avec un prix NULL
-- Cette requête doit échouer en raison de la contrainte NOT NULL sur price
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'constraint-test-place-2',
    'Invalid Price Place',
    'This place has a NULL price',
    NULL,  -- Prix NULL
    40.7128,
    -74.0060,
    'user-uuid-1234-5678-90ab-cdef',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Test 11: Tentative de création d'un avis avec un texte NULL
-- Cette requête doit échouer en raison de la contrainte NOT NULL sur text
INSERT INTO reviews (id, text, rating, place_id, user_id, created_at, updated_at)
VALUES (
    'constraint-test-review-5',
    NULL,  -- Texte NULL
    5,
    'place-uuid-1234-5678-90ab-cdef',
    'user-uuid-1234-5678-90ab-cdef',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Test 12: Tentative de création d'un équipement avec un nom NULL
-- Cette requête doit échouer en raison de la contrainte NOT NULL sur name
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    'constraint-test-amenity-2',
    NULL,  -- Nom NULL
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- =====================
-- Test des suppressions en cascade
-- =====================

-- Création d'objets temporaires pour tester les suppressions en cascade
INSERT INTO users (id, first_name, last_name, email, _password_hash, is_admin, created_at, updated_at)
VALUES (
    'cascade-test-user',
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
    'cascade-test-place',
    'Cascade Test Place',
    'This place will be used to test cascade deletion',
    150.00,
    34.0522,
    -118.2437,
    'cascade-test-user',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO reviews (id, text, rating, place_id, user_id, created_at, updated_at)
VALUES (
    'cascade-test-review',
    'This review will be deleted when the place is deleted',
    5,
    'cascade-test-place',
    'cascade-test-user',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    'cascade-test-amenity',
    'Cascade Test Amenity',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    'cascade-test-place',
    'cascade-test-amenity'
);

-- Test 13: Suppression d'un logement et vérification de la cascade sur les avis et associations
-- Cette requête doit supprimer le logement et tous les avis associés
DELETE FROM places WHERE id = 'cascade-test-place';

-- Vérification que l'avis a bien été supprimé en cascade
SELECT * FROM reviews WHERE id = 'cascade-test-review';

-- Vérification que l'association a bien été supprimée en cascade
SELECT * FROM place_amenity WHERE place_id = 'cascade-test-place';

-- Test 14: Suppression d'un utilisateur et vérification de la cascade sur ses logements
-- Cette requête doit supprimer l'utilisateur et tous ses logements
DELETE FROM users WHERE id = 'cascade-test-user';

-- Vérification que tous les logements de l'utilisateur ont été supprimés
SELECT * FROM places WHERE owner_id = 'cascade-test-user';

-- Nettoyage final
DELETE FROM amenities WHERE id = 'cascade-test-amenity'; 