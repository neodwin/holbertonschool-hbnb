# Diagrammes pour HBnB

Ce répertoire contient les diagrammes pour le projet HBnB, créés avec Mermaid.js.

## Contenu

- `er_diagram.md` : Diagramme Entity-Relationship (ER) pour la base de données
- `class_diagram.md` : Diagramme de classe pour les modèles SQLAlchemy
- `architecture_diagram.md` : Diagramme d'architecture pour l'application

## À propos de Mermaid.js

[Mermaid.js](https://mermaid.js.org/) est un outil de génération de diagrammes basé sur JavaScript qui permet de créer des diagrammes à partir d'une syntaxe de type Markdown. Il est particulièrement utile pour créer des diagrammes ER, des diagrammes de classe, des diagrammes de séquence, des diagrammes de flux, etc.

## Comment visualiser les diagrammes

### Option 1 : GitHub

Si vous consultez ces fichiers sur GitHub, les diagrammes Mermaid sont automatiquement rendus dans l'interface web.

### Option 2 : Éditeur Mermaid Live

Vous pouvez copier-coller le code Mermaid dans l'[éditeur Mermaid Live](https://mermaid.live/) pour visualiser et modifier les diagrammes.

### Option 3 : Extensions VS Code

Si vous utilisez VS Code, vous pouvez installer l'extension [Mermaid Preview](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) pour visualiser les diagrammes directement dans l'éditeur.

## Types de diagrammes

### Diagramme ER (Entity-Relationship)

Le diagramme ER représente la structure de la base de données, montrant les tables, leurs attributs et les relations entre elles. Il est utile pour comprendre comment les données sont organisées et liées dans la base de données.

### Diagramme de classe

Le diagramme de classe représente la structure des classes Python utilisées dans le projet, montrant les attributs, les méthodes et les relations entre les classes. Il est utile pour comprendre l'architecture orientée objet du projet.

### Diagramme d'architecture

Le diagramme d'architecture représente la structure globale de l'application, montrant les différentes couches et leurs interactions. Il est utile pour comprendre comment les différentes parties de l'application fonctionnent ensemble.

## Structure du projet HBnB

Le projet HBnB est structuré en plusieurs couches :

1. **Couche Présentation** : API REST avec authentification JWT
2. **Couche Métier** : Façade (HBnBFacade) qui centralise la logique métier
3. **Couche Persistance** : Repositories qui gèrent l'accès aux données
4. **Couche Données** : Base de données SQLite/MySQL

Les entités principales du projet sont :

1. **User** : Utilisateurs de l'application
2. **Place** : Lieux/propriétés à louer
3. **Review** : Avis des utilisateurs sur les lieux
4. **Amenity** : Équipements/commodités disponibles dans les lieux 