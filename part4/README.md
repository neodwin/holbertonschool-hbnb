# Partie 4 – Client Web Simple

Dans cette phase, vous vous concentrerez sur le développement front-end de votre application en utilisant HTML5, CSS3 et JavaScript ES6. Votre tâche consiste à concevoir et implémenter une interface utilisateur interactive qui communique avec les services back-end que vous avez développés lors des parties précédentes du projet.

## Objectifs

* Développer une interface conviviale suivant les spécifications de design fournies.

* Implémenter les fonctionnalités côté client pour interagir avec l’API back-end.

* Garantir une gestion des données sécurisée et efficace avec JavaScript.

* Appliquer des pratiques modernes de développement web pour créer une application dynamique.

## Objectifs d’apprentissage

* Comprendre et utiliser HTML5, CSS3 et JavaScript ES6 dans un projet concret.

* Apprendre à interagir avec les services back-end en utilisant AJAX / Fetch API.

* Implémenter des mécanismes d’authentification et gérer les sessions utilisateur.

* Utiliser des scripts côté client pour améliorer l’expérience utilisateur sans recharger la page.


# Tâche 0: Design

## Réalisation

J'ai créé les fichiers HTML et CSS suivants conformément aux spécifications demandées:

1. **Structure HTML**:
   - `index.html`: Page principale avec la liste des lieux
   - `login.html`: Formulaire de connexion 
   - `place.html`: Page de détails d'un lieu
   - `add_review.html`: Formulaire pour ajouter un avis

2. **Styles CSS**:
   - J'ai utilisé une palette de couleurs avec du bleu comme couleur principale
   - Tous les cards (lieux et avis) ont:
     - Marge de 20px
     - Padding de 10px
     - Bordure de 1px solid #ddd
     - Rayon de bordure de 10px

3. **Éléments requis**:
   - Header avec logo et bouton de connexion
   - Footer avec mention de droits réservés
   - Barre de navigation avec liens pertinents
   - Cards pour les lieux avec nom, prix par nuit et bouton "View Details"
   - Section détaillée pour un lieu avec informations sur l'hôte, prix, description et équipements
   - Cards pour les avis avec le commentaire, le nom de l'utilisateur et la note
   - Bouton pour naviguer vers la page d'ajout d'avis

Tous les fichiers HTML sont valides selon les standards W3C. 

# Tâche 1: Login

## Réalisation

J'ai implémenté la fonctionnalité de login qui utilise l'API backend pour authentifier les utilisateurs. Voici les détails de l'implémentation :

1. **Ajout de l'écouteur d'événements pour le formulaire de connexion** :
   - Un écouteur d'événements est ajouté au formulaire de connexion pour intercepter la soumission
   - La soumission par défaut du formulaire est annulée avec `preventDefault()`
   - Les valeurs d'email et de mot de passe sont récupérées des champs du formulaire

2. **Validation des entrées** :
   - Vérification que les champs email et mot de passe ne sont pas vides
   - Affichage d'un message d'erreur si l'un des champs est vide

3. **Requête AJAX vers l'API** :
   - Utilisation de l'API Fetch pour envoyer une requête POST à l'endpoint de login
   - Envoi des données au format JSON avec les bons en-têtes
   - Point d'entrée utilisé : `http://localhost:3000/api/v1/auth/login`

4. **Gestion de la réponse** :
   - En cas de succès (statut 200) :
     - Stockage du jeton JWT dans un cookie valide pour 24 heures
     - Redirection vers la page principale (index.html)
   - En cas d'échec :
     - Affichage d'un message d'erreur adapté selon le code d'erreur reçu
     - Gestion spécifique des erreurs 401 (identifiants invalides) et 400 (requête incorrecte)

5. **Fonctions utilitaires** :
   - `showError()` : Pour afficher un message d'erreur dans l'élément spécifié
   - `clearError()` : Pour effacer un message d'erreur
   - `getCookie()` : Pour récupérer la valeur d'un cookie par son nom (sera utilisé dans les tâches suivantes)

## Utilisation

Pour tester la fonctionnalité de login, vous pouvez utiliser les identifiants suivants (basés sur les valeurs par défaut dans config.py & add_johndoe.py) :
- Email : admin@hbnb.io
- Mot de passe : admin1234

Ces identifiants correspondent à l'utilisateur administrateur créé par défaut dans la configuration du backend.

- Email : johndoe@test.com
- Mot de passe : johndoe1234

Ces identifiants correspondent à l'utilisateur classique créé par défaut dans la configuration du backend.

## Remarques

- La durée de validité du jeton JWT est fixée à 24 heures (86400 secondes)
- Tous les messages d'erreur sont affichés dans l'élément avec l'ID "login-error"
- Le formulaire valide à la fois côté client et côté serveur pour assurer l'intégrité des données 

