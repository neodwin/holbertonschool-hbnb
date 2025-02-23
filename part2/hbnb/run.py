"""
Point d'entrée principal de l'application HBnB.
Ce script permet de démarrer le serveur de l'application en mode développement.
"""

from app import create_app

# Création de l'instance de l'application
app = create_app()

if __name__ == '__main__':
    # Démarrage du serveur en mode debug
    # Le mode debug permet le rechargement automatique du serveur lors des modifications
    # et fournit des pages d'erreur détaillées
    app.run(debug=True) 