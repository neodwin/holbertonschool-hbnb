# Scripts SQL pour la Base de Données HBnB

Ce répertoire contient les scripts SQL nécessaires pour créer et gérer le schéma de la base de données HBnB.

## Fichiers

- `schema.sql` : Crée le schéma de la base de données (tables, contraintes, index)
- `initial_data.sql` : Insère les données initiales (utilisateur administrateur, équipements, exemple de logement)
- `crud_test.sql` : Teste les opérations CRUD (Création, Lecture, Mise à jour, Suppression)
- `constraint_test.sql` : Teste les contraintes de la base de données et l'intégrité référentielle
- `setup_database.sh` : Script shell pour configurer la base de données et exécuter tous les scripts

## Schéma de la Base de Données

Le schéma de la base de données comprend les tables suivantes :

1. `users` : Stocke les informations des utilisateurs
   - Clé primaire : `id`
   - Contrainte d'unicité : `email`
   - Contient le hash du mot de passe, les informations personnelles et les statuts administrateur

2. `amenities` : Stocke les informations sur les équipements/commodités
   - Clé primaire : `id`
   - Contrainte d'unicité : `name`
   - Permet d'enregistrer les différentes options disponibles dans les logements

3. `places` : Stocke les informations sur les logements
   - Clé primaire : `id`
   - Clé étrangère : `owner_id` référence `users(id)`
   - Contient le titre, la description, le prix et les coordonnées géographiques

4. `reviews` : Stocke les avis sur les logements
   - Clé primaire : `id`
   - Clé étrangère : `place_id` référence `places(id)`
   - Clé étrangère : `user_id` référence `users(id)`
   - Contrainte d'unicité : `(place_id, user_id)` (un utilisateur ne peut donner qu'un seul avis par logement)
   - Contient le texte de l'avis et la note attribuée

5. `place_amenity` : Table d'association pour la relation plusieurs-à-plusieurs entre logements et équipements
   - Clé primaire : `(place_id, amenity_id)`
   - Clé étrangère : `place_id` référence `places(id)`
   - Clé étrangère : `amenity_id` référence `amenities(id)`
   - Permet d'associer plusieurs équipements à un logement et vice-versa

## Utilisation

### Configuration de la base de données

Pour configurer la base de données et exécuter tous les scripts, utilisez le script `setup_database.sh` :

```bash
cd part3/sql
./setup_database.sh
```

Ce script va :
1. Créer un nouveau fichier de base de données SQLite (`hbnb.db`)
2. Créer le schéma de la base de données
3. Insérer les données initiales
4. Exécuter les tests CRUD
5. Exécuter les tests de contraintes (certaines erreurs sont attendues)

### Explorer la base de données

Pour explorer manuellement la base de données, utilisez l'outil en ligne de commande SQLite :

```bash
cd part3/sql
sqlite3 hbnb.db
```

Quelques commandes SQLite utiles :
- `.tables` : Liste toutes les tables
- `.schema [table]` : Affiche le schéma d'une table
- `.headers on` : Affiche les en-têtes de colonnes dans les résultats des requêtes
- `.mode column` : Formate les résultats des requêtes en colonnes
- `.exit` : Quitte SQLite

### Exécution de scripts individuels

Vous pouvez également exécuter des scripts individuels à l'aide de l'outil en ligne de commande SQLite :

```bash
cd part3/sql
sqlite3 hbnb.db < schema.sql
sqlite3 hbnb.db < initial_data.sql
sqlite3 hbnb.db < crud_test.sql
sqlite3 hbnb.db < constraint_test.sql
```

## Remarques

- Le script `constraint_test.sql` inclut intentionnellement des opérations qui devraient échouer en raison de violations de contraintes. Ces erreurs sont attendues et démontrent que les contraintes de la base de données fonctionnent correctement.
- Le script `setup_database.sh` supprimera tout fichier `hbnb.db` existant avant d'en créer un nouveau.
- Toutes les tables utilisent des identifiants UUID au format de chaîne pour assurer l'unicité globale des clés.
- Les suppressions en cascade sont configurées pour maintenir l'intégrité référentielle (par exemple, lorsqu'un utilisateur est supprimé, tous ses logements et avis sont également supprimés).
- Des index ont été ajoutés sur les clés étrangères fréquemment utilisées pour améliorer les performances des requêtes. 