# Tâche 2: Index

## Réalisation

J'ai implémenté les fonctionnalités pour la page d'index qui permet d'afficher et de filtrer la liste des logements, ainsi que de gérer l'affichage du bouton de connexion en fonction de l'état d'authentification de l'utilisateur.

1. **Vérification de l'authentification** :
   - J'ai créé une fonction `checkAuthentication()` qui vérifie la présence du jeton JWT dans les cookies
   - Si l'utilisateur est authentifié (le jeton existe), le lien de connexion est masqué
   - Si l'utilisateur n'est pas authentifié, le lien de connexion est affiché
   - Dans les deux cas, la fonction récupère la liste des logements

2. **Récupération des données de logements** :
   - J'ai implémenté une fonction `fetchPlaces()` qui envoie une requête GET à l'API
   - Si un jeton d'authentification est disponible, il est inclus dans l'en-tête Authorization
   - Les données des logements récupérées sont stockées dans une variable globale pour le filtrage
   - Les logements sont ensuite affichés sur la page

3. **Affichage des logements** :
   - La fonction `displayPlaces()` génère dynamiquement des cartes pour chaque logement
   - Chaque carte inclut une image, le titre du logement, le prix par nuit et un bouton pour voir les détails
   - Le prix est stocké comme attribut de données sur chaque carte pour faciliter le filtrage

4. **Filtrage par prix** :
   - J'ai ajouté un écouteur d'événements au menu déroulant de filtrage par prix
   - La fonction `filterPlacesByPrice()` filtre les logements en fonction du prix maximum sélectionné
   - Si l'option "All" est sélectionnée, tous les logements sont affichés
   - Sinon, seuls les logements dont le prix est inférieur ou égal au prix maximum sont affichés

5. **Intégration avec l'API backend** :
   - L'application communique avec l'API RESTful du backend
   - Point d'entrée utilisé pour récupérer les logements : `http://localhost:3000/api/v1/places`

## Remarques techniques

- Le filtrage des logements se fait côté client, sans recharger la page
- L'application fonctionne pour les utilisateurs authentifiés et non authentifiés
- Les utilisateurs non authentifiés peuvent voir la liste des logements mais verront le lien de connexion
- Les utilisateurs authentifiés ne verront pas le lien de connexion
- En cas d'erreur lors de la récupération des données, un message d'erreur est affiché dans la console

## Test de la fonctionnalité

Pour tester cette fonctionnalité :
1. Visitez la page d'index sans être connecté - le lien de connexion devrait être visible
2. Connectez-vous avec des identifiants valides, puis retournez à la page d'index - le lien de connexion devrait être masqué
3. Testez le filtrage en sélectionnant différentes options de prix dans le menu déroulant 

# Tâche 3: Place details

## Réalisation

J'ai implémenté les fonctionnalités pour la page de détails d'un logement qui permet d'afficher toutes les informations concernant un logement spécifique, ses équipements et ses avis. La page gère également l'affichage conditionnel du formulaire pour ajouter un avis en fonction de l'authentification de l'utilisateur.

1. **Extraction de l'ID du logement depuis l'URL** :
   - J'ai implémenté la fonction `getPlaceIdFromURL()` qui extrait l'ID du logement à partir des paramètres de l'URL
   - L'application vérifie que l'ID du logement est valide avant de continuer

2. **Vérification de l'authentification** :
   - La fonction `checkAuthenticationForPlaceDetails()` vérifie la présence du jeton JWT dans les cookies
   - Si l'utilisateur est authentifié, le lien de connexion est masqué et le bouton pour ajouter un avis est affiché
   - Si l'utilisateur n'est pas authentifié, le lien de connexion est affiché et le bouton pour ajouter un avis est masqué

3. **Récupération des détails du logement** :
   - La fonction `fetchPlaceDetails()` envoie une requête GET à l'API pour récupérer les informations détaillées du logement
   - L'URL utilisée est `http://localhost:3000/api/v1/places/{placeId}`
   - Si un jeton d'authentification est disponible, il est inclus dans l'en-tête Authorization
   - En cas de succès, les détails du logement sont affichés et les avis sont ensuite récupérés

4. **Récupération des avis** :
   - La fonction `fetchPlaceReviews()` envoie une requête GET à l'API pour récupérer les avis associés au logement
   - L'URL utilisée est `http://localhost:3000/api/v1/places/{placeId}/reviews/`
   - Les avis récupérés sont affichés dans la section prévue à cet effet

5. **Affichage des détails du logement** :
   - La fonction `displayPlaceDetails()` génère dynamiquement le contenu HTML pour afficher les détails du logement
   - Elle crée une section pour les informations générales (titre, prix, description, hôte)
   - Elle affiche la liste des équipements du logement
   - Elle prépare la section des avis
   - Elle gère l'affichage conditionnel du bouton pour ajouter un avis

