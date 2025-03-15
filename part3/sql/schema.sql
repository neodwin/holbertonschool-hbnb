-- schema.sql
-- Script pour créer le schéma de base de données du projet HolbertonBnB.
-- Ce fichier définit la structure des tables, les contraintes et les index
-- pour le stockage des données de l'application.

-- Suppression des tables si elles existent déjà pour éviter les conflits
-- lors de la réinitialisation de la base de données
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

-- Création de la table des utilisateurs
-- Stocke les informations des utilisateurs enregistrés dans l'application
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,                 -- Identifiant unique (UUID)
    first_name VARCHAR(50) NOT NULL,            -- Prénom (obligatoire)
    last_name VARCHAR(50) NOT NULL,             -- Nom de famille (obligatoire)
    email VARCHAR(120) NOT NULL UNIQUE,         -- Email (unique et obligatoire)
    _password_hash VARCHAR(128),                -- Hash du mot de passe (stocké de manière sécurisée)
    is_admin BOOLEAN DEFAULT FALSE,             -- Indique si l'utilisateur est administrateur
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Date de création du compte
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP    -- Date de dernière mise à jour
);

-- Création de la table des équipements/commodités
-- Stocke les équipements disponibles dans les logements (WiFi, piscine, etc.)
CREATE TABLE amenities (
    id VARCHAR(36) PRIMARY KEY,                 -- Identifiant unique (UUID)
    name VARCHAR(50) NOT NULL UNIQUE,           -- Nom de l'équipement (unique et obligatoire)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Date de création 
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP    -- Date de dernière mise à jour
);

-- Création de la table des logements
-- Stocke les informations sur les logements disponibles à la location
CREATE TABLE places (
    id VARCHAR(36) PRIMARY KEY,                 -- Identifiant unique (UUID)
    title VARCHAR(100) NOT NULL,                -- Titre de l'annonce (obligatoire)
    description TEXT,                           -- Description détaillée du logement
    price FLOAT NOT NULL,                       -- Prix par nuit (obligatoire)
    latitude FLOAT NOT NULL,                    -- Coordonnée géographique (latitude)
    longitude FLOAT NOT NULL,                   -- Coordonnée géographique (longitude)
    owner_id VARCHAR(36) NOT NULL,              -- Référence à l'utilisateur propriétaire
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Date de création de l'annonce
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Date de dernière mise à jour
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE  -- Supprime le logement si le propriétaire est supprimé
);

-- Création de la table des avis
-- Stocke les avis laissés par les utilisateurs sur les logements
CREATE TABLE reviews (
    id VARCHAR(36) PRIMARY KEY,                 -- Identifiant unique (UUID)
    text TEXT NOT NULL,                         -- Texte de l'avis (obligatoire)
    rating INTEGER NOT NULL,                    -- Note attribuée (1-5) (obligatoire)
    place_id VARCHAR(36) NOT NULL,              -- Référence au logement concerné
    user_id VARCHAR(36) NOT NULL,               -- Référence à l'utilisateur qui a laissé l'avis
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Date de création de l'avis
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Date de dernière mise à jour
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,  -- Supprime l'avis si le logement est supprimé
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,    -- Supprime l'avis si l'utilisateur est supprimé
    -- Assure qu'un utilisateur ne peut pas laisser plusieurs avis sur le même logement
    UNIQUE (place_id, user_id)
);

-- Création de la table d'association entre logements et équipements
-- Table de jointure pour la relation many-to-many (plusieurs-à-plusieurs)
CREATE TABLE place_amenity (
    place_id VARCHAR(36) NOT NULL,              -- Référence au logement
    amenity_id VARCHAR(36) NOT NULL,            -- Référence à l'équipement
    PRIMARY KEY (place_id, amenity_id),         -- Clé primaire composite
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,      -- Supprime l'association si le logement est supprimé
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE  -- Supprime l'association si l'équipement est supprimé
);

-- Ajout d'index pour améliorer les performances des requêtes fréquentes
CREATE INDEX idx_places_owner_id ON places(owner_id);                       -- Index sur le propriétaire du logement
CREATE INDEX idx_reviews_place_id ON reviews(place_id);                     -- Index sur les avis par logement
CREATE INDEX idx_reviews_user_id ON reviews(user_id);                       -- Index sur les avis par utilisateur
CREATE INDEX idx_place_amenity_place_id ON place_amenity(place_id);         -- Index sur les équipements par logement
CREATE INDEX idx_place_amenity_amenity_id ON place_amenity(amenity_id);     -- Index sur les logements par équipement 