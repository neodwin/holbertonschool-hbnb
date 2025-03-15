#!/bin/bash
# Script de configuration de la base de données SQLite pour l'application HolbertonBnB
# Ce script initialise la base de données, crée les tables et insère les données initiales

# Se déplacer dans le répertoire contenant ce script
# Cela garantit que les chemins relatifs des fichiers SQL fonctionneront correctement
cd "$(dirname "$0")"

# Définir le fichier de base de données SQLite
DB_FILE="hbnb.db"

# Supprimer le fichier de base de données existant s'il existe
# Cela permet d'avoir une base de données propre à chaque exécution du script
if [ -f "$DB_FILE" ]; then
    echo "Suppression du fichier de base de données existant..."
    rm "$DB_FILE"
fi

# Créer une nouvelle base de données SQLite et exécuter le script de schéma
# Ce script crée toutes les tables, contraintes et index nécessaires
echo "Création du schéma de la base de données..."
sqlite3 "$DB_FILE" < schema.sql

# Insérer les données initiales
# Ce script ajoute un administrateur, un utilisateur standard et des équipements courants
echo "Insertion des données initiales..."
sqlite3 "$DB_FILE" < initial_data.sql

# Exécuter les tests CRUD
# Ce script vérifie que les opérations Create, Read, Update et Delete fonctionnent correctement
echo "Exécution des tests CRUD..."
sqlite3 "$DB_FILE" < crud_test.sql

# Exécuter les tests de contraintes
# Ces tests vont générer des erreurs intentionnellement pour vérifier les contraintes d'intégrité
echo "Exécution des tests de contraintes (des erreurs sont attendues)..."
sqlite3 "$DB_FILE" < constraint_test.sql

echo "Configuration de la base de données terminée !"
echo "Vous pouvez explorer la base de données avec la commande: sqlite3 $DB_FILE" 