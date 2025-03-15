#!/usr/bin/env python3
"""
Extensions Flask utilisées par l'application HolbertonBnB.
Ce module initialise les extensions Flask de manière centralisée pour éviter
les dépendances circulaires et permettre leur réutilisation dans différents modules.
"""

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# Extension pour le hachage des mots de passe
# Utilise l'algorithme bcrypt, considéré comme sécurisé pour le stockage des mots de passe
bcrypt = Bcrypt()

# Extension pour gérer l'authentification par tokens JWT (JSON Web Tokens)
# Permet de créer, valider et rafraîchir les tokens d'authentification
jwt = JWTManager()

# ORM (Object-Relational Mapping) pour interagir avec la base de données
# Permet de définir des modèles Python qui sont mappés aux tables de la base de données
db = SQLAlchemy() 