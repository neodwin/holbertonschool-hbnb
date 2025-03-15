#!/usr/bin/env python3
"""
Module d'initialisation de la couche de persistance de l'application HolbertonBnB.
Ce fichier marque le répertoire 'persistence' comme un package Python.

La couche de persistance est responsable de :
- Gérer l'accès aux données stockées en base de données
- Implémenter le pattern Repository pour abstraire les détails de stockage
- Fournir une interface cohérente pour les opérations CRUD (Create, Read, Update, Delete)
- Appliquer les validations liées à l'intégrité des données
- Gérer les transactions et les erreurs liées à la base de données

Chaque type d'entité (User, Place, Amenity, Review) dispose de son propre repository
qui étend les fonctionnalités de base avec des méthodes spécifiques à l'entité.

L'architecture utilisée permet de :
- Faciliter les tests unitaires en permettant de remplacer facilement la source de données
- Centraliser la logique d'accès aux données
- Séparer la logique métier de la logique de persistance
- Maintenir une cohérence dans les opérations sur les données
"""
