from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from flask_bcrypt import Bcrypt  # Import Bcrypt

bcrypt = Bcrypt()  # Initialize the Bcrypt instance


def create_app(config_class="config.DevelopmentConfig"):
    # Create the Flask application
    app = Flask(__name__)

    bcrypt.init_app(app)  # Register the bcrypt instance

    # Load the configuration from the provided config_class
    app.config.from_object(config_class)

    # Initialize the API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