6. **Affichage des avis** :
   - La fonction `displayPlaceReviews()` génère dynamiquement des cartes pour chaque avis
   - Chaque carte affiche le nom de l'utilisateur, une notation par étoiles et le texte de l'avis
   - Si aucun avis n'existe, un message approprié est affiché

7. **Gestion des erreurs** :
   - L'application gère les erreurs potentielles lors de la récupération des données
   - Des messages d'erreur explicites sont affichés en cas de problème

## Remarques techniques

- L'affichage conditionnel des éléments est basé sur l'état d'authentification de l'utilisateur
- La notation par étoiles est générée dynamiquement en fonction de la valeur numérique de la note
- L'application gère le cas où l'ID du logement est invalide ou manquant
- Le bouton pour ajouter un avis redirige vers la page add_review.html avec l'ID du logement en paramètre

## Test de la fonctionnalité

Pour tester cette fonctionnalité :
1. Visitez la page d'index et cliquez sur le bouton "View Details" d'un logement
2. Vérifiez que les détails du logement et les avis s'affichent correctement
3. Sans être connecté, vérifiez que le lien de connexion est visible et que le bouton pour ajouter un avis est masqué
4. Connectez-vous, puis retournez à la page de détails pour vérifier que le lien de connexion est masqué et que le bouton pour ajouter un avis est visible 

# Tâche 4: Add Review form

## Réalisation

J'ai implémenté les fonctionnalités pour la page d'ajout d'avis qui permet aux utilisateurs authentifiés de soumettre des critiques pour un logement spécifique. L'application vérifie l'authentification de l'utilisateur et redirige les utilisateurs non authentifiés vers la page d'accueil.

1. **Vérification de l'authentification** :
   - La fonction `checkAuthenticationForAddReview()` vérifie la présence du jeton JWT dans les cookies
   - Si l'utilisateur n'est pas authentifié, il est automatiquement redirigé vers la page d'accueil
   - Si l'utilisateur est authentifié, le lien de connexion est masqué et le formulaire est affiché

2. **Extraction de l'ID du logement depuis l'URL** :
   - La fonction `getPlaceIdFromURL()` extrait l'ID du logement à partir des paramètres de l'URL
   - L'application vérifie que l'ID du logement est valide avant de continuer
   - Le bouton "Cancel" est mis à jour dynamiquement pour rediriger vers la page de détails du logement correct

3. **Configuration du formulaire** :
   - La fonction `setupReviewFormSubmission()` ajoute un écouteur d'événements pour intercepter la soumission du formulaire
   - Le formulaire recueille les données de notation (1-5 étoiles) et le texte de l'avis
   - Une validation basique est effectuée pour s'assurer que tous les champs sont remplis

4. **Soumission de l'avis à l'API** :
   - La fonction `submitReview()` prépare et envoie les données de l'avis à l'API
   - L'application récupère d'abord les informations de l'utilisateur actuel via l'endpoint `/auth/me`
   - Les données complètes (texte de l'avis, notation, ID utilisateur, ID logement) sont envoyées à l'endpoint `/reviews`
   - Le jeton JWT est inclus dans l'en-tête Authorization pour authentifier la requête

5. **Gestion des réponses de l'API** :
   - En cas de succès, un message de confirmation est affiché et le formulaire est réinitialisé
   - Après 2 secondes, l'utilisateur est redirigé vers la page de détails du logement
   - En cas d'échec, un message d'erreur approprié est affiché

6. **Affichage des messages** :
   - La fonction `showMessage()` permet d'afficher des messages de succès ou d'erreur
   - Les messages sont stylisés différemment selon leur type (succès ou erreur)

## Remarques techniques

- L'application effectue plusieurs appels API :
  - Récupération des informations de l'utilisateur authentifié via `/auth/me`
  - Soumission de l'avis via `/reviews`
- Le bouton "Cancel" est configuré dynamiquement pour renvoyer l'utilisateur à la page du logement correct
- La redirection post-soumission améliore l'expérience utilisateur en montrant l'avis ajouté dans la liste des avis
- Des messages explicites sont affichés pour chaque étape du processus

## Test de la fonctionnalité

Pour tester cette fonctionnalité :
1. Essayez d'accéder à la page add_review.html sans être connecté - vous devriez être redirigé vers la page d'accueil
2. Connectez-vous et accédez à la page de détails d'un logement
3. Cliquez sur le bouton "Add a Review" et vérifiez que vous êtes bien dirigé vers le formulaire
4. Soumettez un avis avec une notation et un texte
5. Vérifiez que l'avis est soumis avec succès et que vous êtes redirigé vers la page de détails
6. Confirmez que votre nouvel avis apparaît dans la liste des avis pour ce logement

## Auteur 
* [Edwin Dervaux](https://github.com/neodwin)
