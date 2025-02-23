"""
Package gérant la persistance des données de l'application HBnB.
Ce package fournit les interfaces et implémentations pour :
- Le stockage des objets du domaine
- La récupération des objets par ID ou attributs
- La mise à jour et la suppression des objets

L'implémentation actuelle utilise un stockage en mémoire (InMemoryRepository),
mais l'architecture permet facilement d'ajouter d'autres types de stockage
(base de données, fichiers, etc.) en implémentant l'interface Repository.
"""
