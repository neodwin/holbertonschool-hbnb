"""
Module de configuration de l'application HBnB.
Ce module définit les différentes configurations possibles pour l'application,
permettant une gestion flexible des paramètres selon l'environnement d'exécution.
"""

import os

class Config:
    """
    Classe de configuration de base.
    Contient les paramètres de configuration communs à tous les environnements.
    
    Attributs:
        SECRET_KEY (str): Clé secrète utilisée pour la sécurité de l'application
                         (sessions, tokens, etc.). Peut être définie via une 
                         variable d'environnement.
        DEBUG (bool): Mode debug désactivé par défaut dans la configuration de base.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    """
    Configuration spécifique pour l'environnement de développement.
    Hérite de la classe Config de base.
    
    Cette configuration active le mode debug pour faciliter le développement
    et le débogage de l'application.
    
    Attributs:
        DEBUG (bool): Mode debug activé pour l'environnement de développement.
    """
    DEBUG = True

# Dictionnaire des configurations disponibles
config = {
    'development': DevelopmentConfig,  # Configuration de développement
    'default': DevelopmentConfig       # Configuration par défaut
} 