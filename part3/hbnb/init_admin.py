#!/usr/bin/env python3
"""
Script d'initialisation de l'utilisateur administrateur pour l'application HolbertonBnB.
Ce script crée un utilisateur avec des droits d'administrateur si celui-ci n'existe pas déjà.
À utiliser lors de la première configuration de l'application.
"""

from app import create_app
from app.extensions import db
from app.models.user import User

def create_admin():
    """
    Crée un utilisateur administrateur pour l'application HolbertonBnB.
    
    Cette fonction:
    1. Vérifie si un administrateur existe déjà (avec l'email 'admin@hbnb.com')
    2. Si non, crée un nouvel utilisateur avec les droits d'administration
    3. Affiche les informations de connexion pour l'administrateur
    
    Note: En production, il faudrait utiliser un mot de passe plus sécurisé
    et des informations différentes.
    """
    # Création d'une instance de l'application en mode développement
    app = create_app('development')
    
    with app.app_context():
        # Vérifie si l'utilisateur admin existe déjà
        admin = User.query.filter_by(email='admin@hbnb.com').first()
        if admin:
            print("L'utilisateur administrateur existe déjà.")
            return
        
        # Création de l'utilisateur administrateur
        admin = User(
            first_name='Admin',
            last_name='User',
            email='admin@hbnb.com',
            password='adminpassword',  # Sera automatiquement haché par le modèle
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Utilisateur administrateur créé avec succès.")
        print(f"ID Admin: {admin.id}")
        print(f"Email Admin: {admin.email}")
        print(f"Mot de passe Admin: adminpassword")

if __name__ == '__main__':
    create_admin() 