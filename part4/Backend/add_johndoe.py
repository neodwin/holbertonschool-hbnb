from app import create_app
from app.services import facade
from app.models.user import User

app = create_app()

with app.app_context():
    # Définir les informations du nouvel utilisateur
    # Ne pas hasher le mot de passe ici, le modèle User le fera automatiquement
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@test.com",
        "password": "johndoe1234", # mot de passe en clair, sera hashé par le modèle User
        "is_admin": False
    }
    
    # Vérifier si l'utilisateur existe déjà (par email)
    existing_user = facade.get_user_by_email(user_data["email"])
    
    if existing_user:
        print(f"L'utilisateur avec l'email {user_data['email']} existe déjà.")
        print(f"Suppression de cet utilisateur pour le recréer correctement...")
        
        # Supprimer l'utilisateur existant
        try:
            # Récupérer l'ID de l'utilisateur existant
            user_id = existing_user.id
            
            # Supprimer l'utilisateur de la base de données
            from app.extensions import db
            db.session.delete(existing_user)
            db.session.commit()
            
            print(f"Utilisateur supprimé avec succès.")
            
            # Créer un nouvel utilisateur avec les mêmes informations
            new_user = facade.create_user(user_data)
            print(f"Utilisateur recréé avec succès:")
            print(f"ID: {new_user.id}")
            print(f"Nom: {new_user.first_name} {new_user.last_name}")
            print(f"Email: {new_user.email}")
            print(f"Admin: {new_user.is_admin}")
            print("\nVous pouvez maintenant vous connecter avec:")
            print(f"Email: {user_data['email']}")
            print(f"Mot de passe: {user_data['password']}")
        except Exception as e:
            print(f"Erreur lors de la suppression/recréation de l'utilisateur: {e}")
    else:
        # Créer l'utilisateur
        try:
            new_user = facade.create_user(user_data)
            print(f"Nouvel utilisateur créé avec succès:")
            print(f"ID: {new_user.id}")
            print(f"Nom: {new_user.first_name} {new_user.last_name}")
            print(f"Email: {new_user.email}")
            print(f"Admin: {new_user.is_admin}")
            print("\nVous pouvez maintenant vous connecter avec:")
            print(f"Email: {user_data['email']}")
            print(f"Mot de passe: {user_data['password']}")
        except Exception as e:
            print(f"Erreur lors de la création de l'utilisateur: {e}") 