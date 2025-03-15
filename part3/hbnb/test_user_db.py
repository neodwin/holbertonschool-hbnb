#!/usr/bin/env python3
"""
Script de test des opérations CRUD pour le modèle User de l'application HolbertonBnB.
Ce module vérifie que les opérations de base (Création, Lecture, Mise à jour, Suppression)
fonctionnent correctement pour les utilisateurs dans la base de données.
"""

from app import create_app
from app.extensions import db
from app.models.user import User
from app.db_init import init_db
import json

def test_user_crud():
    """
    Teste les opérations CRUD (Create, Read, Update, Delete) pour le modèle User.
    
    Cette fonction vérifie :
    - La création d'un utilisateur avec son mot de passe hashé
    - La récupération d'un utilisateur par son email
    - La vérification du mot de passe hashé
    - La mise à jour des informations d'un utilisateur
    - La suppression d'un utilisateur
    """
    # Création d'une instance d'application avec la configuration de test
    app = create_app('testing')
    
    with app.app_context():
        # Initialisation de la base de données
        db.create_all()
        
        # Création d'un utilisateur de test
        test_user = User(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='testpassword'  # Le mot de passe sera automatiquement hashé
        )
        db.session.add(test_user)
        db.session.commit()
        
        # Récupération de l'utilisateur par son email
        user = User.query.filter_by(email='test@example.com').first()
        
        # Vérification des informations de l'utilisateur récupéré
        assert user is not None, "L'utilisateur n'a pas été créé correctement"
        assert user.first_name == 'Test', "Le prénom ne correspond pas"
        assert user.last_name == 'User', "Le nom de famille ne correspond pas"
        
        # Vérification que le mot de passe a été correctement hashé et peut être vérifié
        assert user.check_password('testpassword'), "La vérification du mot de passe a échoué"
        
        # Mise à jour des informations de l'utilisateur
        user.first_name = 'Updated'
        db.session.commit()
        
        # Vérification de la mise à jour
        updated_user = User.query.get(user.id)
        assert updated_user.first_name == 'Updated', "La mise à jour n'a pas été appliquée"
        
        # Suppression de l'utilisateur
        db.session.delete(user)
        db.session.commit()
        
        # Vérification de la suppression
        deleted_user = User.query.get(user.id)
        assert deleted_user is None, "L'utilisateur n'a pas été supprimé correctement"
        
        print("Tous les tests CRUD pour le modèle User ont réussi !")
        
        # Nettoyage de la base de données
        db.drop_all()

if __name__ == '__main__':
    # Si ce script est exécuté directement, lance la fonction de test
    test_user_crud() 