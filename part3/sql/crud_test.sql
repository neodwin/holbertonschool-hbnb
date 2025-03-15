-- crud_test.sql
-- Script de test des opérations CRUD (Create, Read, Update, Delete) sur la base de données HolbertonBnB.
-- Ce fichier contient des requêtes SQL pour vérifier que toutes les opérations de base
-- fonctionnent correctement sur les différentes tables.

-- =====================
-- Opérations CREATE (Création)
-- =====================

-- Création d'un nouvel utilisateur
-- Test de l'insertion de données dans la table users
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

-- Création d'un nouvel équipement
-- Test de l'insertion de données dans la table amenities
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    'test-amenity-uuid-create-0000',
    'Test Amenity',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Création d'un nouveau logement
-- Test de l'insertion de données dans la table places avec référence à un utilisateur existant
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'test-place-uuid-create-test-000',
    'Test Place',
    'A place created for testing',
    120.00,
    37.7749,
    -122.4194,
    'test-user-uuid-create-test-0000',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Création d'un nouvel avis
-- Test de l'insertion de données dans la table reviews avec références aux tables users et places
INSERT INTO reviews (id, text, rating, place_id, user_id, created_at, updated_at)
VALUES (
    'test-review-uuid-create-0000',
    'This is a test review',
    4,
    'test-place-uuid-create-test-000',
    'test-user-uuid-create-test-0000',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Association d'un équipement à un logement
-- Test de l'insertion de données dans la table d'association place_amenity
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    'test-place-uuid-create-test-000',
    'test-amenity-uuid-create-0000'
);

-- =====================
-- Opérations READ (Lecture)
-- =====================

-- Lecture d'un utilisateur par son ID
-- Vérifie que l'utilisateur créé est correctement récupérable
SELECT * FROM users WHERE id = 'test-user-uuid-create-test-0000';

-- Lecture d'un équipement par son nom
-- Vérifie que l'équipement créé est correctement récupérable
SELECT * FROM amenities WHERE name = 'Test Amenity';

-- Lecture d'un logement et de son propriétaire par ID
-- Utilisation d'une jointure pour récupérer des données liées
SELECT p.*, u.first_name, u.last_name, u.email
FROM places p
JOIN users u ON p.owner_id = u.id
WHERE p.id = 'test-place-uuid-create-test-000';

-- Lecture d'un avis et des informations associées
-- Jointure complexe pour récupérer l'avis, l'utilisateur et le logement concernés
SELECT r.*, u.first_name, u.last_name, p.title
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN places p ON r.place_id = p.id
WHERE r.id = 'test-review-uuid-create-0000';

-- Lecture des équipements d'un logement
-- Utilisation d'une jointure via la table d'association
SELECT a.*
FROM amenities a
JOIN place_amenity pa ON a.id = pa.amenity_id
WHERE pa.place_id = 'test-place-uuid-create-test-000';

-- =====================
-- Opérations UPDATE (Mise à jour)
-- =====================

-- Mise à jour des informations d'un utilisateur
-- Test de la modification de données existantes
UPDATE users
SET first_name = 'Updated', last_name = 'Name', updated_at = CURRENT_TIMESTAMP
WHERE id = 'test-user-uuid-create-test-0000';

-- Vérification de la mise à jour de l'utilisateur
SELECT * FROM users WHERE id = 'test-user-uuid-create-test-0000';

-- Mise à jour du nom d'un équipement
UPDATE amenities
SET name = 'Updated Amenity', updated_at = CURRENT_TIMESTAMP
WHERE id = 'test-amenity-uuid-create-0000';

-- Vérification de la mise à jour de l'équipement
SELECT * FROM amenities WHERE id = 'test-amenity-uuid-create-0000';

-- Mise à jour des informations d'un logement
UPDATE places
SET title = 'Updated Place', price = 150.00, updated_at = CURRENT_TIMESTAMP
WHERE id = 'test-place-uuid-create-test-000';

-- Vérification de la mise à jour du logement
SELECT * FROM places WHERE id = 'test-place-uuid-create-test-000';

-- Mise à jour d'un avis
UPDATE reviews
SET text = 'This is an updated review', rating = 5, updated_at = CURRENT_TIMESTAMP
WHERE id = 'test-review-uuid-create-0000';

-- Vérification de la mise à jour de l'avis
SELECT * FROM reviews WHERE id = 'test-review-uuid-create-0000';

-- =====================
-- Opérations DELETE (Suppression)
-- =====================

-- Suppression de l'association équipement-logement
-- Test de la suppression dans une table d'association
DELETE FROM place_amenity
WHERE place_id = 'test-place-uuid-create-test-000' AND amenity_id = 'test-amenity-uuid-create-0000';

-- Vérification de la suppression de l'association
SELECT * FROM place_amenity
WHERE place_id = 'test-place-uuid-create-test-000' AND amenity_id = 'test-amenity-uuid-create-0000';

-- Suppression de l'avis
-- Test de la suppression d'une entité avec des clés étrangères
DELETE FROM reviews
WHERE id = 'test-review-uuid-create-0000';

-- Vérification de la suppression de l'avis
SELECT * FROM reviews WHERE id = 'test-review-uuid-create-0000';

-- Suppression du logement
-- Test de l'effet cascade sur les avis et associations
DELETE FROM places
WHERE id = 'test-place-uuid-create-test-000';

-- Vérification de la suppression du logement
SELECT * FROM places WHERE id = 'test-place-uuid-create-test-000';

-- Suppression de l'équipement
DELETE FROM amenities
WHERE id = 'test-amenity-uuid-create-0000';

-- Vérification de la suppression de l'équipement
SELECT * FROM amenities WHERE id = 'test-amenity-uuid-create-0000';

-- Suppression de l'utilisateur
-- Test de l'effet cascade sur les logements et avis
DELETE FROM users
WHERE id = 'test-user-uuid-create-test-0000';

-- Vérification de la suppression de l'utilisateur
SELECT * FROM users WHERE id = 'test-user-uuid-create-test-0000'; 